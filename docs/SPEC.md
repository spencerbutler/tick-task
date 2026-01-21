# SPEC (v0)

## Product statement
A local-first task tracking app supporting personal and professional workstreams with a stable local API for interoperation with other local apps.

## Goals (v0)
- Beautiful, responsive UI suitable for daily use.
- Durable local persistence.
- Local API for CRUD + query.
- Export JSON required; CSV strongly preferred.
- Comprehensive tests and pre-commit/CI gates.

## Non-goals (v0)
- Multi-user access control
- Cloud sync
- Mobile app
- Complex recurrence rules
- Full-text search beyond minimal substring matching (unless trivial)

## Functional requirements
### Task entity
- id (stable)
- title (required)
- description (optional)
- status: todo|doing|blocked|done|archived
- priority: define scheme in docs/DATA_MODEL.md
- due_at (optional)
- tags (0..n)
- context: personal|professional|mixed (+ optional workspace)
- created_at, updated_at, completed_at
- estimate (optional; define scheme)

### Operations
- Create/update/complete/reopen/archive (prefer soft-delete semantics)
- Filtering and sorting (status/context/tags/due/priority/updated)
- Views: Today, Inbox, By Context, By Tag

## Interop API requirements
- Local-only by default (127.0.0.1)
- Optional LAN bind behind explicit config
- If LAN bind enabled, require token header

## Data requirements
- Crash-safe persistence
- Human-readable export
