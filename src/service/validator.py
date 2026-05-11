"""Play validation service."""

from __future__ import annotations

from src.types.grid import Grid, Path
from src.types.board import BoardState
from src.types.game import WordResult, PlayResult
from src.config.game import GAME_CONFIG
from src.utils.grid import is_valid_path
from src.utils.word import has_repeated_positions


def validate_positions(grid: Grid, path: Path) -> bool:
    """
    Validate a path of positions.
    
    Args:
        grid: The letter grid
        path: List of positions
        
    Returns:
        True if positions are valid
    """
    # Check path validity
    if not is_valid_path(grid, path):
        return False
    
    # Check for repeated positions
    if has_repeated_positions(list(path)):
        return False
    
    return True


def validate_play(
    grid: Grid,
    path: Path,
    theme_words: set[str],
    found_words: set[str]
) -> WordResult | None:
    """
    Validate a player's play.
    
    Args:
        grid: The letter grid
        path: Path of positions forming the word
        theme_words: Set of theme words to find
        found_words: Set of already found words
        
    Returns:
        WordResult if valid, None otherwise
    """
    # Validate path
    if not validate_positions(grid, path):
        return None
    
    # Extract word from path
    word = "".join(grid[r][c] for r, c in path)
    
    # Normalize word
    word = word.upper()
    
    # Check word length
    if len(word) < GAME_CONFIG.MIN_WORD_LENGTH:
        return None
    
    # Check if word was already found
    if word in found_words:
        return None
    
    # Check if word is in theme words
    is_theme = word in theme_words
    
    # Check if it's a spangram (if word length >= 6 and touches sides)
    is_spangram = _check_is_spangram(grid, path) if len(word) >= 6 else False
    
    # Validate word against dictionary (if available)
    if not is_theme:
        # Allow non-theme words but mark as bonus
        pass
    
    return WordResult(
        word=word,
        path=path,
        is_theme=is_theme,
        is_spangram=is_spangram,
        score=0  # Will be calculated by scorer
    )


def _check_is_spangram(grid: Grid, path: Path) -> bool:
    """
    Check if a word is a spangram (touches two opposite sides).
    
    Args:
        grid: The letter grid
        path: Path of positions
        
    Returns:
        True if word is a spangram
    """
    if len(path) < 6:
        return False
    
    rows = set(r for r, c in path)
    cols = set(c for r, c in path)
    
    # Check if touches top and bottom
    if 0 in rows and GAME_CONFIG.GRID_ROWS - 1 in rows:
        return True
    
    # Check if touches left and right
    if 0 in cols and GAME_CONFIG.GRID_COLS - 1 in cols:
        return True
    
    return False


def check_completion(board: BoardState, theme_words: set[str]) -> bool:
    """
    Check if the game is complete.
    
    Args:
        board: Current board state
        theme_words: Set of theme words
        
    Returns:
        True if all theme words are found
    """
    found_theme_words = {
        w.word for w in board.found_words 
        if w.is_theme and w.word in theme_words
    }
    
    return found_theme_words == theme_words


def validate_word_in_dictionary(word: str) -> bool:
    """
    Validate a word against the dictionary.
    
    Args:
        word: Word to validate
        
    Returns:
        True if word is valid
    """
    from src.providers.dictionary import is_valid_word
    return is_valid_word(word)


__all__ = [
    "validate_positions",
    "validate_play",
    "_check_is_spangram",
    "check_completion",
    "validate_word_in_dictionary",
]
