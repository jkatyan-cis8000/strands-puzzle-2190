"""Service module exports."""

from __future__ import annotations

from src.service.generator import generate_board
from src.service.validator import validate_play, check_completion, validate_positions
from src.service.scorer import calculate_score, get_hint, track_hints

__all__ = [
    "generate_board",
    "validate_play",
    "check_completion",
    "validate_positions",
    "calculate_score",
    "get_hint",
    "track_hints",
]
