"""Report (R&D Activity) domain model."""

from dataclasses import dataclass


@dataclass
class RDActivity:
    """Research and Development Activity for Frascati evaluation."""

    description: str
    char_count: int = 0
    metadata: dict | None = None

    def __post_init__(self):
        if self.char_count == 0:
            self.char_count = len(self.description)
        if self.metadata is None:
            self.metadata = {}
