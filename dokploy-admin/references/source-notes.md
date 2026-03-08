# Source notes for this skill

This file records the core ideas the skill is built on.

## From local vault notes

- Dokploy administration benefits from a safety-first flow: inspect before mutating, use explicit IDs, avoid destructive operations without strong justification.
- Traefik is central to external HTTP routing; direct port exposure should be the exception, not the default.
- SSH and Docker are valuable for runtime-truth debugging when panel state is insufficient.
- Swarm/node placement, persistence strategy, and routing details are recurring failure points.

## From Dokploy docs

- Dokploy is a self-hosted PaaS built around Docker and Traefik.
- Applications, databases, variables, domains, and compose stacks are first-class management areas.
- Application domains hot-reload through Traefik file-provider behavior.
- Docker Compose domains require redeploy because labels are consumed at deploy time.
- Compose variables from the UI become `.env`, but must still be explicitly referenced or loaded.
- Named volumes are recommended when Dokploy backup support matters.
- Docker’s iptables behavior means UFW alone is not sufficient mental protection for published ports.

## From Dokploy MCP docs

- MCP covers most routine operational workflows for projects, applications, databases, and domains.
- Typical real workflows are multi-step: create → configure → deploy → verify.
- Database resources often require explicit deploy actions after creation.

## From Docker docs

- Compose behavior must be reasoned about in terms of services, networks, volumes, env injection, and deploy semantics.
- Stack-mode / Swarm constraints differ from ordinary local compose assumptions.

## Skill design implications

- The skill should strongly bias toward MCP first, because structured management reduces operational risk.
- The skill should still teach when to drop to API, CLI, or SSH/docker instead of pretending one control plane solves everything.
- Verification must be operational, not ceremonial. “Deploy started” is not success.
