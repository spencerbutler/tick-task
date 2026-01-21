# Decision Log

Record design choices that trade off simplicity vs capability.

## Technology Stack Decisions

### Date: 2026-01-21
**Decision**: Use Python FastAPI backend with React TypeScript frontend and SQLite persistence
**Context**: Choosing the complete technology stack for FIN-tasks v1.0
**Alternatives Considered**:
- Django/Flask backend with Vue.js/Svelte frontend
- Node.js/Express backend with React frontend
- Electron for desktop app
**Rationale**:
- FastAPI provides excellent async performance, auto-generated API docs, and type safety
- React + TypeScript offers best-in-class developer experience and accessibility
- SQLite provides crash-safe local persistence with zero external dependencies
- Python packaging ecosystem is mature and cross-platform
**Consequences**:
- Minimal dependencies (FastAPI, SQLAlchemy, React, TypeScript only)
- Excellent performance and developer experience
- Cross-platform compatibility (Windows/macOS/Linux)
- Local-first architecture with no cloud requirements

### Date: 2026-01-21
**Decision**: Single-page application served by backend, no separate frontend deployment
**Context**: How to deploy the web UI
**Alternatives Considered**:
- Separate frontend/backend deployments
- Electron desktop application
- Static site generation
**Rationale**:
- Simplifies deployment (single executable/package)
- Reduces CORS complexity
- Enables offline capability
- Follows local-first principles
**Consequences**:
- Single deployment artifact
- Backend serves both API and UI
- Hot reload in development
- No separate build pipelines

## Data Model Decisions

### Date: 2026-01-21
**Decision**: Use descriptive priority enum (low/medium/high/urgent) instead of numeric scale
**Context**: How to represent task priority levels
**Alternatives Considered**:
- Numeric scale (1-5 or P0-P4)
- Custom priority names per user
- Priority scores with labels
**Rationale**:
- More intuitive for users (self-documenting)
- Aligns with common task management conventions
- Easier to understand in exports and API responses
- Reduces ambiguity in sorting and filtering
**Consequences**:
- Fixed four-level priority system
- Consistent across all users
- Simple to implement and test

### Date: 2026-01-21
**Decision**: Store tags as JSON array in single TEXT column
**Context**: How to store multiple tags per task in SQLite
**Alternatives Considered**:
- Junction table (tasks_tags many-to-many)
- Comma-separated string
- Serialized pickle/binary format
**Rationale**:
- SQLite has good JSON support
- Maintains data locality (no joins needed)
- Easy to query with JSON_EXTRACT functions
- Simple to export/import
- Adequate performance for v1.0 (max 10 tags per task)
**Consequences**:
- No additional tables required
- Tag queries use JSON functions
- Easy to extend in future
- Good performance for typical usage

### Date: 2026-01-21
**Decision**: Exclude estimate field from v1.0 schema
**Context**: Whether to include time/point estimates for tasks
**Alternatives Considered**:
- Time estimates (minutes/hours)
- Story points (1, 2, 3, 5, 8, 13)
- Both time and points
- Custom estimate types
**Rationale**:
- Complex to implement well (different methodologies)
- Not core to basic task management workflow
- Can be added in v2.0 without breaking changes
- Keeps initial scope focused on essential features
**Consequences**:
- Simpler initial data model
- Faster time to v1.0 release
- Future extensibility maintained
- No migration complexity

## API Design Decisions

### Date: 2026-01-21
**Decision**: Use cursor-based pagination with opaque cursors
**Context**: How to implement efficient pagination for large task lists
**Alternatives Considered**:
- Offset/limit pagination
- Keyset pagination with compound keys
- Infinite scroll without pagination
**Rationale**:
- Better performance than offset/limit for large datasets
- Stable across data changes (unlike offset)
- Opaque cursors prevent API clients from making assumptions
- Scales well with SQLite indexing
**Consequences**:
- More complex client implementation
- Excellent performance characteristics
- Future-proof for large datasets
- Requires proper cursor encoding/decoding

### Date: 2026-01-21
**Decision**: Polling-based synchronization for v1.0, WebSocket support reserved for future
**Context**: How to handle real-time updates between UI and API
**Alternatives Considered**:
- WebSocket connections for real-time updates
- Server-sent events (SSE)
- Long polling
- Client-side polling only
**Rationale**:
- Polling is simpler to implement and test
- Works reliably with existing HTTP infrastructure
- Adequate for typical task management usage patterns
- WebSocket can be added in v2.0 for real-time features
**Consequences**:
- 30-60 second polling interval for updates
- Simple to implement and debug
- No additional infrastructure requirements
- Scales well for single-user application

## Security Decisions

### Date: 2026-01-21
**Decision**: Localhost-only by default, optional LAN mode with token authentication
**Context**: Security model for local-first application
**Alternatives Considered**:
- Always require authentication
- OAuth-only access (no local mode)
- API key authentication
- No authentication (completely open)
**Rationale**:
- Localhost trust for primary use case
- LAN mode available for advanced users
- Token-based auth is cryptographically secure
- Balances security with usability
**Consequences**:
- Two distinct security modes
- LAN mode requires explicit user action
- Token generation and management needed
- Clear security boundaries

### Date: 2026-01-21
**Decision**: Defer Google OAuth implementation to post-v1.0
**Context**: Authentication mechanism for multi-user scenarios
**Alternatives Considered**:
- Implement Google OAuth in v1.0
- Use other OAuth providers (GitHub, Microsoft)
- Custom username/password authentication
- Admin-only authentication mode
**Rationale**:
- Google OAuth requires additional dependencies and complexity
- Admin-only mode provides basic multi-user capability
- Keeps v1.0 focused on core functionality
- OAuth can be added as optional feature
**Consequences**:
- v1.0 ships with admin-only auth for LAN mode
- Simpler security implementation
- Future OAuth integration path clear
- No additional dependencies in v1.0

## Performance Decisions

### Date: 2026-01-21
**Decision**: Target <5 second startup time, <200MB memory usage
**Context**: Performance requirements for local application
**Alternatives Considered**:
- Faster startup (2-3 seconds) with higher complexity
- Lower memory usage (100MB) with reduced features
- No specific performance targets
**Rationale**:
- 5 seconds is acceptable for a local application
- 200MB is reasonable for modern systems
- Balances user experience with implementation complexity
- Measurable and testable requirements
**Consequences**:
- Performance monitoring and optimization required
- Architecture designed with performance in mind
- Regular performance testing during development
- Clear success criteria for release

### Date: 2026-01-21
**Decision**: Optimize database queries with targeted indexes, no full-text search in v1.0
**Context**: Database performance and query capabilities
**Alternatives Considered**:
- Full-text search on titles/descriptions
- More comprehensive indexing strategy
- In-memory caching layer
**Rationale**:
- Targeted indexes cover 80% of query patterns
- Full-text search adds complexity and dependencies
- SQLite FTS may not be necessary for basic task management
- Can be added in future version if needed
**Consequences**:
- Efficient queries for core use cases
- Simpler database schema
- Good performance for 100k+ tasks
- Future FTS capability preserved

## Deployment Decisions

### Date: 2026-01-21
**Decision**: PyInstaller for cross-platform executable packaging
**Context**: How to distribute the application to end users
**Alternatives Considered**:
- Python wheel distribution only
- Docker containers
- System package managers (apt, brew)
- Web-only deployment
**Rationale**:
- Single executable simplifies installation
- Cross-platform compatibility (Windows/macOS/Linux)
- No external Python installation required
- Professional user experience
**Consequences**:
- Larger distribution size (~50MB)
- PyInstaller-specific compatibility considerations
- Build process complexity
- Excellent end-user experience

### Date: 2026-01-21
**Decision**: GitHub Releases for distribution, no auto-update mechanism in v1.0
**Context**: Application update and distribution strategy
**Alternatives Considered**:
- Auto-update mechanism built-in
- Package manager distribution (PyPI, npm)
- Platform-specific stores (Microsoft Store, Mac App Store)
**Rationale**:
- GitHub Releases is simple and reliable
- Manual updates acceptable for v1.0
- Avoids complexity of update mechanisms
- Works well with executable distribution
**Consequences**:
- Users manually download new versions
- Clear release notes and changelogs
- No background update processes
- Simpler deployment pipeline

---

Template for new decisions:
- **Date**:
- **Decision**:
- **Context**:
- **Alternatives Considered**:
- **Rationale**:
- **Consequences**:
