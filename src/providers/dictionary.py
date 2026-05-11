"""Dictionary provider for word validation."""

from __future__ import annotations

from pathlib import Path


def load_dictionary() -> set[str]:
    """
    Load the default dictionary of valid words.
    
    Returns:
        Set of valid uppercase words
    """
    # For now, return a minimal set of common words
    # In production, this would load from a dictionary file
    common_words = {
        "THE", "AND", "FOR", "ARE", "BUT", "NOT", "YOU", "ALL", "ANY",
        "CAN", "HAD", "HER", "WAS", "ONE", "OUR", "OUT", "DAY", "GET",
        "HAS", "HIM", "HIS", "HOW", "MAN", "NEW", "NOW", "OLD", "SEE",
        "TWO", "WAY", "WHO", "BOY", "DID", "ITS", "LET", "PUT", "SAY",
        "SHE", "TOO", "USE", "DAD", "MOM", "CAT", "DOG", "BAT", "HAT",
        "SUN", "FUN", "RUN", "BOX", "HOT", "MOM", "DAD", "EYE", "RED",
        "FOX", "JET", "KEY", "MAP", "NUT", "OAT", "PEN", "PIG", "RAT",
        "ROW", "SIT", "TOP", "VAR", "WEB", "ZIP", "APPLE", "BREAD",
        "CHAIR", "DOOR", "EARTH", "FIELD", "GRASS", "HOUSE", "INDEX",
        "JUDGE", "KNIFE", "LUNCH", "MONEY", "NOISE", "OCEAN", "PIZZA",
        "QUICK", "RIVER", "SNAKE", "TIGER", "UNION", "VOICE", "WATER",
        "XENON", "YACHT", "ZEBRA", "PUZZLE", "STRANDS", "GAME", "WORD",
        "LEARN", "PLAY", "FIND", "SEARCH", "CLIMB", "DANCE", "SING",
        "WRITE", "DRIVE", "SLEEP", "EAT", "DRINK", "SWIM", "FLY",
        "WALK", "RUN", "JUMP", "PLAY", "READ", "WATCH", "LISTEN",
        "TALK", "SPEND", "START", "STOP", "OPEN", "CLOSE", "TURN",
        "MAKE", "TAKE", "COME", "GO", "SEEK", "LOOK", "FIND", "LEARN",
    }
    return common_words


# Global dictionary instance
_DICTIONARY: set[str] | None = None


def get_dictionary() -> set[str]:
    """
    Get the dictionary, loading it once.
    
    Returns:
        Set of valid uppercase words
    """
    global _DICTIONARY
    if _DICTIONARY is None:
        _DICTIONARY = load_dictionary()
    return _DICTIONARY


def is_valid_word(word: str) -> bool:
    """
    Check if a word is in the dictionary.
    
    Args:
        word: Word to check (case-insensitive)
        
    Returns:
        True if word is valid
    """
    dictionary = get_dictionary()
    return word.upper() in dictionary


def load_dictionary_from_file(filepath: Path) -> set[str]:
    """
    Load dictionary from a file (one word per line).
    
    Args:
        filepath: Path to dictionary file
        
    Returns:
        Set of uppercase words
    """
    words: set[str] = set()
    
    if filepath.exists():
        with open(filepath, "r") as f:
            for line in f:
                word = line.strip().upper()
                if word:
                    words.add(word)
    
    return words


__all__ = [
    "load_dictionary",
    "get_dictionary",
    "is_valid_word",
    "load_dictionary_from_file",
]
