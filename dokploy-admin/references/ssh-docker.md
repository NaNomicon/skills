# SSH + Docker method reference

This is the infrastructure fallback. Use when Dokploy-level tools cannot explain runtime behavior.

## Enter this layer when

- Dashboard reports healthy but domain/runtime behavior is failing
- You need container/network/port/Traefik runtime truth
- You need Swarm task/node/placement diagnostics
- You need host-level firewall or SSH-security validation

Avoid using SSH/Docker for ordinary CRUD operations that MCP/API/CLI can handle safely.

## Read-first commands

Start with read-only inspection:

```bash
docker ps
docker service ls
docker service ps <service>
docker logs --tail 100 <container>
docker inspect <container-or-service>
docker network inspect <network>
docker volume ls
docker stats --no-stream
```

For Traefik-heavy incidents, inspect router/service mapping from Traefik runtime or config where available.

## Common diagnosis patterns

### 502 from domain

Likely causes:

- Backend unhealthy or crash-looping
- Traefik points to wrong internal port
- Route points to wrong service/container
- App binds only localhost inside container

Check:

1. Backend container logs
2. Actual listening port in container
3. Traefik router/service mapping
4. Network attachment between Traefik and backend

### 404 from domain

Likely causes:

- Wrong host rule
- Wrong path rule
- Missing/stale Traefik label or file-provider config
- HTTPS entrypoint mismatch

Check DNS, route rules, and whether the correct router is loaded.

### Swarm service instability

Likely causes:

- Image pull/auth failures on some nodes
- Missing registry auth with replicas
- Node-specific volume/path assumptions
- Resource pressure or bad placement constraints

Check:

```bash
docker service ps <service>
docker node ls
docker inspect <task-or-service>
```

### Data disappears after redeploy

Likely causes:

- Writes to ephemeral container filesystem
- Config stored in non-persistent checkout path
- Wrong mount type for workload durability

Verify mounts with `docker inspect` and compare against intended Dokploy persistence model.

## Security notes

- Docker-published ports may bypass plain-UFW assumptions due to Docker iptables behavior
- Prefer provider firewalls or `ufw-docker` if direct host ports must be exposed
- Prefer Traefik-managed HTTP(S) over direct host-port exposure
- Prefer key-based SSH and least privilege

## Mutation discipline

If host mutation is unavoidable:

1. State the exact failure
2. State the exact minimal host change required
3. Apply the smallest possible fix
4. Re-verify from both infrastructure and application perspective

Do not make broad host changes when root cause is application configuration.
