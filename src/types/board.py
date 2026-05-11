"""Board state type definitions."""

from __future__ import annotations

from dataclasses import dataclass

from src.types.grid import LetterGrid
from src.types.game import WordResult


@dataclass
class BoardState:
    """Represents the current state of the game board."""
    grid: LetterGrid
    found_words: list[WordResult]
    score: int
    hints_found: int
