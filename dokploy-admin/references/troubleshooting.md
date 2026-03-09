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

1. Inspect actual mounts (ensure Type is 'bind' or 'volume' as intended)
2. Confirm data path is persistent (named volume or intentional bind mount)
3. Avoid relying on repository checkout paths for durable state
4. Redeploy and verify persistence with a write/read test
5. Check for "ghost directories": if a bind-mount source is missing on host, Docker may create an empty directory at that path.
2. Confirm data path is persistent (named volume or intentional bind mount)
3. Avoid relying on repository checkout paths for durable state
4. Redeploy and verify persistence with a write/read test

## 5) Works on one node, fails on others

1. Inspect `docker service ps` distribution
2. Validate image pull/auth on all nodes
3. Validate volume/path assumptions per node
4. Re-check placement constraints and networking
## 6) App crashes with \"is a directory\" for a config file mount

1. **Symptom**: Deployment succeeded in UI, but container logs show "failed to read config file: ... is a directory".
2. **Diagnosis**: Dokploy (or Docker) created the host source path as a directory instead of a file. This is a known issue where empty source paths trigger automatic directory creation before the file is materialized.
3. **Investigation**:
   - Verify the path type on the host with: `ls -ld /path/to/source`
   - If `ls -ld` shows a directory (starts with `d`), you have found the cause.
4. **Resolution**:
   - SSH/Docker to the host.
   - Remove the bad directory from host: `rm -rf /etc/dokploy/compose/<app>/files/<config-file>`
   - Ensure `filePath` in Dokploy UI does NOT have a trailing slash.
   - If the bug persists, switch to the \"Directory Mount\" workaround (see `references/mounts.md`) to avoid single-file bind mount limitations.

1. Symptom: Deployment succeeded in UI, but container logs show "failed to read config file: ... is a directory".
2. Diagnosis: Dokploy or Docker created the source path as a directory instead of a file.
3. Escalation: SSH/Docker to inspect host path.
4. Resolution:
   - Remove the bad directory from host: `rm -rf /etc/dokploy/compose/<app>/files/<config-file>`
   - Ensure `filePath` in Dokploy UI does NOT have a trailing slash.
   - If bug persists, use "Directory Mount" workaround (see `references/mounts.md`).
