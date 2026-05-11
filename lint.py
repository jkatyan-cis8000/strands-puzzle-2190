"""Linting tool for Strands puzzle game.

Verifies layer architecture compliance and code quality.
"""

from __future__ import annotations

import ast
import os
import sys
from pathlib import Path


# Layer definitions (order matters for dependencies)
LAYERS = [
    "types",
    "config",
    "utils",
    "providers",
    "service",
    "runtime",
    "ui",
]

# Allowed imports per layer
ALLOWED_IMPORTS: dict[str, list[str]] = {
    "types": [],
    "config": ["types"],
    "utils": ["types", "config"],
    "providers": ["types", "utils"],
    "service": ["types", "config", "utils", "providers"],
    "runtime": ["types", "config", "service"],
    "ui": ["types", "config", "runtime"],
}


class Linter:
    """Linter for the Strands puzzle game."""
    
    def __init__(self, root: Path):
        """Initialize the linter."""
        self.root = root
        self.violations: list[str] = []
    
    def run(self) -> bool:
        """Run all lint checks. Returns True if clean."""
        self._check_layers_exist()
        self._check_file_structure()
        self._check_imports()
        self._check_line_counts()
        return len(self.violations) == 0
    
    def _check_layers_exist(self) -> None:
        """Verify all layer directories exist."""
        for layer in LAYERS:
            layer_path = self.root / "src" / layer
            if not layer_path.exists():
                self.violations.append(
                    f"Missing layer directory: src/{layer}/"
                )
    
    def _check_file_structure(self) -> None:
        """Check that source files are in correct layer directories."""
        for py_file in self.root.rglob("*.py"):
            if py_file.name in ("__init__.py", "__main__.py", "lint.py"):
                continue
            
            rel_path = py_file.relative_to(self.root)
            parts = list(rel_path.parts)
            
            # Skip tests directory
            if "tests" in parts:
                continue
            
            # Check file is inside src/
            if parts[0] != "src":
                continue
            
            # Extract the layer from path
            if len(parts) < 2:
                continue
            
            # Get the layer directory (second part after src/)
            potential_layer = parts[1]
            if potential_layer in LAYERS:
                # Verify file is in that layer's directory
                layer_path = self.root / "src" / potential_layer
                if not py_file.relative_to(layer_path).parts:
                    # File is directly in the layer directory, that's OK
                    continue
            else:
                # File is in src/ but not in a layer directory
                self.violations.append(
                    f"{py_file}: File '{py_file.name}' is in src/ but not in "
                    f"any layer directory. Move to appropriate layer folder."
                )
    
    def _check_imports(self) -> None:
        """Verify imports respect layer dependencies."""
        for py_file in self.root.rglob("*.py"):
            if py_file.name == "lint.py":
                continue
            
            rel_path = py_file.relative_to(self.root)
            parts = list(rel_path.parts)
            
            # Skip tests
            if "tests" in parts:
                continue
            
            # Get the layer of this file
            if len(parts) < 2 or parts[0] != "src":
                continue
            
            if len(parts) < 3:
                continue
            
            layer = parts[1]
            if layer not in ALLOWED_IMPORTS:
                continue
            
            allowed = ALLOWED_IMPORTS[layer]
            
            # Parse the file
            try:
                with open(py_file, "r") as f:
                    tree = ast.parse(f.read(), filename=str(py_file))
            except SyntaxError:
                continue
            
            # Check imports
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.module is None:
                        continue
                    
                    # Check relative imports
                    if node.level > 0:
                        # Relative import like "from . import X"
                        # or "from .module import X"
                        if node.module:
                            # This is a relative import to another module
                            # Get the target module's layer
                            target_parts = node.module.split(".")
                            # For relative imports, check if it's going down
                            # the layer hierarchy
                            if len(target_parts) > 0:
                                potential_layer = target_parts[0]
                                if potential_layer in LAYERS:
                                    if potential_layer not in allowed:
                                        self.violations.append(
                                            f"{py_file}:{node.lineno}: "
                                            f"Import from '{node.module}' violates "
                                            f"layer dependencies. Layer '{layer}' "
                                            f"can only import from: {', '.join(allowed)}"
                                        )
                    else:
                        # Absolute import like "from src.config import X"
                        if node.module.startswith("src."):
                            # Extract the layer from the import
                            rest = node.module[4:]  # Remove "src."
                            if rest:
                                imported_layer = rest.split(".")[0]
                                if imported_layer in LAYERS:
                                    if imported_layer not in allowed:
                                        self.violations.append(
                                            f"{py_file}:{node.lineno}: "
                                            f"Import from '{node.module}' violates "
                                            f"layer dependencies. Layer '{layer}' "
                                            f"can only import from: {', '.join(allowed)}"
                                        )
    
    def _check_line_counts(self) -> None:
        """Verify no file exceeds MAX_LINES."""
        MAX_LINES = 300
        for py_file in self.root.rglob("*.py"):
            if py_file.name == "lint.py":
                continue
            
            rel_path = py_file.relative_to(self.root)
            parts = list(rel_path.parts)
            
            # Skip tests
            if "tests" in parts:
                continue
            
            try:
                with open(py_file, "r") as f:
                    lines = f.readlines()
                
                if len(lines) > MAX_LINES:
                    self.violations.append(
                        f"{py_file}: File has {len(lines)} lines (max {MAX_LINES})"
                    )
            except OSError:
                continue


def main() -> int:
    """Main entry point."""
    root = Path(__file__).parent
    
    linter = Linter(root)
    is_clean = linter.run()
    
    if is_clean:
        print("✅ All checks passed!")
        return 0
    
    print("❌ Linting failed:")
    for violation in linter.violations:
        print(f"  - {violation}")
    
    return 1


if __name__ == "__main__":
    sys.exit(main())
