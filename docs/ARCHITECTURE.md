# Architecture (v1.0 - Implementation Ready)

## System Overview
FIN-tasks is a local-first task management application built with a clean architecture that separates concerns while maintaining simplicity and performance. The system consists of a Python FastAPI backend serving a React TypeScript frontend, with SQLite providing durable local persistence.

## Architectural Principles
- **Local-First**: All data stored locally, works offline, no cloud dependencies
- **Minimal Dependencies**: Carefully selected third-party libraries with clear justification
- **Separation of Concerns**: Domain, persistence, API, and UI layers clearly defined
- **Testability**: Architecture designed for comprehensive automated testing
- **Performance**: Optimized for local execution with sub-100ms response times
- **Security**: Defense-in-depth with localhost-first security model

## Component Architecture

### Domain Layer
**Purpose**: Business logic, validation, and core task management functionality.

**Components**:
- **Task Entity**: Pydantic model defining task schema and validation rules
- **Task Service**: Business logic for task operations (CRUD, status transitions)
- **Query Service**: Filtering, sorting, and view generation logic
- **Validation Service**: Input validation and business rule enforcement

**Responsibilities**:
- Enforce business invariants (task state transitions, validation rules)
- Provide domain-specific operations (complete task, archive task)
- Define query interfaces for different views
- Maintain data consistency across operations

### Persistence Layer
**Purpose**: Durable data storage with crash-safe operations.

**Technology**: SQLite with SQLAlchemy ORM

**Components**:
- **Database Models**: SQLAlchemy declarative models mapping to database tables
- **Repository Pattern**: Abstract data access interface
- **Migration System**: Alembic for schema versioning and updates
- **Connection Management**: Database session and transaction handling

**Features**:
- WAL mode for concurrent reads/writes
- Automatic transaction management
- Database integrity checks on startup
- Efficient indexing for query performance

### API Layer
**Purpose**: HTTP REST API for client access and interoperation.

**Technology**: FastAPI with automatic OpenAPI documentation

**Endpoints**:
```
GET  /health              - Health check
GET  /tasks               - List tasks with filtering/sorting
POST /tasks               - Create new task
GET  /tasks/{id}          - Get specific task
PUT  /tasks/{id}          - Update specific task
DELETE /tasks/{id}        - Archive specific task
GET  /export              - Export tasks (JSON/CSV)
```

**Features**:
- Request/response validation using Pydantic
- Automatic API documentation generation
- CORS configuration for web UI access
- Error handling with structured error responses
- Optional authentication for LAN mode

### UI Layer
**Purpose**: Web-based user interface for task management.

**Technology**: React 18 + TypeScript + Tailwind CSS

**Components**:
- **Dashboard**: Today view with task summary and quick actions
- **Task List**: Filterable/sortable task listing with bulk operations
- **Task Form**: Create/edit task interface with validation
- **Settings**: Application configuration and preferences

**Features**:
- Responsive design (desktop-first, 1024px+ support)
- Keyboard navigation and accessibility (WCAG 2.1 AA)
- Real-time updates using React Query
- Offline-capable with service worker (future)
- Dark/light mode support

## Data Flow Architecture

### Task Creation Flow
1. UI collects task data via form validation
2. React Query sends POST /tasks request to API
3. FastAPI validates request using Pydantic models
4. Domain service validates business rules
5. Repository saves to SQLite within transaction
6. Response flows back through layers to UI
7. UI updates optimistically and refetches data

### Task Query Flow
1. UI requests tasks via React Query with filter parameters
2. API receives GET /tasks with query parameters
3. Domain service applies filtering/sorting logic
4. Repository executes optimized SQL queries
5. Results serialized and returned through API
6. UI renders tasks with loading/error states

## Security Architecture

### Network Security
- **Default State**: Binds to 127.0.0.1 (localhost only)
- **LAN Mode**: Optional 0.0.0.0 binding with token authentication
- **CORS Policy**: Restrictive, localhost origins only by default
- **Rate Limiting**: Basic protection against abuse (future)

### Data Security
- **Input Validation**: All inputs validated at API and domain layers
- **SQL Injection Protection**: ORM parameterization prevents injection
- **Error Handling**: No sensitive data in error messages
- **Data Encryption**: Optional encryption for sensitive fields (future)

### Authentication & Authorization
- **Local Mode**: No authentication required (localhost trust)
- **LAN Mode**: Bearer token authentication required
- **Token Management**: Cryptographically secure token generation
- **Session Security**: Short-lived tokens with automatic expiration

## Performance Architecture

### Database Optimization
- **Indexing Strategy**: Optimized indexes on query fields (status, context, tags, dates)
- **Query Planning**: Efficient SQL generation with proper joins
- **Connection Pooling**: SQLAlchemy connection management
- **WAL Mode**: Concurrent read/write support

### API Performance
- **Async Operations**: FastAPI async endpoints for I/O operations
- **Response Caching**: In-memory caching for frequently accessed data
- **Pagination**: Cursor-based pagination for large result sets
- **Serialization**: Efficient JSON serialization with orjson

### UI Performance
- **Code Splitting**: Route-based code splitting with React.lazy
- **Bundle Optimization**: Vite production build with tree shaking
- **State Management**: React Query for server state caching
- **Virtual Scrolling**: For large task lists (future optimization)

## Deployment Architecture

### Development Environment
- **Local Development**: Hot reload for both backend and frontend
- **Docker Support**: Optional containerized development
- **Database**: Local SQLite file with migrations
- **Ports**: Backend on 8000, frontend dev server on 5173

### Production Deployment
- **Single Executable**: PyInstaller bundles Python app + frontend assets
- **Configuration**: Environment variables and local config files
- **Database**: Automatic SQLite creation and migration
- **Process Management**: Graceful startup/shutdown handling

### Platform Support
- **Windows**: Portable executable with proper file associations
- **macOS**: App bundle with code signing and notarization
- **Linux**: AppImage or system packages with sandboxing

## Observability & Monitoring

### Logging
- **Structured Logging**: JSON format with consistent fields
- **Log Levels**: DEBUG, INFO, WARNING, ERROR
- **Log Rotation**: Automatic log file rotation and cleanup
- **Performance Logging**: Slow query detection and alerting

### Health Checks
- **Application Health**: /health endpoint with system status
- **Database Health**: Connection and integrity checks
- **Dependency Health**: Third-party service availability
- **Performance Metrics**: Response times and resource usage

### Error Tracking
- **Error Boundaries**: UI error boundaries with user-friendly messages
- **Exception Handling**: Comprehensive error handling with proper logging
- **User Feedback**: Error reporting with actionable messages
- **Debug Information**: Development mode error details

## Testing Architecture

### Unit Testing
- **Backend**: pytest with 80%+ coverage target
- **Frontend**: Vitest with React Testing Library
- **Coverage**: Branch and function coverage tracking
- **Mocking**: External dependencies mocked for isolation

### Integration Testing
- **API Testing**: Full request/response cycles with test database
- **Database Testing**: SQLite in-memory for fast, isolated tests
- **Component Integration**: Component interaction testing
- **Contract Testing**: API contract validation

### End-to-End Testing
- **User Workflows**: Complete task management workflows
- **Cross-Browser**: Chrome, Firefox, Safari compatibility
- **Accessibility**: Automated WCAG compliance testing
- **Performance**: Lighthouse and custom performance tests

## Evolution & Extensibility

### Modular Design
- **Plugin Architecture**: Extension points for future features
- **Configuration System**: Feature flags and runtime configuration
- **API Versioning**: REST API versioning for backward compatibility
- **Database Migrations**: Safe schema evolution with rollback capability

### Future Considerations
- **Mobile Support**: Progressive Web App capabilities
- **Multi-User**: Optional user accounts with data isolation
- **Sync**: Selective cloud synchronization (opt-in)
- **Advanced Features**: Recurrence, full-text search, advanced reporting

## Decision Records
See docs/DECISIONS.md for detailed rationale behind architectural choices:
- Technology stack selection criteria
- Dependency evaluation framework
- Performance vs complexity trade-offs
- Security design decisions

This architecture provides a solid foundation for FIN-tasks v1.0 while maintaining flexibility for future evolution.
