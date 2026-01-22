# ADR 002: Markdown Rendering with Security Constraints

## Status
Accepted

## Context
Users requested rich text formatting in task descriptions. Need to implement markdown rendering while maintaining security against XSS and other injection attacks.

## Decision
Implement markdown rendering using `react-markdown` with `skipHtml={true}` and URL sanitization.

## Consequences
- ✅ **Rich text formatting** available for users (bold, italic, lists, links)
- ✅ **XSS protection** - HTML execution completely disabled
- ✅ **Safe links** - Only http/https protocols allowed
- ✅ **Controlled feature set** - Only safe markdown elements rendered
- ⚠️ **Limited formatting** compared to full HTML
- ⚠️ **Bundle size increase** due to markdown library

## Alternatives Considered

### Plain Text Only
**Pros:**
- Zero security risk
- Minimal bundle size
- Simple implementation

**Cons:**
- No rich formatting capabilities
- Poor user experience for longer descriptions
- Users demand formatting features

### HTML Rendering with Sanitization
**Pros:**
- Full formatting control
- Familiar HTML/CSS styling

**Cons:**
- High security risk (XSS vulnerabilities)
- Complex sanitization required
- Potential for malicious content execution

### Restricted HTML Subset
**Pros:**
- Balance of functionality and security
- Familiar markup for users

**Cons:**
- Still vulnerable to sophisticated attacks
- Complex whitelist management
- Higher maintenance burden

## Future Considerations
Revisit when:
- User feedback indicates insufficient formatting options
- Security landscape changes (new attack vectors)
- Bundle size becomes critical performance issue

## Implementation Notes
- Use `react-markdown` with `skipHtml={true}`
- Implement custom link component for URL validation
- Style markdown elements with Tailwind classes
- Add `@tailwindcss/typography` for consistent styling
- Test against common XSS payloads
