"""Game and word result type definitions."""

from __future__ import annotations

from dataclasses import dataclass

from src.types.grid import Path


@dataclass
class WordResult:
    """Represents a word found on the board."""
    word: str
    positions: Path
    is_spangram: bool
    is_theme: bool
    points: int


@dataclass
class PlayResult:
    """Result of a player's play."""
    words_found: list[WordResult]
    score_delta: int
    hints_unlocked: int


@dataclass
class GameState:
    """Represents the full game state."""
    board: BoardState
    theme_words: set[str]
    spangram: str
    all_words: set[str]
    game_over: bool
