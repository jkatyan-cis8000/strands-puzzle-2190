"""Grid operations utilities."""

from __future__ import annotations

from src.types.grid import Grid, Path, Position
from src.config.game import GAME_CONFIG


def get_adjacent_positions(
    grid: Grid,
    position: Position,
    visited: set[Position] | None = None
) -> list[Position]:
    """
    Get valid adjacent positions for a given position.
    
    Args:
        grid: The letter grid
        position: Current (row, col) position
        visited: Set of already visited positions
        
    Returns:
        List of valid adjacent positions
    """
    if visited is None:
        visited = set()
    
    row, col = position
    adjacent = []
    
    # Check all 8 directions
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            
            new_row, new_col = row + dr, col + dc
            
            if (0 <= new_row < GAME_CONFIG.GRID_ROWS and 
                0 <= new_col < GAME_CONFIG.GRID_COLS):
                if (new_row, new_col) not in visited:
                    adjacent.append((new_row, new_col))
    
    return adjacent


def is_valid_path(grid: Grid, path: Path) -> bool:
    """
    Validate a path is contiguous and has valid positions.
    
    Args:
        grid: The letter grid
        path: List of positions
        
    Returns:
        True if path is valid
    """
    if not path:
        return False
    
    # Check all positions are within grid bounds
    for row, col in path:
        if not (0 <= row < GAME_CONFIG.GRID_ROWS and 
                0 <= col < GAME_CONFIG.GRID_COLS):
            return False
    
    # Check path length
    if len(path) < GAME_CONFIG.MIN_WORD_LENGTH:
        return False
    
    if len(path) > GAME_CONFIG.MAX_WORD_LENGTH:
        return False
    
    # Check path is contiguous
    for i in range(1, len(path)):
        prev_row, prev_col = path[i - 1]
        curr_row, curr_col = path[i]
        
        # Check if adjacent (including diagonals)
        row_diff = abs(curr_row - prev_row)
        col_diff = abs(curr_col - prev_col)
        
        if row_diff > 1 or col_diff > 1:
            return False
    
    return True


def find_paths_for_word(grid: Grid, word: str) -> list[Path]:
    """
    Find all possible paths that spell the given word.
    
    Args:
        grid: The letter grid
        word: Word to find (uppercase)
        
    Returns:
        List of valid paths
    """
    paths: list[Path] = []
    
    # Find all starting positions
    start_positions = []
    for row in range(GAME_CONFIG.GRID_ROWS):
        for col in range(GAME_CONFIG.GRID_COLS):
            if grid[row][col] == word[0]:
                start_positions.append((row, col))
    
    # DFS to find all paths
    for start in start_positions:
        _dfs_find_paths(grid, word, [start], set([start]), paths)
    
    return paths


def _dfs_find_paths(
    grid: Grid,
    word: str,
    current_path: Path,
    visited: set[Position],
    all_paths: list[Path]
) -> None:
    """DFS helper to find paths for a word."""
    if len(current_path) > GAME_CONFIG.MAX_WORD_LENGTH:
        return
    
    if len(current_path) == len(word):
        # Check if path spells the word
        path_word = "".join(grid[r][c] for r, c in current_path)
        if path_word == word:
            all_paths.append(current_path[:])
        return
    
    # Get last position
    row, col = current_path[-1]
    
    # Try all adjacent positions
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            
            new_row, new_col = row + dr, col + dc
            
            if (0 <= new_row < GAME_CONFIG.GRID_ROWS and 
                0 <= new_col < GAME_CONFIG.GRID_COLS and
                (new_row, new_col) not in visited):
                
                # Check if this position matches the next letter
                if grid[new_row][new_col] == word[len(current_path)]:
                    visited.add((new_row, new_col))
                    current_path.append((new_row, new_col))
                    
                    _dfs_find_paths(grid, word, current_path, visited, all_paths)
                    
                    current_path.pop()
                    visited.remove((new_row, new_col))


def positions_to_path(positions: list[tuple[int, int]]) -> Path:
    """
    Convert a list of (row, col) tuples to a Path.
    
    Args:
        positions: List of position tuples
        
    Returns:
        Path (list of Position tuples)
    """
    return [(row, col) for row, col in positions]


__all__ = [
    "get_adjacent_positions",
    "is_valid_path",
    "find_paths_for_word",
    "positions_to_path",
]
