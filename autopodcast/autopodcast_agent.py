from .autopodcast_request import AutoPodcastRequest
from .autopodcast_toc import AutoPodcastTableOfContents
from .autopodcast_chapter import AutoPodcastChapter
from .autopodcast_transcript import AutoPodcastTranscript
from .autopodcast_speaker import AutoPodcastSpeaker
import openai


class AutoPodcastAgent:
    def __init__(
        self,
        openai_token: str,
    ) -> None:
        self.client = openai.OpenAI(api_key=openai_token)

    def generate_toc(self, request: AutoPodcastRequest) -> AutoPodcastTableOfContents:
        messages = [
            {
                "role": "system",
                "content": "Generate the table of contents for the transcript of podcast, revolving around the topic and instructions given by the user. You MUST respond with nothing else, just the table of contents in a specific format. In each line, write a single sentence description of the chapter, then between `(` and `)` (parentheses) write the number of sentences in that chapter's transcript!",
            },
            {
                "role": "user",
                "content": "Create a podcast in the topic of mathematics, specifically algebra.",
            },
            {
                "role": "assistant",
                "content": """
Exploring the origins and fundamental concepts of algebra (10 sentences)
Understanding variables, constants, coefficients, and algebraic expressions (20 sentences)
Step-by-step methods to solve single-variable linear equations (20 sentences)
Techniques and significance of graphing linear equations and understanding slopes and intercepts (20 sentences)
Exploring methods to solve systems of equations including substitution and elimination (20 sentences)
An in-depth look at polynomials, degrees, and the process of factoring them (20 sentences)
Understanding the nature of quadratic equations, methods to solve them, and their applications (20 sentences)
Diving into the concepts and uses of exponential growth and logarithmic functions (20 sentences)
Discussing how algebra is used in various fields such as engineering, physics, and economics (20 sentences)
Exploring the evolving role of algebra in technology and education (10 sentences)
Summarizing key points discussed and the importance of algebra in problem-solving and critical thinking (10 sentences)
""".strip(),
            },
            {"role": "user", "content": request.topic.strip()},
        ]
        response = self.client.chat.completions.create(
            model=request.toc_model,
            messages=messages,
            temperature=request.toc_temperature,
            max_tokens=request.toc_tokens,
        )
        response_message = response.choices[0].message.content
        toc = AutoPodcastTableOfContents()
        for line in response_message.strip().split("\n"):
            try:
                toc.add_chapter(line)
            except Exception as e:
                print(f"Error adding chapter from line `{line}`: \n    -> {e}")
        return toc

    def generate_chapter_transcript(
        self,
        request: AutoPodcastRequest,
        toc: AutoPodcastTableOfContents,
        chapter: AutoPodcastChapter,
    ) -> list[AutoPodcastTranscript]:
        messages = [
            {
                "role": "system",
                "content": f"Generate the transcript for the chapter of a podcast, for the chapter that the user is requesting. You MUST respond with NOTHING ELSE, only the transcript which will be read by the speaker in THAT given chapter of the podcast! Make sure the text flows naturally between chapters, do not start with phrases like 'Welcome to chapter X'!",
            },
            {
                "role": "user",
                "content": "Podcast topic: Create a podcast in the topic of mathematics, specifically algebra.\nChapter (1 / 11): Exploring the origins and fundamental concepts of algebra (10 sentences)",
            },
            {
                "role": "assistant",
                "content": """Welcome to our exploration into algebra, a branch of mathematics that plays a critical role in various aspects of both academic and everyday life. Algebra began in the ancient civilizations of Babylon and Egypt, where it was used to solve practical problems related to commerce, property inheritance, and the measurement of land. The term "algebra" itself comes from the Arabic word "al-jabr," which means "the reunion of broken parts," introduced by the mathematician Al-Khwarizmi in the 9th century. Algebra is fundamentally about finding the unknowns, typically represented as variables like x and y, by manipulating mathematical expressions according to a set of rules. One of the basic concepts in algebra is the equation, which is a statement of equality containing one or more variables. Solving an equation involves finding the values of the variables that make the equality true. In addition to equations, algebra deals with functions, which are mathematical expressions that describe a relationship between different quantities. Functions are vital for understanding how one quantity changes in response to another. As we delve deeper into algebra, we'll see how these relationships can be represented graphically, which helps in visualizing and solving more complex problems. Throughout this podcast, we'll explore how algebra is not just about numbers and equations but is also a language that describes the structure and patterns of the world around us.""",
            },
            {
                "role": "user",
                "content": "Podcast topic: Space exploration, and privatization of the space industry.\nChapter (5 / 9): Legal and Ethical Considerations (20 sentences)",
            },
            {
                "role": "assistant",
                "content": """The privatization of the space industry brings not only technological and economic opportunities but also complex legal and ethical questions. As companies like SpaceX and Blue Origin become major players in what was once a field dominated by national governments, the need for robust legal frameworks becomes apparent. International space law, primarily governed by treaties like the Outer Space Treaty of 1967, was crafted in an era when only nations were capable of space endeavors.

This treaty, along with others, stipulates that space shall be free for exploration and use by all nations, but must be done for the benefit of all humanity. However, these agreements did not foresee the rise of private space companies. As a result, questions arise about property rights, mining rights, and even the potential militarization of space by private entities. For instance, who owns the resources extracted from an asteroid or the Moon? The current legal framework provides a vague answer at best.

Ethically, the expansion of private companies into space raises concerns about the equitable use of outer space. The concept of space being the "province of all mankind" is at odds with activities that might prioritize profit over global cooperation and benefit. There is also the risk of creating a monopolistic control over space resources by a few wealthy entities or individuals, potentially sidelining poorer nations.

Furthermore, there are concerns about the accountability of private companies in space. Governments are subject to public scrutiny and international pressures that private companies often evade. Incidents like spacecraft malfunctions or collisions in space that could create debris and pose hazards to other spacecraft and satellites need stringent oversight.

Efforts to address these issues involve both updating existing treaties and forming new international agreements that include the perspectives of both private enterprises and global stakeholders. This evolving legal landscape must balance innovation and enterprise with responsibility and inclusivity to ensure that space remains a realm for all humanity to explore and benefit from, not just a playground for the affluent.""",
            },
            {
                "role": "user",
                "content": f"Podcast topic: {request.topic.strip()}\nChapter ({chapter.chapter_index} / {len(toc.chapters)}): {chapter.title} ({chapter.sentence_count} sentences)",
            },
        ]
        ai_speaker = AutoPodcastSpeaker(name="AI", age=0, bio="AI generated speaker")
        response = self.client.chat.completions.create(
            model=request.transcript_model,
            messages=messages,
            temperature=request.transcript_temperature,
            max_tokens=request.transcript_tokens,
        )
        response_message = response.choices[0].message.content
        transcript = []
        for line in response_message.strip().split("\n"):
            if line.strip():
                transcript.append(
                    AutoPodcastTranscript(speaker=ai_speaker, text=line.strip())
                )

        return transcript

    def generate_transcript_speech(
        self, request: AutoPodcastRequest, transcript: AutoPodcastTranscript
    ):
        response = self.client.audio.speech.create(
            response_format="mp3",
            voice=request.speech_voice,
            model=request.speech_model,
            input=transcript.text,
        )
        return response.content
