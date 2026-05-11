"""Word utilities."""

from __future__ import annotations

from src.config.game import GAME_CONFIG


def sort_word_by_length(words: list[str]) -> list[str]:
    """
    Sort words by length (longest first).
    
    Args:
        words: List of words
        
    Returns:
        Sorted list of words
    """
    return sorted(words, key=len, reverse=True)


def get_word_signature(word: str) -> str:
    """
    Get alphabetical signature of a word.
    
    Args:
        word: Input word
        
    Returns:
        Alphabetically sorted letters as string
    """
    return "".join(sorted(word.upper()))


def are_anagrams(word1: str, word2: str) -> bool:
    """
    Check if two words are anagrams.
    
    Args:
        word1: First word
        word2: Second word
        
    Returns:
        True if words are anagrams
    """
    return get_word_signature(word1) == get_word_signature(word2)


def normalize_word(word: str) -> str:
    """
    Normalize a word to uppercase.
    
    Args:
        word: Input word
        
    Returns:
        Normalized word (uppercase)
    """
    return word.upper()


def is_valid_word_length(word: str) -> bool:
    """
    Check if word length is within valid range.
    
    Args:
        word: Input word
        
    Returns:
        True if word length is valid
    """
    length = len(word)
    return (GAME_CONFIG.MIN_WORD_LENGTH <= length <= 
            GAME_CONFIG.MAX_WORD_LENGTH)


def has_repeated_positions(path: list[tuple[int, int]]) -> bool:
    """
    Check if path visits same position twice.
    
    Args:
        path: List of positions
        
    Returns:
        True if path has duplicate positions
    """
    return len(path) != len(set(path))


__all__ = [
    "sort_word_by_length",
    "get_word_signature",
    "are_anagrams",
    "normalize_word",
    "is_valid_word_length",
    "has_repeated_positions",
]
