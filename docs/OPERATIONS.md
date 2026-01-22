# Operations (v1.0)

## Development Workflow

### Branch Strategy
- **main**: Production-ready code, protected branch
- **feature/phase-X-***: Feature branches for each development phase
- **No direct commits to main**: All changes via PR review

### Pre-commit Quality Gates
**Trigger**: Before each commit on feature branches
**Timeout**: <30 seconds (blocks commit if exceeded)
**Failure Behavior**: Commit blocked with clear error messages

**Local Checks**:
- **Code Formatting**: Black (Python), Prettier (JavaScript/TypeScript)
- **Import Sorting**: isort (Python), eslint import/sort (JavaScript)
- **Linting**: flake8 (Python), eslint (JavaScript/TypeScript)
- **Type Checking**: mypy (Python), tsc (TypeScript)
- **Fast Unit Tests**: Critical path unit tests (<5 seconds)

### CI Pipeline
**Trigger**: Push to feature branches, all PRs targeting main
**Platforms**: Ubuntu (primary), Windows/macOS (validation)
**Timeout**: <10 minutes total (fails build if exceeded)
**Required Status**: Must pass before PR merge

**CI Stages**:
1. **Lint & Type Check** (<1 minute): All static analysis
2. **Unit Tests** (<2 minutes): Full unit test suite with coverage
3. **Integration Tests** (<3 minutes): API + database tests
4. **E2E Tests** (<3 minutes): Full browser automation
5. **Accessibility Audit** (<1 minute): WCAG compliance check
6. **Performance Budget** (<30 seconds): Response time validation

### Branch Protection Rules
- **main branch**: Requires PR, all CI checks pass, approved review
- **Feature branches**: Pre-commit gates only (no CI requirement)
- **PR Requirements**: Title includes model disclosure `[model: ...]`, description links to issues

## Run Modes

### Development Mode
- Hot reload enabled for both backend and frontend
- Debug logging and error pages
- CORS enabled for localhost development
- Test database with sample data

### Local Production (Single Machine)
- Optimized builds (minified, tree-shaken)
- Production logging and error handling
- SQLite database in user data directory
- Automatic startup on system boot (optional)

### LAN Mode (Explicit Opt-in)
- Requires explicit configuration change
- Binds to 0.0.0.0 with token authentication
- Cryptographically secure tokens generated per enable
- Network access logged for security

## Configuration

### Required Settings
- **Port**: Default 8000, configurable 1024-65535
- **Data Path**: Default `~/.fin-tasks/`, configurable absolute path
- **LAN Mode**: Default disabled, explicit enable required

### Optional Settings
- **Theme**: light/dark/auto (follows system preference)
- **Keyboard Shortcuts**: Enable/disable custom shortcuts
- **Export Path**: Default downloads folder, configurable
- **Log Level**: info/warn/error/debug

### Configuration Storage
- **Format**: JSON file in data directory
- **Validation**: Schema-validated on startup
- **Hot Reload**: Changes applied without restart (where possible)
- **Backup**: Configuration included in data exports

## Deployment & Distribution

### Packaging Strategy
- **PyInstaller**: Cross-platform executable generation
- **Single Binary**: No external Python installation required
- **Platform Targets**: Windows (exe), macOS (app), Linux (AppImage)
- **Size Target**: <50MB compressed

### Distribution Channels
- **GitHub Releases**: Primary distribution mechanism
- **Manual Updates**: Users download new versions manually
- **Version Checking**: Optional version check (no auto-update)
- **Installation**: Drag-and-drop or simple installer

### Data Management
- **User Data Directory**: Platform-specific locations
  - Linux: `~/.fin-tasks/`
  - macOS: `~/Library/Application Support/tick-task/`
  - Windows: `%APPDATA%\tick-task\`
- **Database**: SQLite file with WAL mode enabled
- **Configuration**: JSON file with schema validation
- **Logs**: Rotating log files with configurable retention

## Monitoring & Troubleshooting

### Logging Strategy
- **Development**: Debug level, console output, full stack traces
- **Production**: Info level, file output, user-friendly messages
- **LAN Mode**: Security events logged with timestamps
- **Performance**: Key metrics logged (startup time, query performance)

### Health Checks
- **API Endpoint**: `GET /health` returns system status
- **Database**: Connection and integrity checks
- **Disk Space**: Available space monitoring
- **Memory**: Usage tracking against 200MB budget

### Error Handling
- **User-Friendly**: Clear error messages, recovery suggestions
- **Logging**: Full technical details for debugging
- **Graceful Degradation**: Core functionality preserved during errors
- **Recovery**: Automatic retry for transient failures

## Security Operations

### Access Control
- **Local Mode**: Implicit trust (localhost only)
- **LAN Mode**: Token-based authentication required
- **Token Security**: Cryptographically secure, time-limited
- **Audit Logging**: Access attempts logged in LAN mode

### Data Protection
- **Encryption**: Optional database encryption (future feature)
- **Backup Security**: Exports contain no sensitive configuration
- **Input Validation**: All inputs sanitized and validated
- **Error Leakage**: No sensitive information in error messages

## Release & Versioning

### Versioning Strategy
- **Semantic Versioning**: MAJOR.MINOR.PATCH format
- **Pre-release**: alpha/beta/rc suffixes for development
- **Breaking Changes**: Major version increments
- **Backward Compatibility**: Minor/patch versions maintain compatibility

### Release Process
1. **Feature Complete**: All planned features implemented and tested
2. **Stabilization**: Bug fixes and performance optimization
3. **Release Candidate**: Final testing and validation
4. **Production Release**: Tagged release with changelog
5. **Post-Release**: Monitor for critical issues

### Release Checklist
- [ ] All acceptance criteria met and tested
- [ ] Performance benchmarks achieved
- [ ] Security review completed
- [ ] Documentation updated and accurate
- [ ] Cross-platform testing completed
- [ ] Installation process verified
- [ ] Changelog comprehensive and clear

## Database Management

### Migration Strategy
- **Alembic Integration**: Automated schema migrations
- **Version Control**: Migrations tracked in version control
- **Backward Compatibility**: Support for rollback if needed
- **Testing**: Migrations tested with sample data

### Schema Evolution
- **Additive Changes**: New fields/tables with defaults
- **Data Migration**: Automatic data transformation when needed
- **Deprecation**: Old fields marked deprecated before removal
- **Version Compatibility**: Clear minimum version requirements

### Backup & Recovery
- **Automated Exports**: Regular data exports for backup
- **Recovery Procedures**: Documented steps for data restoration
- **Integrity Checks**: Database validation on startup
- **Corruption Recovery**: Automatic repair when possible

## Changelog Discipline

### Changelog Format
- **Structured Entries**: Consistent format for all changes
- **Categorization**: Features, fixes, breaking changes, security
- **Issue References**: Link to GitHub issues/PRs
- **Migration Notes**: Breaking changes clearly documented

### Changelog Maintenance
- **Continuous Updates**: Changelog updated with each PR
- **Release Preparation**: Final review before tagging
- **User-Focused**: Changes described from user perspective
- **Technical Details**: Implementation details in commit messages

### Version History Tracking
- **Git Tags**: Releases tagged with version numbers
- **Release Notes**: GitHub releases with detailed notes
- **Upgrade Guide**: Migration instructions when needed
- **Deprecation Notices**: Advance warning of breaking changes

## Operational Readiness

### Pre-Release Validation
- [ ] All CI checks passing on all platforms
- [ ] Performance benchmarks met
- [ ] Security testing completed
- [ ] Accessibility compliance verified
- [ ] Documentation reviewed and complete
- [ ] Installation tested on clean systems
- [ ] Data migration tested (if applicable)

### Post-Release Monitoring
- **Health Monitoring**: Application startup and basic functionality
- **Error Tracking**: Unexpected errors reported and analyzed
- **Performance Monitoring**: Real-world performance metrics
- **User Feedback**: Issues and feature requests tracked
- **Security Monitoring**: Vulnerability reports monitored

### Support & Maintenance
- **Issue Response**: Timely response to bug reports
- **Patch Releases**: Critical bug fixes released quickly
- **Security Updates**: Expedited security patch process
- **Feature Updates**: Regular feature releases planned

---

## Agent Prompts and Editor Integration Policy

### Canonical Source of Truth
- All **canonical agent prompts** live in the top-level `prompts/` directory.
- `prompts/` is editor-agnostic and authoritative.
- All governance, review, and enforcement applies to `prompts/`.

### Cursor Integration (Non-Canonical)
- The `.cursor/prompts/` directory exists **only** to improve usability inside Cursor.
- Files in `.cursor/prompts/` are **wrapper stubs**, not authoritative content.
- Cursor users must treat `.cursor/prompts/` as a convenience layer only.

### Wrapper Stub Rules (Option A)
For every file in `prompts/*.md`, there MUST exist a corresponding wrapper file:

.cursor/prompts/<same-filename>.md


Each wrapper file MUST:
1) Clearly point to the canonical prompt in `prompts/`
2) Contain no unique or authoritative instructions
3) Be safe to overwrite automatically in the future

### Change Discipline
- Any change to `prompts/` **requires** a corresponding update to `.cursor/prompts/`
- Both must be committed in the **same commit**
- Reviewers must treat mismatches as a blocking issue

### Enforcement Model
- Short term: enforced via agent rules and PR checklist
- Long term: enforced via a repo-local sync script wired into pre-commit and CI

This policy exists to ensure:
- editor agnosticism
- zero prompt drift
- deterministic repo behavior across humans and agents
