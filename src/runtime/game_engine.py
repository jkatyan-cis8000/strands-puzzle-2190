"""Game engine implementation."""

from __future__ import annotations

from src.types.board import BoardState
from src.types.game import GameState
from src.types.grid import LetterGrid, Path
from src.config.game import GAME_CONFIG
from src.providers.dictionary import get_dictionary
from src.service.generator import generate_board
from src.service.validator import validate_play, check_completion


class GameEngine:
    """Manages the core game state and operations."""
    
    def __init__(
        self,
        theme_words: list[str],
        spangram: str | None = None,
        seed: int | None = None
    ):
        """
        Initialize the game engine.
        
        Args:
            theme_words: List of theme words
            spangram: Optional spangram (touches two opposite sides)
            seed: Optional random seed for reproducibility
        """
        self.theme_words = {w.upper() for w in theme_words}
        self.spangram = spangram.upper() if spangram else None
        self.seed = seed
        
        # Generate initial board
        board = generate_board(
            list(self.theme_words),
            self.spangram,
            self.seed
        )
        
        # Build all words from dictionary
        self.all_words = get_dictionary()
        
        # Initialize game state
        self.state = GameState(
            board=board,
            theme_words=self.theme_words,
            spangram=self.spangram or "",
            all_words=self.all_words,
            game_over=False
        )
        
        # Track found words for hint calculation
        self.found_words: set[str] = set()
        self.hints_unlocked = 0
        
        # Calculate initial hint progress
        self._update_hint_progress()
    
    def play(self, positions: Path) -> tuple[bool, str]:
        """
        Process a player's play.
        
        Args:
            positions: Path of positions representing the word
            
        Returns:
            Tuple of (success, message)
        """
        if self.state.game_over:
            return False, "Game is already over"
        
        # Validate the play
        result = validate_play(
            self.state.board.grid,
            positions,
            self.theme_words,
            self.found_words
        )
        
        if result is None:
            return False, "Invalid play"
        
        # Update board state
        self.state.board.found_words.append(result)
        self.found_words.add(result.word)
        
        # Update score
        score_delta = calculate_score(result)
        self.state.board.score += score_delta
        
        # Update hint progress
        self._update_hint_progress()
        
        # Check if game is complete
        if check_completion(self.state.board, self.theme_words):
            self.state.game_over = True
            return True, f"Level complete! Final score: {self.state.board.score}"
        
        return True, f"Found '{result.word}'! Points: {score_delta}"
    
    def _update_hint_progress(self) -> None:
        """Update hint progress based on found words."""
        from src.service.scorer import track_hints
        new_hints, self.hints_unlocked = track_hints(
            self.found_words,
            self.theme_words,
            self.hints_unlocked
        )
    
    def get_hint(self) -> str | None:
        """Get a hint if available."""
        from src.service.scorer import get_hint
        return get_hint(
            self.state.board,
            self.theme_words,
            self.hints_unlocked
        )


def calculate_score(result: WordResult) -> int:
    """Calculate score for a word result."""
    if not result.is_theme:
        return 0
    
    base = len(result.word) * GAME_CONFIG.POINTS_PER_LETTER
    
    if result.is_spangram:
        base += GAME_CONFIG.SPANGRAM_BONUS
    
    return base


def initialize_game(
    theme_words: list[str],
    spangram: str | None = None,
    seed: int | None = None
) -> tuple[GameState, GameEngine]:
    """
    Initialize a new game and return the game state and engine.
    
    Args:
        theme_words: List of theme words
        spangram: Optional spangram
        seed: Optional random seed
        
    Returns:
        Tuple of (game_state, game_engine)
    """
    engine = GameEngine(theme_words, spangram, seed)
    return engine.state, engine
