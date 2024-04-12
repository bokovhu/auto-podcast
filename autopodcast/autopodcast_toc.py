from .autopodcast_chapter import parse_toc_chapter


class AutoPodcastTableOfContents:
    def __init__(self) -> None:
        self.chapters = []

    def add_chapter(self, chapter_line: str):
        chapt = parse_toc_chapter(chapter_line)
        chapt.chapter_index = len(self.chapters) + 1
        self.chapters.append(chapt)
