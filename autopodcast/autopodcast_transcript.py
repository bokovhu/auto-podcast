class AutoPodcastTranscript:
    def __init__(self, speaker=None, text="") -> None:
        self.speaker = speaker
        self.text = text
        self.speech = None
