def chapter_line_error(message):
    return ValueError(
        f"Illegal chapter line format! {message}\n\nValid formats:\n\nChapter One (123 sentences)\nChapter One: In this chapter, we introduce things (123 sentences)\nChapter One - In this chapter, we introduce things (123 sentences)"
    )


class AutoPodcastChapter:
    def __init__(self, title="", sentence_count=0) -> None:
        self.title = title
        self.sentence_count = sentence_count
        self.chapter_index = 0
        self.transcript = []


def parse_toc_chapter(chapter_line: str) -> AutoPodcastChapter:
    list_item_symbols = ["-", "*", "#", "##", "###", "####", "#####", "."]

    # Remove preceeding list item symbols
    chapter_line_stripped = chapter_line.strip()
    for symbol in list_item_symbols:
        if chapter_line_stripped.startswith(symbol):
            chapter_line_stripped = chapter_line_stripped[len(symbol) :].strip()

    # Possible formats:
    # <chapter_title> (<sentence_count> [sentences])
    # <chapter_title>: <chapter_description> (<sentence_count> [sentences])
    # <chapter_title> - <chapter_description> (<sentence_count> [sentences])

    # Find last lparent and rparen
    lparen_index = chapter_line_stripped.rfind("(")
    rparen_index = chapter_line_stripped.rfind(")")

    if lparen_index == -1 or rparen_index == -1:
        raise chapter_line_error(
            "Chapter line must contain a sentence count in parentheses"
        )

    if lparen_index >= rparen_index:
        raise chapter_line_error(
            "Chapter line must contain a sentence count in parentheses"
        )

    chapter_title = chapter_line_stripped[:lparen_index].strip()
    chapter_sentence_count_text = chapter_line_stripped[
        lparen_index + 1 : rparen_index
    ].strip()

    # Extract number from sentence count text
    sentence_count = 0
    for char in chapter_sentence_count_text:
        if char.isdigit():
            sentence_count = sentence_count * 10 + int(char)
        else:
            break

    if sentence_count == 0:
        raise chapter_line_error("Sentence count must be a positive integer")

    return AutoPodcastChapter(title=chapter_title, sentence_count=sentence_count)
