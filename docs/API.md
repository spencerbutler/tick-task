# tick-task Local API (v1.0)

## Overview
The tick-task API provides a RESTful interface for task management operations. The API is designed for local-first usage with optional LAN access, supporting full CRUD operations, advanced querying, and data export functionality.

## Base URL and Versioning
- **Base URL**: `http://127.0.0.1:8000/api/v1` (default localhost)
- **LAN Mode**: `http://0.0.0.0:8000/api/v1` (when explicitly enabled)
- **Versioning**: Path-based versioning (`/api/v1/`) with backward compatibility
- **Content Type**: `application/json` for all requests and responses

## Authentication
- **Local Mode**: No authentication required (localhost trust)
- **LAN Mode**: Bearer token authentication required
  - Header: `Authorization: Bearer <token>`
  - Token obtained via settings/configuration
- **CORS**: Configured for localhost origins by default

## Error Handling
All errors return appropriate HTTP status codes with a consistent JSON error envelope:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Task title cannot be empty",
    "details": {
      "field": "title",
      "value": ""
    }
  }
}
```

### Error Codes
- `VALIDATION_ERROR` (400): Invalid request data
- `NOT_FOUND` (404): Resource not found
- `CONFLICT` (409): Resource state conflict
- `UNAUTHORIZED` (401): Authentication required but missing/invalid
- `FORBIDDEN` (403): Insufficient permissions
- `INTERNAL_ERROR` (500): Server error
- `SERVICE_UNAVAILABLE` (503): Service temporarily unavailable

## Data Types

### Task Object
```json
{
  "id": "uuid-v4-string",
  "title": "Complete project proposal",
  "description": "Write and review the Q1 project proposal document",
  "status": "todo",
  "priority": "high",
  "due_at": "2024-01-15T17:00:00Z",
  "tags": ["work", "urgent"],
  "context": "professional",
  "workspace": "Q1 Planning",
  "created_at": "2024-01-10T09:00:00Z",
  "updated_at": "2024-01-10T09:00:00Z",
  "completed_at": null
}
```

### Field Constraints
- `id`: UUID v4, auto-generated, immutable
- `title`: String, 1-200 characters, required, non-empty after trimming
- `description`: String, 0-2000 characters, optional, supports markdown
- `status`: Enum: `todo`, `doing`, `blocked`, `done`, `archived`
- `priority`: Enum: `low`, `medium`, `high`, `urgent`
- `due_at`: ISO 8601 datetime string, optional
- `tags`: Array of strings, 0-10 items, each 1-50 chars, normalized
- `context`: Enum: `personal`, `professional`, `mixed`
- `workspace`: String, 0-100 characters, optional
- `created_at`: ISO 8601 datetime, immutable, auto-set
- `updated_at`: ISO 8601 datetime, auto-updated
- `completed_at`: ISO 8601 datetime, set when status becomes `done`

## Endpoints

### Health Check
**GET /health**

Returns the health status of the API service.

**Response (200)**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected",
  "timestamp": "2024-01-10T09:00:00Z"
}
```

### Create Task
**POST /tasks**

Creates a new task with the provided data.

**Request Body**:
```json
{
  "title": "Complete project proposal",
  "description": "Write and review the Q1 project proposal document",
  "status": "todo",
  "priority": "high",
  "due_at": "2024-01-15T17:00:00Z",
  "tags": ["work", "urgent"],
  "context": "professional",
  "workspace": "Q1 Planning"
}
```

**Response (201)**: Complete task object with generated fields

**Error Responses**:
- `400`: Validation error with field details
- `500`: Server error

### Get Task
**GET /tasks/{id}**

Retrieves a specific task by ID.

**Parameters**:
- `id` (path): UUID v4 of the task

**Response (200)**: Complete task object

**Error Responses**:
- `404`: Task not found
- `400`: Invalid UUID format

### Update Task
**PUT /tasks/{id}**

Updates an existing task with the provided data. Only provided fields are updated.

**Parameters**:
- `id` (path): UUID v4 of the task

**Request Body**: Partial task object (same schema as create, all fields optional)

**Response (200)**: Complete updated task object

**Error Responses**:
- `404`: Task not found
- `409`: Cannot update archived task
- `400`: Validation error

### Delete Task (Soft Delete)
**DELETE /tasks/{id}**

Archives a task (soft delete). The task status is set to `archived`.

**Parameters**:
- `id` (path): UUID v4 of the task

**Response (200)**: Updated task object with `status: "archived"`

**Error Responses**:
- `404`: Task not found
- `409`: Task already archived

### List Tasks
**GET /tasks**

Retrieves a list of tasks with optional filtering, sorting, and pagination.

**Query Parameters**:

**Filtering**:
- `status` (string/array): Filter by status(es)
- `context` (string/array): Filter by context(s)
- `tags` (string): Tasks containing this tag (comma-separated for multiple)
- `priority` (string): Minimum priority level (`low`, `medium`, `high`, `urgent`)
- `due_before` (datetime): Tasks due before this date
- `due_after` (datetime): Tasks due after this date
- `updated_since` (datetime): Tasks updated since this time

**Sorting**:
- `sort` (string): Field to sort by (`created_at`, `updated_at`, `due_at`, `priority`, `title`)
- `order` (string): Sort order (`asc`, `desc`) - default: `desc`

**Pagination**:
- `limit` (integer): Maximum number of results (1-1000, default: 100)
- `cursor` (string): Cursor for pagination (from previous response)

**Response (200)**:
```json
{
  "tasks": [
    // Array of task objects
  ],
  "pagination": {
    "has_more": true,
    "next_cursor": "eyJpZCI6ImFiYzEyMyJ9",
    "total_count": 150
  }
}
```

### Export Tasks
**GET /export**

Exports all tasks in the requested format.

**Query Parameters**:
- `format` (string): Export format (`json` or `csv`, default: `json`)

**Response (200)**:
- **JSON Format**: JSON Lines (.jsonl) with one task per line
- **CSV Format**: CSV with headers and proper escaping

**Response Headers**:
- `Content-Type`: `application/jsonl` or `text/csv`
- `Content-Disposition`: `attachment; filename="fin-tasks-export-20240110.jsonl"`

**Error Responses**:
- `400`: Invalid format parameter
- `500`: Export generation failed

## Special Views

### Today View
**GET /tasks?status=todo,doing,blocked&due_before={tomorrow}&due_after={today}**

Returns tasks that should be worked on today.

### Inbox View
**GET /tasks?status=todo&due_at=null&sort=created_at&order=desc**

Returns pure inbox items (tasks without due dates).

### By Context View
**GET /tasks?status!=archived&sort=updated_at&order=desc**

Returns all active tasks grouped by context (client-side grouping).

### By Tag View
**GET /tasks?status!=archived&sort=updated_at&order=desc**

Returns all active tasks (client-side tag grouping).

## Polling and Synchronization (v1.0)
For v1.0, the API supports polling-based synchronization:

- Use `updated_since` parameter to get recently changed tasks
- Combine with appropriate filtering for efficient sync
- Client should poll every 30-60 seconds for real-time updates
- Future versions may add WebSocket support for push notifications

## Rate Limiting
- **Local Mode**: No rate limiting (localhost trust)
- **LAN Mode**: 1000 requests per hour per IP (configurable)
- Rate limit headers included in responses when approaching limits

## API Stability Guarantees
- **Backward Compatibility**: API v1 endpoints will remain compatible
- **Additive Changes**: New optional fields/parameters may be added
- **Deprecation Policy**: Breaking changes require new version
- **Documentation**: OpenAPI 3.0 spec available at `/docs`

## Testing the API
The API contract is designed to be testable with standard HTTP clients:

```bash
# Health check
curl http://127.0.0.1:8000/api/v1/health

# Create task
curl -X POST http://127.0.0.1:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "status": "todo"}'

# List tasks
curl "http://127.0.0.1:8000/api/v1/tasks?status=todo&limit=10"
```

## Implementation Plan

### Backend Architecture Implementation

**FastAPI Application Structure**:
- **Main Application**: `main.py` with FastAPI app instance and route inclusion
- **Route Modules**: Separate files for different endpoint groups (`tasks.py`, `health.py`)
- **Models**: Pydantic models for request/response validation
- **Dependencies**: Dependency injection for database sessions and authentication
- **Middleware**: CORS, error handling, request logging

**Database Layer Implementation**:
- **SQLAlchemy Models**: Declarative base classes mapping to SQLite tables
- **Session Management**: Async session context managers with proper cleanup
- **Migration System**: Alembic integration for schema versioning
- **Connection Pooling**: SQLAlchemy engine configuration for concurrent access

**Business Logic Implementation**:
- **Domain Services**: Pure business logic classes (TaskService, QueryService)
- **Repository Pattern**: Data access abstraction layer
- **Validation Layer**: Input sanitization and business rule enforcement
- **Error Handling**: Custom exception classes with appropriate HTTP status mapping

### Endpoint Implementation Strategy

**Request/Response Flow**:
1. **Routing**: FastAPI routes incoming requests to handler functions
2. **Dependency Injection**: Database sessions and auth tokens injected
3. **Validation**: Pydantic models validate and parse request data
4. **Business Logic**: Domain services execute core operations
5. **Data Access**: Repository layer handles database interactions
6. **Response**: Structured JSON responses with appropriate status codes

**Error Handling Implementation**:
- **Custom Exceptions**: Domain-specific exception classes
- **Exception Handlers**: FastAPI exception handlers for consistent error responses
- **Validation Errors**: Pydantic validation errors converted to API format
- **Database Errors**: SQLite errors handled with appropriate user messages

**Authentication Implementation**:
- **Local Mode**: No-op authentication (trust localhost)
- **LAN Mode**: Bearer token validation middleware
- **Token Management**: Secure token generation and validation
- **CORS Configuration**: Origin-based access control

### Query Implementation Strategy

**Filtering Implementation**:
- **Query Builder**: SQLAlchemy query construction with dynamic filters
- **Parameter Validation**: Strict validation of filter parameters
- **Type Safety**: Type hints for all query parameters
- **Performance**: Optimized queries with proper indexing

**Sorting Implementation**:
- **Column Mapping**: Safe mapping of string parameters to database columns
- **Direction Handling**: ASC/DESC with null handling
- **Compound Sorting**: Multi-column sorting with stable results
- **Default Ordering**: Sensible defaults for each endpoint

**Pagination Implementation**:
- **Cursor Encoding**: Opaque cursor strings with embedded state
- **Query Efficiency**: Cursor-based pagination for large datasets
- **Limit Enforcement**: Configurable and enforced result limits
- **Metadata**: Pagination metadata in response envelopes

### Data Export Implementation

**JSON Export**:
- **JSON Lines Format**: One task per line for streaming
- **Field Ordering**: Consistent field order for diffing
- **Timestamp Format**: ISO 8601 strings in UTC
- **Streaming Response**: Efficient handling of large exports

**CSV Export**:
- **Header Row**: Standardized column headers
- **Field Mapping**: Task fields mapped to CSV columns
- **Escaping**: Proper CSV escaping for special characters
- **Encoding**: UTF-8 with BOM for Excel compatibility

### Testing Strategy Implementation

**Unit Testing**:
- **Endpoint Testing**: Handler functions with mocked dependencies
- **Validation Testing**: Pydantic model validation edge cases
- **Business Logic**: Domain service testing with fake repositories
- **Error Handling**: Exception handler testing

**Integration Testing**:
- **API Testing**: Full request/response cycles with test database
- **Database Integration**: Real SQLite interactions with cleanup
- **Authentication**: LAN mode token validation
- **Export Testing**: End-to-end export generation and validation

**Contract Testing**:
- **OpenAPI Validation**: Generated spec matches implementation
- **Response Schema**: All responses validated against schemas
- **Error Contract**: Error responses follow documented format
- **Backward Compatibility**: Tests for API contract stability

### Performance Optimization

**Database Optimization**:
- **Indexing Strategy**: Targeted indexes on query columns
- **Query Analysis**: EXPLAIN QUERY PLAN for performance tuning
- **Connection Management**: Efficient connection pooling
- **Transaction Batching**: Group operations where possible

**API Performance**:
- **Async Handlers**: All endpoints support async/await
- **Response Caching**: ETag headers for conditional requests
- **Streaming**: Large exports use streaming responses
- **Rate Limiting**: Configurable limits for LAN mode

**Monitoring**:
- **Request Logging**: Structured logging for all API calls
- **Performance Metrics**: Response time tracking
- **Error Tracking**: Comprehensive error logging
- **Health Endpoints**: System status monitoring

## Future API Evolution
- **API v2**: May include breaking changes for advanced features
- **WebSocket Support**: Real-time updates for collaborative features
- **Bulk Operations**: Batch task creation/updates
- **Advanced Querying**: Full-text search and complex filters
