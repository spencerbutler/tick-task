# UX/UI Specification (v1.0)

## Design Philosophy
FIN-tasks embraces a **keyboard-first, productivity-focused** design philosophy. The interface prioritizes speed and efficiency while maintaining visual clarity and professional aesthetics suitable for both personal and professional task management.

## Core Design Principles
- **Minimalism**: Clean, uncluttered interface focused on content
- **Speed**: Fast interactions, keyboard shortcuts for power users
- **Reliability**: Consistent behavior, clear feedback, error prevention
- **Accessibility**: WCAG 2.1 AA compliant, keyboard navigable
- **Responsiveness**: Works on desktop (1024px+), optimized for productivity workflows

## Visual Design System

### Typography
- **Primary Font**: System font stack (Segoe UI, -apple-system, Roboto, sans-serif)
- **Hierarchy**:
  - H1: 24px, 600 weight (page titles)
  - H2: 20px, 600 weight (section headers)
  - Body: 14px, 400 weight (task content)
  - Small: 12px, 400 weight (metadata, timestamps)
- **Line Height**: 1.5 for readability
- **Color**: High contrast text on neutral backgrounds

### Spacing & Layout
- **Grid**: 8px base unit system
- **Page Margins**: 24px (3x base)
- **Section Spacing**: 16px (2x base)
- **Component Spacing**: 8px (1x base)
- **Content Width**: Max 1200px, centered layout

### Color Scheme
- **Primary**: Professional blue (#2563eb) for actions, links
- **Success**: Green (#16a34a) for completed states
- **Warning**: Orange (#ea580c) for due dates, blocked states
- **Error**: Red (#dc2626) for errors, urgent priority
- **Neutral**: Gray scale (#6b7280 for text, #f3f4f6 for backgrounds)

### Dark Mode
- **Decision**: System preference detection with manual override
- **Implementation**: CSS custom properties for seamless switching
- **Contrast**: Maintained WCAG AA ratios in both modes

## Required Views & Navigation

### Primary Navigation
Top-level navigation between four core views:
1. **Today** - Time-sensitive tasks due today
2. **Inbox** - New tasks without due dates
3. **Contexts** - Tasks grouped by context (personal/professional/mixed)
4. **Tags** - Tasks grouped by tags

### Today View (/)
- **Purpose**: Focus on time-sensitive work
- **Content**: Tasks due today + overdue, grouped by status
- **Layout**: Priority-ordered list with due time indicators
- **Empty State**: "No tasks due today. Great job!" with quick add CTA

### Inbox View (/inbox)
- **Purpose**: Capture and triage new tasks
- **Content**: Tasks with status=todo and no due_date
- **Layout**: Chronological list (newest first)
- **Actions**: Quick triage (set due date, add tags, change context)

### Contexts View (/contexts)
- **Purpose**: Work/life balance management
- **Content**: All active tasks grouped by context
- **Layout**: Three columns (Personal | Professional | Mixed)
- **Interactions**: Drag between contexts, context-specific filtering

### Tags View (/tags)
- **Purpose**: Topic-based organization
- **Content**: Tasks grouped by tags (tasks can appear in multiple groups)
- **Layout**: Tag cloud with expandable sections
- **Interactions**: Tag management, bulk operations

### Task Detail/Edit Modal
- **Purpose**: Comprehensive task management
- **Layout**: Two-column layout (content | metadata)
- **Fields**: Title, description (markdown), priority, due date, tags, context, workspace
- **Actions**: Save, cancel, delete, archive

## User Flows

### Task Creation Flow
1. **Quick Add**: Global shortcut (Ctrl/Cmd+N) opens mini modal
2. **Title Input**: Auto-focus, enter to save with defaults
3. **Smart Parsing**: "Task title #tag @context !priority" syntax
4. **Success Feedback**: Toast notification with link to edit

### Task Completion Flow
1. **Quick Complete**: Checkbox or keyboard shortcut (Space/X)
2. **Status Update**: Visual feedback, celebration animation
3. **Today View Update**: Automatic removal from view
4. **Streak Tracking**: Optional progress indicator

### Task Editing Flow
1. **Inline Edit**: Double-click title for quick edits
2. **Modal Edit**: Click anywhere else for full editor
3. **Auto-save**: Draft state with manual save option
4. **Validation**: Real-time feedback for invalid inputs

## Keyboard Shortcuts (Minimal Set)

### Global Shortcuts
- `Ctrl/Cmd+N`: New task
- `Ctrl/Cmd+K`: Focus search/filter
- `Ctrl/Cmd+1-4`: Switch between views (1=Today, 2=Inbox, 3=Contexts, 4=Tags)
- `Ctrl/Cmd+,`: Open settings
- `?`: Show shortcuts help

### Task List Shortcuts
- `↑/↓`: Navigate tasks
- `Enter`: Open task detail
- `Space`: Toggle complete (todo ↔ done)
- `E`: Edit task
- `Delete/Backspace`: Archive task
- `T`: Add/edit tags
- `D`: Set due date
- `P`: Change priority

### Modal Shortcuts
- `Esc`: Close modal
- `Ctrl/Cmd+Enter`: Save and close
- `Ctrl/Cmd+Delete`: Delete and close

## Component Specifications

### Task Item Component
- **Layout**: Checkbox + title + metadata row
- **States**: Normal, hover, selected, completed, overdue
- **Metadata**: Due date, priority indicator, tags, context badge
- **Actions**: Complete, edit, delete (on hover/selection)

### Filter Bar Component
- **Position**: Top of each view
- **Controls**: Text search, status filter, priority filter, date range
- **Behavior**: Real-time filtering, URL state persistence

### Status Indicators
- **Todo**: Empty checkbox
- **Doing**: Filled checkbox with progress indicator
- **Blocked**: Checkbox with warning icon
- **Done**: Checkmark with strikethrough text
- **Archived**: Hidden from normal views

## Responsive Design
- **Breakpoint**: 1024px minimum width
- **Mobile**: Graceful degradation with horizontal scroll
- **Touch**: Touch-friendly targets (44px minimum)
- **Focus**: Visible focus rings for keyboard navigation

## Loading & Error States
- **Skeleton Loading**: Content-shaped placeholders during load
- **Error Boundaries**: User-friendly error messages with recovery options
- **Offline Indicator**: Banner when API unavailable
- **Retry Mechanisms**: Automatic retry for failed operations

## Accessibility Checklist (WCAG 2.1 AA)

### Keyboard Navigation
- [ ] All interactive elements reachable via Tab
- [ ] Logical tab order matches visual layout
- [ ] Keyboard shortcuts don't interfere with screen readers
- [ ] Focus indicators visible and high contrast
- [ ] Modal dialogs trap focus appropriately

### Screen Reader Support
- [ ] Semantic HTML structure (<main>, <nav>, <section>)
- [ ] ARIA labels on complex widgets
- [ ] Live regions for dynamic content updates
- [ ] Form fields have associated labels
- [ ] Images have alt text (icons described)

### Color & Contrast
- [ ] Text contrast ratio ≥ 4.5:1 (normal text)
- [ ] Text contrast ratio ≥ 3:1 (large text)
- [ ] Color not used as only indicator of state
- [ ] Focus indicators meet contrast requirements
- [ ] Error states clearly distinguishable

### Content & Media
- [ ] Text can be resized to 200% without loss
- [ ] Content readable when zoomed to 200%
- [ ] No horizontal scrolling at 320px width
- [ ] Multimedia content has text alternatives
- [ ] Animations can be disabled (prefers-reduced-motion)

### Forms & Controls
- [ ] Form fields have visible labels
- [ ] Required fields clearly indicated
- [ ] Error messages associated with inputs
- [ ] Form validation provides helpful feedback
- [ ] Custom controls have ARIA attributes

## Implementation Notes
- **Framework**: React with TypeScript for type safety
- **Styling**: Tailwind CSS for utility-first approach
- **State**: Local component state with optimistic updates
- **Persistence**: API calls with error handling and retry logic
- **Testing**: Component tests for accessibility compliance
