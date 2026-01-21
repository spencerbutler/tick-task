# Architecture (v0)

## Principles
- Local-first, offline-capable.
- Minimal third-party dependencies.
- Clear separation: domain model, persistence, API, UI.

## Proposed components
- Domain: task model + validation + query language
- Persistence: durable store (decision to be recorded in docs/DECISIONS.md)
- API: local HTTP API, versioned (v0)
- UI: responsive web UI

## Observability (local)
- Structured logs (v1)
- Basic health endpoint (v0 preferred)

## Threat model (summary)
- Default: localhost-only, no auth
- Optional LAN mode: token required
