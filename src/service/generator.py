"""Board generation service."""

from __future__ import annotations

import random
from typing import Optional

from src.types.grid import Grid, Path, Position
from src.types.board import BoardState
from src.config.game import GAME_CONFIG
from src.providers.dictionary import get_dictionary
from src.utils.grid import positions_to_path


def generate_board(
    theme_words: list[str],
    spangram: str | None = None,
    seed: int | None = None
) -> BoardState:
    """
    Generate a new Strands puzzle board.
    
    Args:
        theme_words: List of theme words
        spangram: Optional spangram (must touch two opposite sides)
        seed: Optional random seed
        
    Returns:
        BoardState with generated grid and found_words list
    """
    if seed is not None:
        random.seed(seed)
    
    # Normalize theme words
    theme_words = [w.upper() for w in theme_words]
    
    # Calculate total cells needed
    total_theme_cells = sum(len(w) for w in theme_words)
    
    # Place spangram first if provided
    if spangram and is_valid_spangram(spangram):
        spangram = spangram.upper()
        grid, placed_words = _place_spangram(theme_words, spangram)
    else:
        # Place all theme words
        grid, placed_words = _place_theme_words(theme_words)
    
    # Fill empty cells with random letters
    grid = _fill_empty_cells(grid)
    
    # Create initial board state
    found_words = []
    
    return BoardState(grid=grid, score=0, found_words=found_words)


def is_valid_spangram(word: str) -> bool:
    """
    Check if a word can be a valid spangram.
    
    Args:
        word: Potential spangram
        
    Returns:
        True if word can be placed as spangram
    """
    return (len(word) >= 6 and  # At least 6 letters for grid span
            len(word) <= 8)


def _place_spangram(
    theme_words: list[str],
    spangram: str
) -> tuple[Grid, set[str]]:
    """
    Place spangram first, then remaining theme words.
    
    Returns:
        Tuple of (grid, set of placed words)
    """
    # Initialize empty grid
    grid: Grid = [
        [""] * GAME_CONFIG.GRID_COLS
        for _ in range(GAME_CONFIG.GRID_ROWS)
    ]
    
    placed_words: set[str] = {spangram}
    
    # Place spangram (horizontal in middle rows)
    row = GAME_CONFIG.GRID_ROWS // 2
    col = 0
    for i, letter in enumerate(spangram):
        grid[row][col + i] = letter
    
    # Place remaining theme words around spangram
    remaining_words = theme_words
    
    for word in remaining_words:
        if word.upper() in placed_words:
            continue
        
        if _try_place_word(grid, word.upper()):
            placed_words.add(word.upper())
    
    return grid, placed_words


def _place_theme_words(theme_words: list[str]) -> tuple[Grid, set[str]]:
    """
    Place all theme words on the grid.
    
    Returns:
        Tuple of (grid, set of placed words)
    """
    grid: Grid = [
        [""] * GAME_CONFIG.GRID_COLS
        for _ in range(GAME_CONFIG.GRID_ROWS)
    ]
    
    placed_words: set[str] = set()
    
    # Sort by length (longest first for better placement)
    sorted_words = sorted(theme_words, key=len, reverse=True)
    
    for word in sorted_words:
        word_upper = word.upper()
        
        # Skip duplicates
        if word_upper in placed_words:
            continue
        
        # Try to place the word
        if _try_place_word(grid, word_upper):
            placed_words.add(word_upper)
    
    return grid, placed_words


def _try_place_word(grid: Grid, word: str) -> bool:
    """
    Try to place a word on the grid.
    
    Args:
        grid: Current grid state
        word: Word to place
        
    Returns:
        True if word was placed successfully
    """
    # Try various starting positions and directions
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    
    for row in range(GAME_CONFIG.GRID_ROWS):
        for col in range(GAME_CONFIG.GRID_COLS):
            for dr, dc in directions:
                if _can_place_word(grid, word, (row, col), (dr, dc)):
                    _place_word_at(grid, word, (row, col), (dr, dc))
                    return True
    
    return False


def _can_place_word(
    grid: Grid,
    word: str,
    start: Position,
    direction: tuple[int, int]
) -> bool:
    """
    Check if a word can be placed at position in direction.
    
    Args:
        grid: Current grid state
        word: Word to place
        start: Starting position
        direction: (row_delta, col_delta)
        
    Returns:
        True if word can be placed
    """
    dr, dc = direction
    row, col = start
    
    # Check if word fits
    end_row = row + (len(word) - 1) * dr
    end_col = col + (len(word) - 1) * dc
    
    if (end_row < 0 or end_row >= GAME_CONFIG.GRID_ROWS or
        end_col < 0 or end_col >= GAME_CONFIG.GRID_COLS):
        return False
    
    # Check for conflicts
    for i, letter in enumerate(word):
        check_row = row + i * dr
        check_col = col + i * dc
        
        cell = grid[check_row][check_col]
        if cell and cell != letter:
            return False
    
    return True


def _place_word_at(
    grid: Grid,
    word: str,
    start: Position,
    direction: tuple[int, int]
) -> None:
    """
    Place a word on the grid at position in direction.
    
    Args:
        grid: Grid to modify
        word: Word to place
        start: Starting position
        direction: (row_delta, col_delta)
    """
    dr, dc = direction
    row, col = start
    
    for i, letter in enumerate(word):
        check_row = row + i * dr
        check_col = col + i * dc
        grid[check_row][check_col] = letter


def _fill_empty_cells(grid: Grid) -> Grid:
    """
    Fill empty cells with random letters.
    
    Args:
        grid: Current grid state
        
    Returns:
        Grid with empty cells filled
    """
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    for row in range(GAME_CONFIG.GRID_ROWS):
        for col in range(GAME_CONFIG.GRID_COLS):
            if grid[row][col] == "":
                grid[row][col] = random.choice(alphabet)
    
    return grid


__all__ = [
    "generate_board",
    "is_valid_spangram",
]
