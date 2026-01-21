# Agent Prompt 12 — Implementation Requirements

## User-Specified Requirements
- **Persistence**: SQLite (local-first, crash-safe, no external dependencies)
- **UI Framework**: No preference - agent to choose based on beauty, responsiveness, accessibility
- **Authentication**: OAuth with Google support if feasible within constraints, otherwise single-user with admin powers
- **Local-First Priority**: Default localhost-only, optional LAN mode with token auth

## Constraints
- All phases require separate feature branches with PRs
- All tests must pass before merge to main
- Every commit includes model disclosure: [model: Cline]
- Maintain spec-first discipline: planning/documentation before code
- Minimize third-party dependencies with clear value justification

## Success Criteria
- Beautiful, responsive UI suitable for daily task management
- Crash-safe local persistence with human-readable exports
- Stable local API for FIN ecosystem interoperation
- Comprehensive test coverage (unit, integration, E2E)
- Secure authentication with OAuth preferred, admin fallback

## Agent Decision Space
- UI framework selection (React/TypeScript recommended for accessibility + beauty)
- OAuth implementation approach (Authlib vs native, Google OAuth feasibility)
- Testing framework choices (pytest + Playwright baseline)
- Build/deployment tooling (Vite, setuptools, GitHub Actions)

## Output
- Document technology choices in docs/DECISIONS.md
- Update relevant docs with implementation details
- Ensure all requirements traceable to SPEC.md acceptance criteria
