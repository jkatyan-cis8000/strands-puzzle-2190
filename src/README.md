"""Layer structure and dependency rules.

This module defines the layered architecture of the Strands puzzle game.

## Layers

The codebase follows a layered architecture with strict dependency direction:

1. **types** - Core type definitions (dataclasses, type aliases)
   - No dependencies on other layers
   - Defines shared interfaces and data structures

2. **config** - Configuration constants
   - Dependencies: types
   - Game settings, grid dimensions, scoring rules

3. **utils** - Utility functions
   - Dependencies: types, config
   - Grid operations, word validation helpers

4. **providers** - External data sources
   - Dependencies: types, utils
   - Dictionary loading, word validation

5. **service** - Business logic
   - Dependencies: types, config, utils, providers
   - Board generation, scoring, validation

6. **runtime** - Game engine and state management
   - Dependencies: types, config, service
   - Game loop, state transitions

7. **ui** - User interface
   - Dependencies: types, config, runtime
   - CLI, web interface implementations

## Import Rules

Each layer can only import from layers below it:

- types:    no internal imports (only from typing, dataclasses)
- config:   src.types
- utils:    src.types, src.config
- providers: src.types, src.utils
- service:  src.types, src.config, src.utils, src.providers
- runtime:  src.types, src.config, src.service
- ui:       src.types, src.config, src.runtime

## Layout

```
src/
├── __init__.py       # Package version
├── __main__.py       # Entry point
├── config/           # Configuration layer
│   ├── __init__.py
│   └── game.py
├── types/            # Types layer
│   ├── __init__.py
│   ├── board.py
│   ├── game.py
│   ├── grid.py
│   └── hint.py
├── utils/            # Utils layer
│   ├── __init__.py
│   ├── grid.py
│   └── word.py
├── providers/        # Providers layer
│   ├── __init__.py
│   └── dictionary.py
├── service/          # Service layer
│   ├── __init__.py
│   ├── generator.py
│   ├── scorer.py
│   └── validator.py
├── runtime/          # Runtime layer
│   ├── __init__.py
│   └── game_engine.py
└── ui/               # UI layer
    ├── __init__.py
    └── cli.py
```

"""

from __future__ import annotations
