"""Scoring and hint service."""

from __future__ import annotations

from src.types.board import BoardState
from src.types.game import WordResult
from src.types.hint import Hint, HintType
from src.config.game import GAME_CONFIG


def calculate_score(word_result: WordResult) -> int:
    """
    Calculate points for a found word.
    
    Args:
        word_result: The word result to score
        
    Returns:
        Number of points earned
    """
    if not word_result.is_theme:
        return 0
    
    # Base points: 1 per letter
    base = len(word_result.word) * GAME_CONFIG.POINTS_PER_LETTER
    
    # Spangram bonus
    if word_result.is_spangram:
        base += GAME_CONFIG.SPANGRAM_BONUS
    
    return base


def track_hints(
    found_words: set[str],
    theme_words: set[str],
    hints_unlocked: int
) -> tuple[list[Hint], int]:
    """
    Track hint progress based on non-theme words found.
    
    Args:
        found_words: All words found so far
        theme_words: Set of theme words
        hints_unlocked: Number of hints already unlocked
        
    Returns:
        Tuple of (new hints to unlock, updated hints_unlocked count)
    """
    non_theme_count = len(found_words) - len(theme_words)
    hints_to_unlock = max(0, non_theme_count // GAME_CONFIG.NON_THEME_HINT_COST - hints_unlocked)
    
    new_hints = []
    for i in range(hints_unlocked, hints_unlocked + hints_to_unlock):
        hint = Hint(
            hint_type=HintType.THEME,
            description=f"Hint {i + 1}: One of the theme words starts with...",
            cost=GAME_CONFIG.NON_THEME_HINT_COST
        )
        new_hints.append(hint)
    
    return new_hints, hints_unlocked + hints_to_unlock


def get_hint(
    board: BoardState,
    theme_words: set[str],
    hints_used: int,
    max_hints: int = GAME_CONFIG.MAX_HINTS
) -> str | None:
    """
    Generate a hint based on theme words not yet found.
    
    Args:
        board: Current board state
        theme_words: Set of all theme words
        hints_used: Number of hints already used
        max_hints: Maximum hints allowed
        
    Returns:
        Hint text or None if no hints available
    """
    found_theme = {w.word for w in board.found_words if w.is_theme}
    remaining = theme_words - found_theme
    
    if not remaining:
        return None
    
    if hints_used >= max_hints:
        return None
    
    # Return first remaining theme word length as hint
    word = next(iter(remaining))
    return f"Theme word length: {len(word)} letters"
