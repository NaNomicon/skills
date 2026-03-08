# Troubleshooting playbook

Follow symptom → diagnosis, escalating control planes safely.

## 1) App marked running, domain returns 502

1. MCP/API/CLI: inspect deployment status, app logs, domain config
2. Confirm internal container port expected by Traefik
3. If unresolved, SSH/Docker:
   - container health/logs
   - Traefik router/service mapping
   - network attachment between Traefik and backend

## 2) Domain returns 404

1. Verify DNS points to correct Dokploy host
2. Verify host/path rules and HTTPS mode
3. Confirm correct app/compose domain binding
4. For Compose, ensure redeploy occurred after label/domain changes

## 3) Deployment succeeds but app unhealthy/crashing

1. Inspect startup logs for missing env/dependency
2. Validate source/build path and runtime command
3. Validate secret/env wiring and service dependencies
4. Check resource limits/placement constraints if Swarm involved

## 4) Data/config lost after redeploy

1. Inspect actual mounts
2. Confirm data path is persistent (named volume or intentional bind mount)
3. Avoid relying on repository checkout paths for durable state
4. Redeploy and verify persistence with a write/read test

## 5) Works on one node, fails on others

1. Inspect `docker service ps` distribution
2. Validate image pull/auth on all nodes
3. Validate volume/path assumptions per node
4. Re-check placement constraints and networking
