# Deployment Documentation

> SSOT for environments, CI/CD pipelines, and operational runbooks.

---

## Files to create here

```
deployment/
  environments.md    ← dev / staging / prod: URLs, configs, access
  local.md           ← how to run the project locally
  ci-cd.md           ← pipeline overview, how to trigger deploys
  runbooks/          ← step-by-step ops procedures
    rollback.md
    db-migration.md
    incident.md
```

---

## environments.md template

```markdown
## Environments

| Env | URL | Database | Notes |
|-----|-----|----------|-------|
| local | localhost:3000 | local postgres | |
| staging | staging.example.com | staging-db | auto-deploys from `main` |
| production | example.com | prod-db | manual deploy via CI |

## Access
- Staging: [how to get access]
- Production: [who has access, how to request]
```

---

## local.md must include

1. Prerequisites (runtime versions, tools)
2. Environment variables needed (reference `.env.example`)
3. Database setup commands
4. How to run tests
5. Common local issues and fixes
