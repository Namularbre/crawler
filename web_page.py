from datetime import date


class WebPage:
    def __init__(self, url: str, content: str | None = None, blacklisted: bool = False) -> None:
        self.url = url
        self.content = content
        self.blacklisted = blacklisted
        self.created_at = date.today()

    def to_dict(self) -> dict:
        return {
            'url': self.url,
            'text': self.content,
            'blacklisted': self.blacklisted,
            'createdAt': self.created_at
        }

    def __str__(self) -> str:
        return f"url: {self.url}, blacklisted: {self.blacklisted}"

    def __eq__(self, other) -> bool:
        if isinstance(other, WebPage):
            return hash(self) == hash(other)
        return False

    def __key(self) -> tuple[str, str, bool]:
        return self.url, self.content, self.blacklisted

    def __hash__(self) -> int:
        return hash(self.__key())
