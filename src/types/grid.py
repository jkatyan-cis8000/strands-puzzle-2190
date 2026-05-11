"""Grid type definitions."""

from __future__ import annotations

from typing import TypeAlias

Grid: TypeAlias = list[list[str]]
"""A 6x8 grid represented as a list of lists."""

LetterGrid: TypeAlias = list[list[str]]
"""A grid containing letters (the playing board)."""

Position: TypeAlias = tuple[int, int]
"""A position in the grid as (row, col)."""

Path: TypeAlias = list[Position]
"""A path through the grid, representing a word."""
