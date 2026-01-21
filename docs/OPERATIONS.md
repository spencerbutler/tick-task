# Operations (v0)

## Run modes
- Dev
- Local production (single machine)
- Optional LAN (explicit)

## Configuration
- Port
- Data path
- LAN enable + token (if enabled)

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

