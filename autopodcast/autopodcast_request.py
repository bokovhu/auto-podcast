class AutoPodcastRequest:
    def __init__(
        self,
        toc_model="gpt-4",
        transcript_model="gpt-4",
        topic="Create a podcast in a random topic",
        toc_temperature=0.5,
        transcript_temperature=0.5,
        toc_tokens=4000,
        transcript_tokens=4000,
        speech_model="tts-1",
        speech_voice="alloy",
    ) -> None:
        self.toc_model = toc_model
        self.transcript_model = transcript_model
        self.topic = topic
        self.toc_temperature = toc_temperature
        self.transcript_temperature = transcript_temperature
        self.toc_tokens = toc_tokens
        self.transcript_tokens = transcript_tokens
        self.speech_model = speech_model
        self.speech_voice = speech_voice
