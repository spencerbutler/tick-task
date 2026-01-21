# Changelog

This project uses verbose, decision-oriented changelog entries.

## v0.6.0 — Development Wrapper (2026-01-21)
- **Development Tools**: Single-command development server wrapper for streamlined development
- Dev script: `dev.py` handles both backend and frontend server startup with dependency checking
- Process management: Graceful startup, monitoring, and shutdown of development servers
- Dependency validation: Automatic checking and installation of Python/Node.js dependencies
- Documentation: Comprehensive DEV_SETUP.md with setup instructions and troubleshooting

## v0.5.0 — Phase 5 Complete (2026-01-21)
- **Phase 5: Frontend Implementation** completed - React TypeScript application foundation
- Project structure: Complete frontend directory structure with components, views, hooks, and utilities
- Configuration: Vite build system, TypeScript strict configuration, Tailwind CSS with custom design system
- API integration: React Query hooks for all CRUD operations with optimistic updates and error handling
- TypeScript types: Comprehensive API type definitions matching backend schemas
- Component architecture: Navigation component with routing, responsive design with dark mode support
- Views implementation: Today view with real-time data loading, placeholder views for Inbox/Contexts/Tags
- Styling system: Tailwind CSS with custom component classes and accessibility-focused design
- Build system: Vite configuration with API proxy, code splitting, and production optimization
- Testing setup: Vitest configuration with jsdom environment and test utilities

## v0.4.0 — Phase 4 Complete (2026-01-21)
- **Phase 4: Backend Implementation** completed - functional FastAPI backend
- Database models: SQLAlchemy Task model with all required fields and constraints
- Database migrations: Alembic migration system with initial tasks table schema
- API schemas: Pydantic models for request/response validation with comprehensive field validation
- FastAPI application: Complete API server with CORS, error handling, and OpenAPI docs
- CRUD endpoints: Full task management API (create, read, update, delete, list)
- Database layer: Async SQLAlchemy session management with proper connection handling
- Configuration system: Pydantic settings with environment variable support
- Project structure: Proper Python package layout with src/ directory
- Dependencies: Complete pyproject.toml with development and production dependencies

## v0.3.0 — Phase 3 Complete (2026-01-21)
- **Phase 3: Foundation Planning** completed - detailed implementation plans
- Backend architecture: FastAPI + SQLAlchemy implementation strategy
- Frontend architecture: React + TypeScript + Vite component design
- API implementation: Request/response flow, validation, error handling
- Testing infrastructure: Unit, integration, E2E, and accessibility test plans
- Security hardening: Threat model, network security, and operational security
- Release preparation: Versioning, migrations, backups, changelog discipline
- Implementation roadmap updated with Phase 4-7 execution plans

## v0.2.0 — Phase 2 Complete (2026-01-21)
- **Phase 2: Design & Strategy** completed - comprehensive design specifications
- Detailed UX/UI specification with keyboard-first design philosophy
- Complete testing strategy with test pyramid and coverage requirements
- Pre-commit and CI pipeline specifications with quality gates
- Updated SPEC.md acceptance criteria with concrete implementation details
- Enhanced OPERATIONS.md with development workflow and deployment strategy
- Quality assurance decisions documented in DECISIONS.md

## v0.1.0 — Phase 1 Complete (2026-01-21)
- **Phase 1: Spec & Architecture Refinement** completed and merged to main
- Comprehensive SPEC.md with prioritized requirements and explicit acceptance criteria
- Complete API contract documentation with request/response schemas
- Detailed data model specification with validation rules
- Architectural decisions documented in DECISIONS.md with trade-off analysis
- Implementation roadmap created (ROADMAP.md) with 7-phase development plan
- All prompts 01-14 executed, establishing solid foundation for implementation

## Unreleased
- (v0) Repository initialized with documentation and agent prompt suite. No code introduced.
