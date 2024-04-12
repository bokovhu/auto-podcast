import argparse
import autopodcast
import dotenv
import os
import multiprocessing
import io
from pydub import AudioSegment
import asyncio
import concurrent.futures


async def main():
    dotenv.load_dotenv()

    parser = argparse.ArgumentParser(
        description="This CLI uses generative AI to generate an entire podcast."
    )

    parser.add_argument(
        "--toc-model",
        type=str,
        default="gpt-4",
        help="The model to use for the Table of Contents",
    )
    parser.add_argument(
        "--transcript-model",
        type=str,
        default="gpt-4",
        help="The model to use for the Transcript",
    )
    parser.add_argument(
        "--speech-model",
        type=str,
        default="tts-1",
        help="The model to use for the Speech",
    )
    parser.add_argument(
        "--speech-voice",
        type=str,
        default="alloy",
        help="The voice to use for the Speech",
    )
    parser.add_argument(
        "--topic",
        type=str,
        default="Create a podcast, revolving around cats: how we love them, what traditions there are in the world around them, what they like to eat, and other interesting topics.",
        help="The topic of the podcast",
    )
    parser.add_argument(
        "--toc-temperature",
        type=float,
        default=0.5,
        help="The temperature to use for the Table of Contents",
    )
    parser.add_argument(
        "--transcript-temperature",
        type=float,
        default=0.5,
        help="The temperature to use for the Transcript",
    )
    parser.add_argument(
        "--toc-tokens",
        type=int,
        default=4000,
        help="The max tokens to use for the Table of Contents",
    )
    parser.add_argument(
        "--transcript-tokens",
        type=int,
        default=4000,
        help="The max tokens to use for the Transcript",
    )
    parser.add_argument(
        "--openai-token",
        type=str,
        help="The OpenAI API token to use for the agent",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output",
        help="The output filename prefix",
    )

    args = parser.parse_args()

    openai_token = args.openai_token or os.getenv("OPENAI_API_KEY")

    agent = autopodcast.AutoPodcastAgent(openai_token=openai_token)
    request = autopodcast.AutoPodcastRequest(
        toc_model=args.toc_model,
        transcript_model=args.transcript_model,
        topic=args.topic,
        toc_temperature=args.toc_temperature,
        transcript_temperature=args.transcript_temperature,
        toc_tokens=args.toc_tokens,
        transcript_tokens=args.transcript_tokens,
        speech_model=args.speech_model,
        speech_voice=args.speech_voice,
    )

    print("Generating Table of Contents ...")
    toc = agent.generate_toc(request)

    async def do_generate_chapters(executor):
        loop = asyncio.get_running_loop()
        tasks = []

        async def one_task(chapter, semaphore):
            await semaphore.acquire()
            try:
                print(
                    f"Generating '{chapter.title}' ({chapter.chapter_index} / {len(toc.chapters)}) ..."
                )
                return await loop.run_in_executor(
                    executor,
                    agent.generate_chapter_transcript,
                    request,
                    toc,
                    chapter,
                )
            finally:
                semaphore.release()

        sem = asyncio.Semaphore(4)

        for chapter in toc.chapters:
            tasks.append(one_task(chapter, sem))
        return await asyncio.gather(*tasks)

    async def do_generate_chapter_speech(executor):
        loop = asyncio.get_running_loop()
        tasks = []

        async def one_task(chapter, semaphore):
            await semaphore.acquire()
            try:
                for tr in chapter.transcript:
                    speech_mp3 = await loop.run_in_executor(
                        executor, agent.generate_transcript_speech, request, tr
                    )
                    speech_segment = AudioSegment.from_file(
                        io.BytesIO(speech_mp3), format="mp3"
                    )
                    tr.speech = speech_segment
            finally:
                semaphore.release()

        sem = asyncio.Semaphore(4)

        for chapter in toc.chapters:
            tasks.append(one_task(chapter, sem))
        return await asyncio.gather(*tasks)

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        chapter_results = await do_generate_chapters(executor)
        for i in range(len(toc.chapters)):
            toc.chapters[i].transcript = chapter_results[i]
        await do_generate_chapter_speech(executor)

    print("Exporting ...")

    txt_content = ""
    audio_content = AudioSegment.silent(duration=0)
    for chapter in toc.chapters:
        txt_content += f"# {chapter.title}\n\n"
        txt_content += "\n\n".join([t.text for t in chapter.transcript])
        txt_content += "\n\n"
        for tr in chapter.transcript:
            audio_content += tr.speech

    with open(f"{args.output}.md", "w") as f:
        f.write(txt_content)

    audio_content.export(f"{args.output}.mp3", format="mp3")


if __name__ == "__main__":
    asyncio.run(main())
