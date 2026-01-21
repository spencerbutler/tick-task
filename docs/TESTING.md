# Testing strategy (v0)

## Required suites
- Unit: model, validation, query, serialization
- Integration: persistence + API
- Contract: API schema/behavior
- UI: minimal smoke tests only (justify tooling)

## Quality gates
- Pre-commit runs: formatting/lint/typecheck (if applicable) + fast unit subset
- CI runs: full suite on PR

## Test principles
- Deterministic
- Fast
- Minimal external dependencies
