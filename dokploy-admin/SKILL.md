---
name: dokploy-admin
description: Use for Dokploy deployment, operations, and troubleshooting across MCP, API, CLI, and SSH/Docker. Select the safest effective control plane, apply minimal changes, and verify real runtime outcomes.
compatibility: Requires Dokploy MCP tools and optionally bash/ssh/docker/gh/web access when MCP is unavailable or insufficient.
---

# Dokploy Admin

This skill is for operating Dokploy with the right control plane:

1. **MCP first** (default)
2. **API second** (automation/programmatic fallback)
3. **CLI third** (when CLI is already installed and authenticated)
4. **SSH + Docker last** (infrastructure fallback)

## Primary outcomes

- Deploy and redeploy applications safely
- Configure databases, domains, variables, and compose stacks
- Troubleshoot 404/502, unhealthy deployments, and persistence issues
- Verify *actual* runtime health, not just dashboard state

## Control-plane decision matrix

Use the first option that cleanly solves the task.

| Situation | Best method | Why |
|---|---|---|
| Create/update projects, apps, DBs, domains | MCP | Structured, safest, least error-prone |
| Need scripted integration not covered by MCP | API | Full programmatic control |
| Team already uses authenticated Dokploy CLI | CLI | Fast terminal operations in known environments |
| Panel state conflicts with runtime reality | SSH/Docker | Required for container/network/Traefik truth |
| DNS/Traefik/Swarm node-level anomalies | SSH/Docker | Host-level inspection needed |
| MCP/API behavior is ambiguous or buggy | Source Analysis | Use `librarian`/`explore` to find implementation truth |
| DNS/Traefik/Swarm node-level anomalies | SSH/Docker | Host-level inspection needed |

## Operating rules

1. Inspect current state before mutating
2. Confirm target project/environment/resource IDs before edits
3. Prefer Traefik domains over direct host-port exposure
4. Treat rebuild/delete/volume-destructive actions as high-risk
5. Never claim success without verification (logs + reachability + health)

## Standard workflow

1. **Clarify target topology**
   - project/environment/service type
   - source/build type
   - domain vs direct port intent
   - persistence requirements
2. **Inspect state** with lowest-risk method available
3. **Apply minimal correct mutation**
4. **Verify outcome** against user goal
5. **Report residual risk / next step**

## Method-specific references

- `references/mcp.md` — canonical MCP workflows and operations
- `references/api.md` — API fallback patterns and safety
- `references/cli.md` — CLI usage patterns and guardrails
- `references/ssh-docker.md` — host/runtime fallback diagnostics
- `references/troubleshooting.md` — symptom → diagnosis playbooks
- `references/mounts.md` — mounts, volumes, and persistence guide
- `references/dokploy-workflows.md` — consolidated workflow guide
- `references/source-notes.md` — distilled rationale and source constraints
- `references/dokploy-workflows.md` — consolidated workflow guide
- `references/source-notes.md` — distilled rationale and source constraints

## Reference routing quick-map

- **Provision/update via Dokploy resources** → start with `references/mcp.md`
- **MCP unavailable or missing operation** → use `references/api.md`
- **CLI-first environment already configured** → use `references/cli.md`
- **Runtime truth needed (Traefik/container/network/host)** → use `references/ssh-docker.md`
- **Symptom-led incident handling (502/404/crash/persistence)** → use `references/troubleshooting.md`
- **Background rationale and source constraints** → use `references/source-notes.md`

## Response format for substantial tasks

1. Goal
2. Method chosen (MCP/API/CLI/SSH) + why
3. Actions taken
4. Verification evidence
5. Risks / follow-up

## Boundaries

- Don’t invent Dokploy IDs/resources/fields
- Don’t jump to SSH before exhausting safer Dokploy-level inspection (unless clearly infra-level)
- Don’t expose secrets in logs or summaries
- Don’t treat "deploy started" as "deploy succeeded"
