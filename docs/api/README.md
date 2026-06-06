# API Documentation

> SSOT for API contracts. One file per service or major resource group.

---

## Structure

```
api/
  conventions.md     ← shared rules: auth headers, error format, versioning
  [resource].md      ← one file per resource or service
```

---

## conventions.md should cover

- Base URL and versioning strategy
- Authentication method (e.g., Bearer token, API key)
- Standard error response format
- Pagination conventions
- Rate limiting

---

## Per-resource file template

```markdown
# [Resource Name] API

## Endpoints

### GET /[path]
**Purpose:** ...
**Auth:** required / public
**Query params:**
**Response:**
\`\`\`json
{ ... }
\`\`\`

### POST /[path]
**Purpose:** ...
**Request body:**
\`\`\`json
{ ... }
\`\`\`
**Response:**
\`\`\`json
{ ... }
\`\`\`
**Errors:**
| Code | Meaning |
|------|---------|
| 400 | ... |
| 401 | ... |
```
