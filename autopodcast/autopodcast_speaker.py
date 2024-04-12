class AutoPodcastSpeaker:
    def __init__(
        self,
        name="John Doe",
        age=32,
        bio="John has been a radio host for 10 years. He covers any subject with ease, and brings a fresh entertainment style.",
    ) -> None:
        self.name = name
        self.age = age
        self.bio = bio


def speaker_line_error(message):
    return ValueError(
        f"Illegal speaker line format! {message}\n\nValid formats:\n\nSome Name (XY years old) - Some bio here\nSome Name - Some bio here\nSome Name (XY years old) - Some bio here\nSome Name - Some bio here"
    )


def parse_speaker(speaker_line: str) -> AutoPodcastSpeaker:
    # Format is this:
    # Some Name (XY years old) - Some bio here
    speaker_line_stripped = speaker_line.strip()
    lparen_index = speaker_line_stripped.find("(")
    rparen_index = speaker_line_stripped.find(")")

    if lparen_index == -1 or rparen_index == -1:
        raise speaker_line_error("Speaker line must contain age in parentheses")

    speaker_name = speaker_line_stripped[:lparen_index].strip()
    speaker_age_text = speaker_line_stripped[lparen_index + 1 : rparen_index].strip()

    # Extract number from age text
    age = 0
    for char in speaker_age_text:
        if char.isdigit():
            age = age * 10 + int(char)
        else:
            break

    if age == 0:
        raise speaker_line_error("Age must be a positive integer")

    bio = speaker_line_stripped[rparen_index + 1 :].strip()
    if bio.startswith("-"):
        bio = bio[1:].strip()

    return AutoPodcastSpeaker(name=speaker_name, age=age, bio=bio)
