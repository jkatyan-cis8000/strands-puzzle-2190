"""Providers module exports."""

from __future__ import annotations

from src.providers.dictionary import (
    load_dictionary,
    get_dictionary,
    is_valid_word,
    load_dictionary_from_file,
)

__all__ = [
    "load_dictionary",
    "get_dictionary",
    "is_valid_word",
    "load_dictionary_from_file",
]
