# Local API (v0)

## Conventions
- Base URL: http://127.0.0.1:<port>/api/v0
- JSON request/response
- Explicit versioning in path
- Errors: consistent JSON envelope

## Endpoints (proposed)
- GET /health
- POST /tasks
- GET /tasks
- GET /tasks/{id}
- PATCH /tasks/{id}
- POST /tasks/{id}/complete
- POST /tasks/{id}/reopen
- POST /export (or GET /export)
- POST /import (v0 optional)

## Query parameters (GET /tasks)
- status, context, tag, due_before, due_after
- sort: due_at|priority|updated_at
- order: asc|desc
- limit, offset
- updated_since (for polling/eventing v0)

## Auth (LAN mode only)
- Header: Authorization: Bearer <token>
