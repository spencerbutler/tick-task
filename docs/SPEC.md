# SPEC (v1.0 - Implementation Ready)

## Product Statement
FIN-tasks is a local-first task tracking application supporting personal and professional workflows, with a stable local API for interoperation with other local apps in the FIN ecosystem.

## Vision
A beautiful, reliable task management tool that works offline-first, ensuring users never lose their data while providing powerful organization capabilities for both personal and professional contexts.

## Success Criteria (v1.0)
- [ ] All acceptance criteria pass with ≥95% test coverage
- [ ] Application starts in <5 seconds on target hardware
- [ ] Zero data loss in normal operation (crash-safe persistence)
- [ ] UI passes WCAG 2.1 AA accessibility standards
- [ ] API response time <100ms for typical operations
- [ ] Memory usage <200MB during normal operation

## Requirements Priority Framework
- **MUST (v1.0)**: Critical for core functionality, cannot be deferred
- **SHOULD (v1.0)**: Important but can be implemented post-v1.0 if time-constrained
- **COULD (Future)**: Nice-to-have, implement only if time allows
- **WON'T (Out of Scope)**: Explicitly excluded from v1.0

## Functional Requirements

### MUST (v1.0): Core Task Management

#### Task Entity (MUST-TASK-001)
**Requirement**: Tasks must have the following immutable schema:
- `id`: UUID v4, stable identifier
- `title`: String (1-200 chars), required, non-empty after trimming
- `description`: String (0-2000 chars), optional, supports markdown
- `status`: Enum [todo, doing, blocked, done, archived], default: todo
- `priority`: Enum [low, medium, high, urgent], default: medium
- `due_at`: ISO 8601 datetime, optional
- `tags`: Array of strings (0-10 items), each 1-50 chars, unique within task
- `context`: Enum [personal, professional, mixed], default: personal
- `workspace`: String (0-100 chars), optional, free-form workspace name
- `created_at`: ISO 8601 datetime, set on creation, immutable
- `updated_at`: ISO 8601 datetime, updated on any change
- `completed_at`: ISO 8601 datetime, set when status becomes done, cleared otherwise

**Acceptance Criteria**:
- [ ] API rejects tasks with invalid/missing required fields
- [ ] Title validation prevents empty/whitespace-only titles
- [ ] Status transitions are validated (archived tasks cannot be modified)
- [ ] Tags are normalized (trimmed, lowercased, deduplicated)
- [ ] Timestamps are stored in UTC with microsecond precision

#### Task CRUD Operations (MUST-CRUD-001)
**Requirement**: Full CRUD operations with proper validation and error handling.

**Create Task (MUST-CRUD-001a)**:
- Accepts all task fields except id/timestamps
- Generates UUID v4 for id
- Sets created_at/updated_at to current time
- Returns complete task object with all fields

**Read Task (MUST-CRUD-001b)**:
- Retrieves task by id
- Returns 404 for non-existent tasks
- Includes all task fields in response

**Update Task (MUST-CRUD-001c)**:
- Accepts partial updates (only changed fields)
- Validates all provided fields
- Prevents updates to archived tasks
- Sets updated_at to current time
- Returns complete updated task object

**Delete Task (MUST-CRUD-001d)**:
- Soft delete (sets status to archived)
- Maintains data integrity for future restoration
- Returns success confirmation

**Acceptance Criteria**:
- [ ] Create validates all required fields and constraints
- [ ] Update merges partial data correctly
- [ ] Delete preserves referential integrity
- [ ] All operations return appropriate HTTP status codes
- [ ] Error responses include descriptive messages

### MUST (v1.0): Task Querying and Views

#### Filtering and Sorting (MUST-QUERY-001)
**Requirement**: Tasks can be filtered and sorted by multiple criteria.

**Supported Filters**:
- `status`: Single status or array of statuses
- `context`: Single context or array of contexts
- `tags`: Tasks containing any/all of specified tags
- `priority`: Minimum priority level
- `due_before`: ISO datetime (tasks due before this date)
- `due_after`: ISO datetime (tasks due after this date)
- `updated_since`: ISO datetime (tasks updated since this time)

**Supported Sorting**:
- `created_at`: asc/desc
- `updated_at`: asc/desc
- `due_at`: asc/desc (nulls last)
- `priority`: asc/desc (urgent > high > medium > low)
- `title`: asc/desc (case-insensitive)

**Acceptance Criteria**:
- [ ] All filters work independently and in combination
- [ ] Sorting is stable and deterministic
- [ ] Empty result sets return proper structure
- [ ] Query performance scales with result size (not total tasks)

#### Predefined Views (MUST-VIEWS-001)
**Requirement**: Application provides four core views with specific filtering logic.

**Today View (MUST-VIEWS-001a)**:
- Tasks with `due_at` today (start of day to end of day)
- Tasks with `status` in [todo, doing, blocked]
- Sorted by `due_at` asc, then `priority` desc

**Inbox View (MUST-VIEWS-001b)**:
- Tasks with `status` = todo
- No `due_at` set (pure inbox items)
- Sorted by `created_at` desc (newest first)

**By Context View (MUST-VIEWS-001c)**:
- Grouped by `context` (personal/professional/mixed)
- Within each group, sorted by `updated_at` desc
- Shows all non-archived tasks

**By Tag View (MUST-VIEWS-001d)**:
- Grouped by tags (tasks can appear in multiple groups)
- Within each group, sorted by `updated_at` desc
- Only shows tasks with at least one tag

**Acceptance Criteria**:
- [ ] Each view returns correct task subsets
- [ ] Grouping works correctly (no data loss/duplication)
- [ ] Sorting within groups is applied properly
- [ ] Views update correctly when tasks change

### MUST (v1.0): Data Persistence

#### SQLite Backend (MUST-PERSIST-001)
**Requirement**: All data stored in SQLite database with crash-safe operations.

**Database Schema**:
- Single `tasks` table with all task fields
- Proper indexes on frequently queried columns
- Foreign key constraints where applicable
- Transactional operations for data integrity

**Crash Safety**:
- WAL mode enabled for concurrent reads/writes
- Transaction rollback on errors
- Database integrity checks on startup
- Automatic recovery from corruption

**Acceptance Criteria**:
- [ ] SQLite database created automatically on first run
- [ ] All CRUD operations wrapped in transactions
- [ ] Application recovers gracefully from database corruption
- [ ] Concurrent access (API + UI) works correctly

#### Export Functionality (MUST-EXPORT-001)
**Requirement**: Tasks can be exported in multiple formats for backup/portability.

**JSON Export (MUST-EXPORT-001a)**:
- Complete task data in JSON Lines format (.jsonl)
- One task per line, valid JSON parseable
- All fields included, timestamps in ISO format
- Sorted by created_at for consistency

**CSV Export (MUST-EXPORT-001b)**:
- Human-readable tabular format
- Columns: id, title, description, status, priority, due_at, tags, context, workspace, created_at, updated_at, completed_at
- Tags as comma-separated string
- Proper CSV escaping for special characters

**Acceptance Criteria**:
- [ ] JSON export contains all task data and metadata
- [ ] CSV export is readable in spreadsheet applications
- [ ] Export operations complete within 30 seconds for 10k tasks
- [ ] Exported files include timestamp in filename

### MUST (v1.0): Local API

#### REST API Design (MUST-API-001)
**Requirement**: HTTP REST API running on localhost with OpenAPI documentation.

**Endpoints**:
- `GET /health` - Health check endpoint
- `GET /tasks` - List tasks with filtering/sorting/pagination
- `POST /tasks` - Create new task
- `GET /tasks/{id}` - Get specific task
- `PUT /tasks/{id}` - Update specific task
- `DELETE /tasks/{id}` - Archive specific task
- `GET /export` - Export tasks (JSON/CSV)

**Request/Response Format**:
- JSON request/response bodies
- Standard HTTP status codes
- Error responses include `error` field with description
- Pagination uses cursor-based approach

**Acceptance Criteria**:
- [ ] All endpoints documented in OpenAPI 3.0 spec
- [ ] API responses are valid JSON with correct schemas
- [ ] Error responses include helpful messages
- [ ] API handles malformed requests gracefully

#### Security and Access Control (MUST-API-002)
**Requirement**: Local-only access with optional LAN mode.

**Localhost Binding (MUST-API-002a)**:
- Server binds to 127.0.0.1 only by default
- No external network access without explicit configuration
- CORS headers allow localhost origins

**LAN Mode (MUST-API-002b)**:
- Optional configuration to bind to 0.0.0.0
- Requires explicit token authentication
- Token must be provided in Authorization header
- Token is generated on first LAN mode enable

**Acceptance Criteria**:
- [ ] Default configuration only accepts localhost connections
- [ ] LAN mode requires explicit configuration change
- [ ] Token authentication works correctly in LAN mode
- [ ] Invalid tokens return 401 Unauthorized

### SHOULD (v1.0): User Experience

#### Responsive Web UI (SHOULD-UI-001)
**Requirement**: Beautiful, responsive web interface accessible at http://localhost:8000.

**Design Principles**:
- Clean, minimal aesthetic suitable for daily use
- Responsive design working on 1024px+ widths
- Dark/light mode support (system preference)
- Keyboard navigation support
- Loading states and error handling

**Core Pages**:
- Dashboard: Today view with summary stats
- Tasks: Full task list with filtering/sorting
- Task Detail: Create/edit individual tasks
- Settings: Application configuration

**Acceptance Criteria**:
- [ ] UI loads and functions without JavaScript errors
- [ ] All core workflows work end-to-end (task creation, editing, completion, filtering)
- [ ] Four required views implemented: Today, Inbox, Contexts, Tags
- [ ] Interface is usable on desktop browsers (Chrome, Firefox, Safari) at 1024px+
- [ ] Keyboard navigation works for all interactive elements (Tab order, shortcuts)
- [ ] Dark/light mode support with system preference detection
- [ ] Responsive design with touch-friendly targets (44px minimum)
- [ ] Task creation supports smart parsing syntax (#tag @context !priority)
- [ ] Real-time filtering and search functionality
- [ ] Loading states and error boundaries implemented

#### Accessibility Compliance (SHOULD-ACCESS-001)
**Requirement**: UI meets WCAG 2.1 AA accessibility standards.

**Requirements**:
- Screen reader compatibility
- Keyboard-only navigation
- Sufficient color contrast ratios
- Semantic HTML structure
- Focus management and indicators

**Acceptance Criteria**:
- [ ] Passes automated accessibility audits
- [ ] Screen reader can navigate and operate all features
- [ ] Keyboard navigation covers all interactive elements
- [ ] Color contrast meets WCAG AA standards

### SHOULD (v1.0): Quality Assurance

#### Test Coverage (SHOULD-TEST-001)
**Requirement**: Comprehensive automated test suite covering all acceptance criteria.

**Unit Tests**: ≥80% statement coverage
**Integration Tests**: API + database interaction
**End-to-End Tests**: Complete user workflows
**Accessibility Tests**: Automated WCAG compliance

**Acceptance Criteria**:
- [ ] Unit tests: ≥80% statement, ≥90% branch coverage
- [ ] Integration tests: ≥90% API endpoint coverage
- [ ] E2E tests: ≥95% user workflow coverage
- [ ] Accessibility tests: 100% WCAG 2.1 AA compliance
- [ ] Overall: ≥95% acceptance criteria test coverage
- [ ] Test suite runs in <5 minutes locally
- [ ] Tests pass on all supported platforms (Ubuntu primary, Windows/macOS validation)
- [ ] Coverage reports generated and tracked
- [ ] Pre-commit hooks block commits on failures (<30 seconds)
- [ ] CI pipeline passes all stages before merge (<10 minutes)

#### Pre-commit Quality Gates (SHOULD-CI-001)
**Requirement**: Automated quality checks prevent regressions.

**Pre-commit Hooks**:
- Code formatting (black, isort)
- Type checking (mypy)
- Lint checking (flake8, eslint)
- Unit tests (subset)

**CI Pipeline**:
- Full test suite on push/PR
- Coverage reporting
- Security scanning
- Build verification

**Acceptance Criteria**:
- [ ] Pre-commit hooks run automatically
- [ ] CI passes for all PRs before merge
- [ ] Code formatting is consistent across codebase
- [ ] Type errors are caught before commit

## Performance Requirements

### MUST (v1.0): Performance Targets
- **Startup Time**: <5 seconds from launch to UI ready
- **API Response Time**: <100ms for typical operations (create, read, update)
- **Query Performance**: <500ms for complex queries on 10k tasks
- **Memory Usage**: <200MB during normal operation
- **Database Size**: Efficient storage (target <10MB for 10k tasks)

### SHOULD (v1.0): Scalability Targets
- Support for 100k+ tasks without performance degradation
- Concurrent API requests handled gracefully
- Background operations don't block UI
- Export operations scale linearly with data size

## Security Requirements

### MUST (v1.0): Security Baseline
- **Local-Only Access**: No external exposure by default
- **Input Validation**: All user inputs validated and sanitized
- **Error Handling**: No sensitive information in error messages
- **Dependency Security**: Regular security updates for dependencies

### SHOULD (v1.0): Enhanced Security
- **Token Security**: Cryptographically secure tokens for LAN mode
- **Request Rate Limiting**: Basic protection against abuse
- **Audit Logging**: Important operations logged locally
- **Data Encryption**: Optional encryption for sensitive data

## Non-Goals (Explicit Exclusions)
- **Multi-user support**: Single-user application only
- **Cloud synchronization**: Local-only data storage
- **Mobile native apps**: Web-based interface only
- **Complex recurrence**: No recurring task support
- **Advanced search**: Basic filtering only (no full-text search)
- **Real-time collaboration**: Single-user, local-only
- **Plugin ecosystem**: Monolithic application design
- **Advanced reporting**: Basic export functionality only

## Implementation Constraints
- **Technology Stack**: Python FastAPI backend, React TypeScript frontend, SQLite database
- **Platform Support**: Windows 10+, macOS 11+, Linux (Ubuntu 20.04+)
- **Browser Support**: Chrome 90+, Firefox 88+, Safari 14+
- **Python Version**: 3.9+ required
- **Node Version**: 16+ required (for development)

## Implementation Plan

### Phase 3: Foundation Planning (Current)
**Status**: In Progress - Planning and specification complete

**Deliverables**:
- Backend foundation: FastAPI + SQLAlchemy architecture specified
- Frontend foundation: React + TypeScript + Vite stack confirmed
- Testing infrastructure: pytest + Playwright frameworks selected
- Development environment: Local setup and tooling defined
- Quality gates: Pre-commit and CI policies established

**Success Criteria**:
- All technology choices documented with rationale
- Dependency list justified and minimal
- Test strategy maps requirements to test types
- Development workflow supports efficient coding

### Phase 4: Backend Implementation
**Status**: Planned

**Deliverables**:
- SQLite schema with Alembic migrations
- FastAPI endpoints with Pydantic validation
- Business logic layer with domain services
- Comprehensive backend test suite (unit + integration)

**Test Mapping**:
- Unit: Task model validation, query logic, utility functions
- Integration: CRUD operations, database transactions, API contracts
- Performance: Query optimization, memory usage, startup time

### Phase 5: Frontend Implementation
**Status**: Planned

**Deliverables**:
- React component architecture with TypeScript
- Four core views (Today, Inbox, Contexts, Tags)
- State management with React Query
- Responsive design with accessibility compliance

**Test Mapping**:
- Unit: Component rendering, user interactions, state updates
- Integration: API integration, routing, error boundaries
- E2E: Complete user workflows, accessibility validation
- Performance: Bundle size, rendering performance, memory usage

### Phase 6: Integration & Authentication
**Status**: Planned

**Deliverables**:
- Frontend/backend REST API integration
- Authentication system (admin mode + OAuth preparation)
- End-to-end testing pipeline
- Security hardening and input validation

**Test Mapping**:
- Integration: API authentication, data synchronization
- E2E: Multi-step workflows, error recovery, security validation
- Contract: API schema compliance, request/response validation

### Phase 7: Release Preparation
**Status**: Planned

**Deliverables**:
- PyInstaller packaging for cross-platform distribution
- Final testing and performance optimization
- Documentation completion and user guides
- v1.0.0 release with comprehensive changelog

**Test Mapping**:
- E2E: Installation process, first-run experience, data migration
- Performance: Full application benchmarks, resource usage
- Accessibility: Complete WCAG 2.1 AA audit
- Integration: Packaging verification, deployment automation

## Success Metrics (v1.0)
- All MUST requirements implemented and tested
- SHOULD requirements implemented where time permits
- Zero critical bugs in manual testing
- Performance targets met on target hardware
- Documentation complete and accurate
- Installation process works on all supported platforms
