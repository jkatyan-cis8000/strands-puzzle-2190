"""Hint system type definitions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class HintType(Enum):
    """Types of hints available."""
    THEME = "theme"
    WORD_LENGTH = "word_length"
    LOCATION = "location"
    EXAMPLE = "example"


@dataclass
class Hint:
    """A hint that can be unlocked."""
    hint_type: HintType
    description: str
    cost: int  # Non-theme words needed to unlock
