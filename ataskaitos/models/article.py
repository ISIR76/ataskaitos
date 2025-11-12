"""Scientific Article domain model."""

from dataclasses import dataclass


@dataclass
class ScientificArticle:
    """Scientific article for SMSM standards evaluation."""

    description: str
    char_count: int = 0
    metadata: dict | None = None

    def __post_init__(self):
        if self.char_count == 0:
            self.char_count = len(self.description)
        if self.metadata is None:
            self.metadata = {}

    @property
    def author_sheets(self) -> float:
        """Calculate number of author's sheets (1 sheet = 40,000 characters)."""
        return self.char_count / 40000
