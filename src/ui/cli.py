"""CLI UI implementation."""

from __future__ import annotations

import sys
from typing import cast

from src.types.board import BoardState
from src.types.game import GameState
from src.types.grid import Path, Position
from src.config.game import GAME_CONFIG
from src.runtime.game_engine import initialize_game, GameEngine


class StrandsCLI:
    """Command-line interface for the Strands puzzle game."""
    
    def __init__(self, theme_words: list[str], spangram: str | None = None):
        """
        Initialize the CLI.
        
        Args:
            theme_words: List of theme words for the puzzle
            spangram: Optional spangram
        """
        self.engine: GameEngine | None = None
        self.theme_words = theme_words
        self.spangram = spangram
        
        # Initialize game
        self._init_game()
    
    def _init_game(self) -> None:
        """Initialize the game engine."""
        _, self.engine = initialize_game(
            self.theme_words,
            self.spangram
        )
        assert self.engine is not None
    
    def run(self) -> None:
        """Run the main game loop."""
        print("\n" + "=" * 40)
        print("       🌐 STRANDS PUZZLE 🌐")
        print("=" * 40)
        
        while not self.engine.state.game_over:
            self._display_board()
            self._display_score()
            
            # Get player input
            command = input("\n> ").strip().lower()
            
            if command in ("quit", "q", "exit"):
                print("Thanks for playing!")
                return
            
            if command in ("hint", "h"):
                self._handle_hint()
                continue
            
            if command == "help":
                self._show_help()
                continue
            
            # Parse positions (e.g., "0,0 0,1 0,2 0,3")
            positions = self._parse_positions(command)
            
            if positions is None:
                print("Invalid input. Use 'help' for instructions.")
                continue
            
            # Process the play
            success, message = self.engine.play(positions)
            print(message)
        
        print("\n🎉 PUZZLE COMPLETED! 🎉")
        print(f"Final Score: {self.engine.state.board.score}")
    
    def _display_board(self) -> None:
        """Display the current board state."""
        grid = self.engine.state.board.grid
        rows, cols = len(grid), len(grid[0])
        
        # Print column numbers
        print("\n   " + " ".join(f"{c}" for c in range(cols)))
        
        # Print rows with row numbers
        for r in range(rows):
            row_letters = [grid[r][c] if grid[r][c] else "_" for c in range(cols)]
            print(f"{r}: " + " ".join(row_letters))
    
    def _display_score(self) -> None:
        """Display current score and progress."""
        score = self.engine.state.board.score
        found_words = self.engine.state.board.found_words
        found_count = len([w for w in found_words if w.is_theme])
        total_theme = len(self.engine.state.theme_words)
        
        print(f"\nScore: {score} | Found: {found_count}/{total_theme} theme words")
        print(f"Hints available: {self.engine.hints_unlocked}")
    
    def _parse_positions(self, input_str: str) -> Path | None:
        """
        Parse positions string into a path.
        
        Args:
            input_str: String like "0,0 0,1 0,2 0,3"
            
        Returns:
            Path or None if invalid
        """
        parts = input_str.strip().split()
        positions: Path = []
        
        for part in parts:
            try:
                r_str, c_str = part.split(",")
                row, col = int(r_str), int(c_str)
                
                if not (0 <= row < GAME_CONFIG.GRID_ROWS and 
                        0 <= col < GAME_CONFIG.GRID_COLS):
                    return None
                
                positions.append((row, col))
            except ValueError:
                return None
        
        return positions if len(positions) >= GAME_CONFIG.MIN_WORD_LENGTH else None
    
    def _handle_hint(self) -> None:
        """Handle hint request."""
        hint = self.engine.get_hint()
        if hint:
            print(f"💡 Hint: {hint}")
        else:
            print("No hints available. Find more non-theme words!")
    
    def _show_help(self) -> None:
        """Show help information."""
        print("\n=== COMMANDS ===")
        print("Enter positions as 'row,col' separated by spaces:")
        print("  e.g., '0,0 0,1 0,2 0,3' to spell a word")
        print("\nCommands:")
        print("  hint, h  - Get a hint")
        print("  help     - Show this help")
        print("  quit, q  - Quit the game")
        print("  exit     - Exit the game")
        print("\n=== GOAL ===")
        print(f"Find all theme words (min {GAME_CONFIG.MIN_WORD_LENGTH} letters).")
        print("A spangram touches two opposite sides of the board.")


def main() -> int:
    """Main entry point for CLI."""
    # Default puzzle words
    theme_words = ["CAT", "DOG", "BAT", "HAT", "SUN", "FUN", "RUN", "BOX"]
    spangram = "PUZZLE"
    
    cli = StrandsCLI(theme_words, spangram)
    cli.run()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
