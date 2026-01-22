# tick-task Data Model (v1.0)

## Overview
The tick-task data model centers around a single `Task` entity that captures all task-related information. The model is designed for local-first usage with SQLite as the persistence layer, emphasizing data integrity, query performance, and export capability.

## Task Entity Schema

### Core Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | UUID v4 | Yes | Auto-generated | Stable, unique identifier |
| `title` | VARCHAR(200) | Yes | N/A | Task title, 1-200 characters |
| `description` | TEXT | No | NULL | Task description, supports markdown, max 2000 chars |
| `status` | ENUM | Yes | 'todo' | Task status: todo, doing, blocked, done, archived |
| `priority` | ENUM | Yes | 'medium' | Task priority: low, medium, high, urgent |
| `due_at` | DATETIME | No | NULL | Due date/time in ISO 8601 format |
| `tags` | JSON | No | [] | Array of tag strings, max 10 tags |
| `context` | ENUM | Yes | 'personal' | Context: personal, professional, mixed |
| `workspace` | VARCHAR(100) | No | NULL | Free-form workspace name |
| `created_at` | DATETIME | Yes | Auto-set | Creation timestamp (UTC) |
| `updated_at` | DATETIME | Yes | Auto-set | Last update timestamp (UTC) |
| `completed_at` | DATETIME | No | NULL | Completion timestamp (UTC) |

### SQLite Table Definition
```sql
CREATE TABLE tasks (
    id TEXT PRIMARY KEY NOT NULL,           -- UUID v4
    title TEXT NOT NULL,                    -- 1-200 chars
    description TEXT,                       -- 0-2000 chars, nullable
    status TEXT NOT NULL CHECK (status IN ('todo', 'doing', 'blocked', 'done', 'archived')),
    priority TEXT NOT NULL CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    due_at TEXT,                            -- ISO 8601 datetime, nullable
    tags TEXT NOT NULL DEFAULT '[]',        -- JSON array string
    context TEXT NOT NULL CHECK (context IN ('personal', 'professional', 'mixed')),
    workspace TEXT,                         -- 0-100 chars, nullable
    created_at TEXT NOT NULL,               -- ISO 8601 datetime
    updated_at TEXT NOT NULL,               -- ISO 8601 datetime
    completed_at TEXT                       -- ISO 8601 datetime, nullable
);
```

## Field Validation Rules

### Title Field
- **Type**: String (VARCHAR(200))
- **Required**: Yes
- **Constraints**:
  - Minimum length: 1 character
  - Maximum length: 200 characters
  - Must not be empty after trimming whitespace
- **Validation**: `title.strip().length > 0 && title.length <= 200`

### Description Field
- **Type**: String (TEXT)
- **Required**: No (nullable)
- **Constraints**:
  - Maximum length: 2000 characters
  - Supports markdown formatting
  - Empty string treated as NULL
- **Validation**: `description == null || description.length <= 2000`

### Status Field
- **Type**: ENUM
- **Required**: Yes
- **Allowed Values**: `['todo', 'doing', 'blocked', 'done', 'archived']`
- **Default**: `'todo'`
- **Business Rules**:
  - Only `todo`, `doing`, `blocked` can transition to `done`
  - `archived` tasks cannot be modified
  - Setting status to `done` sets `completed_at`
  - Setting status from `done` clears `completed_at`

### Priority Field
- **Type**: ENUM
- **Required**: Yes
- **Allowed Values**: `['low', 'medium', 'high', 'urgent']`
- **Default**: `'medium'`
- **Sort Order**: `urgent > high > medium > low`

### Due Date Field
- **Type**: ISO 8601 DateTime String
- **Required**: No (nullable)
- **Format**: `YYYY-MM-DDTHH:MM:SSZ` (UTC)
- **Validation**: Valid ISO 8601 datetime or NULL

### Tags Field
- **Type**: JSON Array of Strings
- **Required**: No (defaults to empty array)
- **Constraints**:
  - Maximum 10 tags per task
  - Each tag: 1-50 characters
  - Tags are normalized (trimmed, lowercased, deduplicated)
- **Storage**: JSON string in SQLite
- **Validation**:
  ```javascript
  Array.isArray(tags) &&
  tags.length <= 10 &&
  tags.every(tag => typeof tag === 'string' && tag.trim().length > 0 && tag.length <= 50)
  ```

### Context Field
- **Type**: ENUM
- **Required**: Yes
- **Allowed Values**: `['personal', 'professional', 'mixed']`
- **Default**: `'personal'`
- **Description**: Categorizes task by life domain

### Workspace Field
- **Type**: String (VARCHAR(100))
- **Required**: No (nullable)
- **Constraints**:
  - Maximum length: 100 characters
  - Free-form text (no validation)
- **Use Case**: Optional grouping within contexts

### Timestamp Fields
- **created_at**: Set once on creation, never modified
- **updated_at**: Updated on any field change
- **completed_at**: Set when status becomes `done`, cleared otherwise
- **All timestamps**: UTC, microsecond precision, ISO 8601 format

## Data Normalization Rules

### Tag Normalization
1. Trim whitespace from each tag
2. Convert to lowercase
3. Remove empty tags
4. Deduplicate (case-insensitive)
5. Sort alphabetically

**Example**:
```javascript
// Input: ["  WORK  ", "urgent", "WORK", ""]
// Output: ["urgent", "work"]
normalizeTags(["  WORK  ", "urgent", "WORK", ""]) // → ["urgent", "work"]
```

### String Field Normalization
- Trim leading/trailing whitespace
- Convert empty strings to NULL (for optional fields)
- Preserve case (except for tags)

### DateTime Handling
- All timestamps stored as UTC
- Input dates parsed and converted to UTC
- Output dates serialized as ISO 8601 with 'Z' suffix
- NULL values preserved for optional dates

## Database Indexing Strategy

### Primary Key
- `id` (TEXT): UUID v4, primary key, unique

### Performance Indexes
```sql
-- Status filtering (most common query)
CREATE INDEX idx_tasks_status ON tasks(status);

-- Context filtering
CREATE INDEX idx_tasks_context ON tasks(context);

-- Due date queries (today view, overdue detection)
CREATE INDEX idx_tasks_due_at ON tasks(due_at);

-- Update time for sync/poll queries
CREATE INDEX idx_tasks_updated_at ON tasks(updated_at);

-- Priority sorting
CREATE INDEX idx_tasks_priority ON tasks(priority);

-- Composite indexes for common query patterns
CREATE INDEX idx_tasks_status_due_at ON tasks(status, due_at);
CREATE INDEX idx_tasks_context_updated_at ON tasks(context, updated_at);
CREATE INDEX idx_tasks_status_context ON tasks(status, context);
```

### Index Justification
- **Status Index**: Most frequent filter (todo, done, archived views)
- **Due Date Index**: Critical for today/overdue queries
- **Updated At Index**: Sync polling and recent changes
- **Composite Indexes**: Optimize multi-field WHERE clauses
- **No Full-Text**: Tags stored as JSON, FTS not required for v1.0

## Query Patterns and Optimization

### Core Query Patterns
1. **Today View**: `status IN ('todo','doing','blocked') AND due_at BETWEEN today AND tomorrow`
2. **Inbox View**: `status = 'todo' AND due_at IS NULL`
3. **By Context**: `status != 'archived'` grouped by context
4. **By Tag**: `status != 'archived'` with JSON tag filtering
5. **Sync**: `updated_at > last_sync_timestamp`

### Performance Considerations
- JSON tag queries use JSON_EXTRACT for filtering
- Date range queries use indexed datetime fields
- Pagination uses cursor-based approach with indexed fields
- Complex queries limited to avoid performance issues

## Data Migration Strategy

### Version 1.0 (Initial Schema)
- No migrations required (greenfield)
- Schema created on first application run
- Automatic table creation with default values

### Future Migration Approach
```sql
-- Migration table for tracking
CREATE TABLE schema_migrations (
    version TEXT PRIMARY KEY,
    applied_at TEXT NOT NULL,
    description TEXT
);

-- Example migration (adding new field)
ALTER TABLE tasks ADD COLUMN new_field TEXT;
UPDATE schema_migrations SET version = '1.1', applied_at = datetime('now'), description = 'Add new_field';
```

### Migration Principles
- **Additive First**: Add nullable columns, populate defaults
- **Safe Rollback**: Design migrations to be reversible
- **Data Preservation**: Never lose user data
- **Tested**: All migrations tested before deployment
- **Versioned**: Schema version tracked in database

## Data Integrity Constraints

### Database-Level Constraints
```sql
-- Enum constraints via CHECK
status TEXT CHECK (status IN ('todo', 'doing', 'blocked', 'done', 'archived')),
priority TEXT CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
context TEXT CHECK (context IN ('personal', 'professional', 'mixed')),

-- String length constraints
title TEXT NOT NULL CHECK (length(title) BETWEEN 1 AND 200),
description TEXT CHECK (description IS NULL OR length(description) <= 2000),
workspace TEXT CHECK (workspace IS NULL OR length(workspace) <= 100),

-- UUID format validation (application-level)
id TEXT PRIMARY KEY CHECK (length(id) = 36 AND id GLOB '[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]-[0-9a-f][0-9a-f][0-9a-f][0-9a-f]-[0-9a-f][0-9a-f][0-9a-f][0-9a-f]-[0-9a-f][0-9a-f][0-9a-f][0-9a-f]-[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]'),
```

### Application-Level Validation
- Business rule enforcement (status transitions)
- Cross-field validation (completed_at only when status=done)
- Tag normalization and deduplication
- Date format validation and timezone handling

## Export and Import Considerations

### JSON Export Format
- One task per line (JSON Lines format)
- All fields included with proper types
- Timestamps in ISO 8601 format
- Tags as JSON arrays

### CSV Export Format
- Standard CSV with headers
- Tags as comma-separated strings (escaped)
- Dates in ISO 8601 format
- Proper escaping for special characters

### Import Validation
- Full schema validation on import
- Conflict resolution for duplicate IDs
- Data transformation and normalization
- Rollback on validation errors

## Decision Records

### Priority Scheme Decision
**Decision**: Use descriptive enum (`low`, `medium`, `high`, `urgent`) instead of numeric (P0-P4)
**Rationale**:
- More intuitive for users
- Self-documenting code
- Easier to understand in exports
- Aligns with common task management conventions

### Estimate Field Exclusion
**Decision**: Exclude estimate field from v1.0 schema
**Rationale**:
- Complex to implement well (time vs points debate)
- Not core to basic task management
- Can be added in future version
- Keeps initial scope focused

### Tag Storage Decision
**Decision**: Store tags as JSON array in single TEXT column
**Rationale**:
- SQLite JSON support adequate for v1.0 needs
- Simpler than junction table approach
- Easy to query with JSON_EXTRACT
- Maintains data locality

This data model provides a solid foundation for tick-task v1.0 while maintaining flexibility for future enhancements.
