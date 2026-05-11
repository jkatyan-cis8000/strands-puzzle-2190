# ARCHITECTURE.md

Written by team-lead before spawning teammates. This is the shared blueprint —
teammates read it to understand what they are building and how their module fits.
Update it when the structure changes; do not let it drift from the actual code.

## Module Structure

- src/types/__init__.py: Type definitions for the Strands game
- src/types/grid.py: Grid and LetterGrid types
- src/types/board.py: BoardState type
- src/types/game.py: GameState, WordResult, PlayResult types
- src/types/hint.py: Hint system types

- src/config/__init__.py: Configuration constants
- src/config/game.py: Game settings (grid size, word length rules, hint frequency)

- src/utils/__init__.py: Utility functions
- src/utils/grid.py: Grid coordinate operations, path finding
- src/utils/word.py: Word validation, scoring, anagram helpers

- src/providers/__init__.py: Provider module exports
- src/providers/dictionary.py: Dictionary loading and word validation

- src/service/__init__.py: Service module exports
- src/service/generator.py: Board generation, word placement
- src/service/scorer.py: Score calculation, hint tracking
- src/service/validator.py: Move validation, word discovery

- src/runtime/__init__.py: Runtime module exports
- src/runtime/game_engine.py: Core game loop, state management

- src/ui/__init__.py: UI module exports
- src/ui/cli.py: Command-line interface, rendering, input handling

- src/__main__.py: Entry point, wires everything together

## Interfaces

### Types (src/types/)
- `Grid`: 6x8 grid represented as list of lists
- `LetterGrid`: Grid[str] - actual letter grid
- `BoardState`: Dataclass with grid, found_words, score, hints_found
- `WordResult`: Dataclass with word, positions, is_spangram, is_theme
- `PlayResult`: Dataclass with words_found, score_delta, hints_unlocked
- `Hint`: Dataclass with type, description, cost

### Providers (src/providers/)
- `load_dictionary() -> set[str]`: Load valid words from file
- `is_valid_word(word: str) -> bool`: Check if word exists in dictionary

### Service (src/service/)
- `generate_board(theme_words: list[str], spangram: str) -> BoardState`: Create puzzle board
- `validate_play(grid: Grid[str], positions: list[tuple[int,int]]) -> WordResult`: Validate a play
- `check_completion(board: BoardState, theme_words: set[str]) -> bool`: Check if puzzle is solved

### UI (src/ui/)
- `render_board(board: BoardState) -> str`: Render board to terminal
- `parse_input(input_str: str) -> list[tuple[int,int]]`: Parse user input to positions
- `main() -> None`: CLI entry point

### Runtime (src/runtime/)
- `GameEngine`: Class managing game state and interactions
- `GameEngine.play_word(positions: list[tuple[int,int]]) -> PlayResult`: Process a play
- `GameEngine.get_hint() -> Hint`: Get a hint (costs 3 non-theme words)

## Shared Data Structures

```python
# Grid type
Grid = list[list[str]]  # 6 rows x 8 columns

# Position in grid
Position = tuple[int, int]  # (row, col)

# Path through grid
Path = list[Position]

# Found word result
@dataclass
class WordResult:
    word: str
    positions: Path
    is_spangram: bool
    is_theme: bool
    points: int

# Board state
@dataclass
class BoardState:
    grid: LetterGrid
    found_words: list[WordResult]
    score: int
    hints_found: int  # Non-theme words found

# Game state
@dataclass
class GameState:
    board: BoardState
    theme_words: set[str]
    spangram: str
    all_words: set[str]
    game_over: bool
```

## External Dependencies

- Python 3.11+ standard library only (no external dependencies)
- Uses: `dataclasses`, `typing`, `collections`, `random`, `json`
