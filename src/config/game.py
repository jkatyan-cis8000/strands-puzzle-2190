"""Game configuration constants."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class GameConfig:
    """Configuration for the Strands puzzle game."""
    
    # Grid dimensions
    GRID_ROWS: int = 6
    GRID_COLS: int = 8
    
    # Word length constraints
    MIN_WORD_LENGTH: int = 4
    MAX_WORD_LENGTH: int = 8
    
    # Scoring
    POINTS_PER_LETTER: int = 1
    SPANGRAM_BONUS: int = 5
    HINT_REVEAL_SCORE: int = 100
    
    # Hints
    MAX_HINTS: int = 3
    HINTS_PER_NON_THEME: int = 3  # Unlocks hint every 3 non-theme words
    
    # Game flow
    MAX_UNCOVERED_CELLS: int = 4  # Allow up to 4 cells uncovered for completion


# Global config instance
GAME_CONFIG = GameConfig()

__all__ = ["GameConfig", "GAME_CONFIG"]
