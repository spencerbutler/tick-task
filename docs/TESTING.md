# Testing Strategy (v1.0)

## Test Pyramid & Coverage Expectations

### Test Categories & Coverage Targets

#### Unit Tests (≥80% statement coverage, ≥90% branch coverage)
**Scope**: Individual functions, classes, and modules in isolation
**Mocking**: External dependencies (database, filesystem, network)
**Runtime**: <100ms per test, <30 seconds total suite
**Location**: `src/` modules with `tests/unit/`

**Test Targets**:
- **Data Models**: Task entity validation, field constraints, serialization
- **Business Logic**: Status transitions, priority ordering, filtering logic
- **Utilities**: Date parsing, tag normalization, export formatting
- **Validation**: Input sanitization, schema enforcement, error handling
- **Query Building**: Filter construction, sort parameter validation

**Examples**:
- Task creation with invalid titles (empty, too long, whitespace-only)
- Priority enum validation and ordering comparisons
- Tag deduplication and normalization logic
- ISO datetime parsing and timezone handling

#### Integration Tests (≥90% API endpoint coverage)
**Scope**: Component interactions, API endpoints with real database
**Mocking**: External services only (no database mocking)
**Runtime**: <200ms per test, <2 minutes total suite
**Location**: `tests/integration/`

**Test Targets**:
- **API Endpoints**: CRUD operations with realistic data
- **Database Layer**: SQLite transactions, migrations, concurrent access
- **Data Flow**: Create → Read → Update → Delete cycles
- **Error Handling**: Database constraints, invalid inputs, edge cases

**Examples**:
- Full task lifecycle (create → update → complete → archive)
- Complex filtering (multiple criteria, sorting combinations)
- Export functionality with various data sizes
- Database integrity after crash simulation

#### End-to-End Tests (≥95% user workflow coverage)
**Scope**: Complete user journeys through the web interface
**Mocking**: None - full stack testing
**Runtime**: <5 seconds per test, <3 minutes total suite
**Location**: `tests/e2e/`

**Test Targets**:
- **Core Workflows**: Task creation, editing, completion, organization
- **View Navigation**: Switching between Today, Inbox, Contexts, Tags
- **Data Persistence**: Changes survive page refreshes
- **Error Recovery**: Network failures, invalid inputs, edge cases

**Examples**:
- Create task via quick-add → edit in modal → complete via keyboard shortcut
- Filter tasks by multiple criteria → sort results → export to CSV
- Navigate between views → verify task counts and ordering
- Simulate offline → verify local storage and sync on reconnect

#### Accessibility Tests (100% WCAG 2.1 AA compliance)
**Scope**: UI components and pages for accessibility violations
**Automation**: axe-core integration with test runners
**Runtime**: <10 seconds per page/component
**Location**: `tests/accessibility/`

**Test Targets**:
- **Color Contrast**: Text/background ratios meet WCAG AA standards
- **Keyboard Navigation**: Tab order, focus management, shortcuts
- **Screen Reader**: ARIA labels, semantic HTML, live regions
- **Touch Targets**: Minimum 44px size, adequate spacing
- **Content Scaling**: 200% zoom without horizontal scroll

### What NOT to Test
- **Third-party Libraries**: Assume frameworks work correctly (React, FastAPI, SQLite)
- **Browser APIs**: Trust browser implementations (DOM, Fetch, LocalStorage)
- **Operating System**: File permissions, network stack, process management
- **Performance Micro-optimizations**: Focus on architectural performance budgets
- **Visual Design Details**: Colors, spacing, typography (manual QA covers this)

## Test Data Strategy

### Test Data Patterns
- **Factory Functions**: Consistent object creation with overrides
- **Fixtures**: Predefined datasets for common scenarios
- **Builders**: Fluent interfaces for complex object construction
- **Constants**: Well-known values for assertions and comparisons

### Data Categories
- **Valid Data**: Normal use cases, edge cases within bounds
- **Invalid Data**: Constraint violations, malformed inputs
- **Edge Cases**: Empty collections, maximum field lengths, special characters
- **Realistic Scenarios**: Representative of actual user data and workflows

### Test Database Management
- **In-Memory SQLite**: Fast, isolated, no cleanup required
- **Transactional Rollback**: Each test starts with clean state
- **Schema Validation**: Tests verify database constraints
- **Migration Testing**: Schema changes tested against sample data

## Quality Gates & Automation

### Pre-commit Hooks (Required)
**Trigger**: Before each commit
**Timeout**: <30 seconds
**Failure Behavior**: Block commit with clear error messages

**Checks**:
- **Code Formatting**: Black (Python), Prettier (JavaScript/TypeScript)
- **Import Sorting**: isort (Python), eslint import/sort (JavaScript)
- **Linting**: flake8 (Python), eslint (JavaScript/TypeScript)
- **Type Checking**: mypy (Python), tsc (TypeScript)
- **Fast Unit Tests**: Subset of critical path tests (<5 seconds)

### CI Pipeline (Required)
**Trigger**: Push to feature branches, all PRs
**Platforms**: Ubuntu (primary), Windows/macOS (validation)
**Timeout**: <10 minutes total
**Required Status**: Must pass before merge

**Stages**:
1. **Lint & Type Check** (<1 minute): All static analysis
2. **Unit Tests** (<2 minutes): Full unit test suite with coverage
3. **Integration Tests** (<3 minutes): API + database tests
4. **E2E Tests** (<3 minutes): Full browser automation
5. **Accessibility Audit** (<1 minute): WCAG compliance check
6. **Performance Budget** (<30 seconds): Response time validation

### Coverage Requirements
- **Unit Tests**: ≥80% statement, ≥90% branch coverage
- **Integration Tests**: ≥90% API endpoint coverage
- **E2E Tests**: ≥95% user workflow coverage
- **Accessibility**: 100% WCAG 2.1 AA compliance
- **Overall**: ≥95% acceptance criteria test coverage

## Performance Budget Checks

### API Response Times
- **Health Check**: <50ms (GET /health)
- **Task CRUD**: <100ms (typical operations)
- **Task Queries**: <500ms (complex filters on 10k tasks)
- **Export Operations**: <30 seconds (10k tasks to JSON/CSV)

### Startup Performance
- **Backend**: <2 seconds (FastAPI startup + database init)
- **Frontend**: <3 seconds (React hydration + data load)
- **Total**: <5 seconds (full application ready)

### Resource Usage
- **Memory**: <200MB (normal operation peak)
- **Database Size**: <10MB (10k tasks with full metadata)
- **CPU**: <10% average (background operations)

### Performance Test Automation
- **Load Testing**: Artillery.js for API endpoint stress testing
- **Bundle Analysis**: webpack-bundle-analyzer for frontend assets
- **Lighthouse CI**: Automated performance scoring
- **Database Benchmarks**: Custom scripts for query performance

## Test Organization & Naming

### File Structure
```
tests/
├── unit/                    # Unit tests (pytest)
│   ├── test_task_model.py
│   ├── test_validation.py
│   └── test_queries.py
├── integration/             # Integration tests (pytest)
│   ├── test_api_endpoints.py
│   └── test_database.py
├── e2e/                     # E2E tests (playwright)
│   ├── specs/
│   │   ├── task-management.spec.ts
│   │   └── view-navigation.spec.ts
│   └── fixtures/
└── accessibility/           # A11y tests (axe-core)
    ├── test-contrast.js
    └── test-navigation.js
```

### Naming Conventions
- **Test Files**: `test_*.py`, `*.spec.ts`, `test-*.js`
- **Test Functions**: `test_*` with descriptive names
- **Test Classes**: `Test*` for pytest class-based tests
- **Mock Objects**: `mock_*`, `fake_*`, `stub_*`

### Test Metadata
- **Issue Links**: Reference SPEC acceptance criteria
- **Performance Benchmarks**: Mark slow tests for separate execution
- **Flaky Tests**: Quarantine and track separately
- **Manual Tests**: Document in comments for regression testing

## Test Execution & Reporting

### Local Development
- **Watch Mode**: Automatic re-run on file changes
- **Debug Mode**: Step-through debugging with breakpoints
- **Coverage Reports**: HTML reports with missing line highlights
- **Selective Running**: Run specific tests, modules, or tags

### CI/CD Integration
- **Parallel Execution**: Split tests across multiple workers
- **Artifact Collection**: Screenshots, videos, logs on failure
- **Coverage Upload**: Send reports to external services
- **Status Reporting**: Update PR checks with detailed results

### Test Result Analysis
- **Failure Triaging**: Categorize failures (code vs environment vs flaky)
- **Trend Analysis**: Track test reliability and performance over time
- **Root Cause Analysis**: Debug failures with detailed logging
- **Regression Prevention**: Block merges until failures are addressed

## Test Maintenance Guidelines

### Refactoring Tests
- **DRY Principle**: Extract common setup/teardown into fixtures
- **Test Data Builders**: Use fluent interfaces for complex objects
- **Custom Assertions**: Create domain-specific assertion helpers
- **Page Objects**: Abstract UI interactions for E2E tests

### Adding New Tests
- **TDD Approach**: Write test first, then implementation
- **Acceptance Criteria**: Every SPEC requirement must have tests
- **Edge Cases**: Test boundaries and error conditions
- **Performance**: Include performance assertions where specified

### Test Debt Management
- **Technical Debt**: Track and prioritize test improvements
- **Flaky Tests**: Investigate root causes, fix or remove
- **Maintenance Burden**: Keep tests fast, reliable, and maintainable
- **Documentation**: Update test docs when behavior changes
