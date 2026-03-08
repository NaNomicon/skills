# API method reference

Use this when MCP is unavailable or missing needed operations.

## When to prefer API

- Need automation outside current MCP surface
- Need repeatable programmatic workflows
- Need integration with existing CI/admin scripts

## API workflow

1. Confirm Dokploy base URL and auth token
2. Read current resource state
3. Apply minimal mutation
4. Trigger deploy/redeploy when required
5. Verify status, logs, and reachability

## API safety

- Never log raw tokens/secrets
- Keep requests idempotent where possible
- Avoid bulk destructive operations without explicit confirmation
- Treat resource identity (project/env/service IDs) as critical precondition

## Typical operations to map

- Project/resource discovery
- Application source/build/env configuration
- Domain assignment and HTTPS configuration
- Database creation/deploy and app wiring
- Deployment lifecycle actions

## Verification requirements

- Resource reports expected config
- Deployment reaches healthy/running state
- Public domain/path returns expected response
- Dependency connectivity works (e.g., app ↔ database)
