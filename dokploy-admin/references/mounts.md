# Dokploy Mounts & Volumes

## Overview
Dokploy handles volumes and file mounts differently between "Application" and "Compose" service types. Understanding these differences is critical for persistence and configuration management.

## 1. Project Directory Structure (Compose)
For Docker Compose services, Dokploy organizes data on the host as follows:
```
/etc/dokploy/compose/<app-name>/
    /code   # Repository checkout (cleared on AutoDeploy)
    /files  # Managed file mounts (persistent across deployments)
```

## 2. Compose Volume Mapping
When using "File Mounts" in the Dokploy UI for a Compose service, you **must** reference them manually in your `docker-compose.yml` using the relative path `../files/`.
## 2. Compose Volume Mapping
When using "File Mounts" in the Dokploy UI for a Compose service, you **must** reference them manually in your `docker-compose.yml` using the relative path `../files/`.

**Important Linkage**: For Dokploy to correctly link file mounts to a Compose service, the `mount` record in the database must specify `serviceType: "compose"` and provide the correct `composeId`.

**Correct Pattern (Compose `docker-compose.yml`):**
```yaml
services:
  myapp:
    volumes:
      - ../files/config:/app/config # Mount a directory, not a single file
```

**Correct Pattern (Dokploy UI file mount configuration):**
  - **Type**: `file`
  - **Mount Path**: `/app/config` (this is the *container* path, should match `docker-compose.yml` target)
  - **Service Type**: `compose`
  - **Service ID**: `<Your Compose ID>` (e.g., `5u8Q5uRrPwuAcBgWEUbjw`)
  - **File Path**: `config/config.yaml` (this creates a nested file within the Dokploy-managed directory)
  - **Content**: `<your config file content>`

**Common Pitfalls:**
- ❌ `./config.yaml`: Points to the repository checkout, which is cleared on every AutoDeploy.
- ❌ `/absolute/path`: May work but is not portable and bypasses Dokploy management.
- ❌ Mounting `../files/config.yaml` directly as a file bind mount: Often leads to Docker creating a directory instead of a file on the host if the source doesn't exist yet, causing `is a directory` errors in the container.

**Common Pitfalls:**
- ❌ `./config.yaml`: Points to the repository checkout, which is cleared on every AutoDeploy.
- ❌ `/absolute/path`: May work but is not portable and bypasses Dokploy management.

## 3. The "Trailing Slash" Trap
In Dokploy's UI, the `filePath` field determines whether a path is created as a file or a directory on the host.
- `config.json` → Created as a **file** containing the UI-provided content.
- `config/` (or any path ending in `/`) → Created as a **directory**.

**Warning:** If you intended a file but Dokploy/Docker created a directory, your app will crash with `is a directory` errors.

## 4. Troubleshooting "Is a Directory" Errors
If a file mount is unexpectedly mounted as a directory:
1. **Diagnosis**: Check container logs for `failed to read ... is a directory`.
2. **Host Inspection**: SSH to the host and check `/etc/dokploy/compose/<app>/files/<path>`.
3. **Fix**:
   - Delete the bad directory from the host: `rm -rf /etc/dokploy/compose/<app>/files/<path>`.
   - Ensure the UI `filePath` does not have a trailing slash.
   - Trigger a redeploy.

## 5. Network Connectivity (Compose)
Compose services are not always added to `dokploy-network` by default when a domain is attached (Issue #3435).

**Fix**: Explicitly define the network in `docker-compose.yml`:
```yaml
services:
  myapp:
    networks:
      - dokploy-network

networks:
  dokploy-network:
    external: true
    name: dokploy-network
```

## 6. AutoDeploy Safety
When AutoDeploy is enabled:
- **NEVER** rely on files created inside the `./code` or `./` directory at runtime.
- **ALWAYS** move such files to "Advanced -> Mounts" (File Mounts) or use persistent volumes.
- Bind mounts to the host filesystem should target paths outside the project's `/code` directory.

## 7. Known Bugs and Workarounds

### `findMountsByApplicationId` Bug (Dokploy v0.27.1)
**Symptom**: Compose service file mounts are created successfully via the API/UI (and may even materialize on disk), but do not appear in `compose.one`'s `mounts: []` list or in the Dokploy UI under the Compose stack's file mounts.

**Root Cause**: In Dokploy v0.27.1 (and potentially other versions), the `findMountsByApplicationId` function in the Dokploy backend (e.g., `packages/server/src/services/mount.ts`) omits the `compose` service type in its logic. This means that even if mount records with `serviceType=compose` are correctly persisted in the database, the API query used by the UI to *list* mounts for a Compose stack will not retrieve them.

**Workaround**: The mounts are likely correctly persisted in the database, but simply not displayed. Direct UI editability for listing these mounts will be broken until the Dokploy platform is updated. Continue using the "Directory Wrapper" workaround (Section 2) for reliable application startup, but be aware that Dokploy's UI may not show the created mount records.
