## Source Code Analysis

When troubleshooting complex platform behavior or when official documentation is sparse/outdated, direct source code analysis of an open-source platform can provide the ultimate truth.

### Official Sources & Repositories
- **Dokploy Repository**: [https://github.com/Dokploy/dokploy](https://github.com/Dokploy/dokploy)
- **Dokploy MCP Server**: [https://github.com/Dokploy/mcp](https://github.com/Dokploy/mcp) (Official MCP interface for programmatic management)
- **Core Modules for File/Mount Analysis**:
  - [Mount Service](https://github.com/Dokploy/dokploy/blob/canary/packages/server/src/services/mount.ts)
  - [Docker Utils](https://github.com/Dokploy/dokploy/blob/canary/packages/server/src/utils/docker/utils.ts)
  - [Traefik Setup](https://github.com/Dokploy/dokploy/blob/canary/packages/server/src/setup/traefik-setup.ts)

## When to Use

When troubleshooting complex platform behavior or when official documentation is sparse/outdated, direct source code analysis of an open-source platform can provide the ultimate truth.

## When to Use

-   **Discrepancies**: Observed live behavior contradicts official documentation or API responses.
-   **Missing Features**: A feature is expected but undocumented or not present in tools.
-   **Deep Bugs**: Persistent issues where higher-level diagnostics (logs, metrics, API responses) are misleading or insufficient.
-   **API Probing**: Understanding internal API schemas, required fields, and linkage mechanisms.

## Approach

1.  **Locate Source Repository**: Identify the official (or relevant fork) source code repository.
2.  **Clone Locally**: If possible, clone the repository to enable full-text search, AST analysis, and detailed reading.
3.  **Inspect Live Container**: For running services, `docker exec <container-id> <shell-command>` can be used to inspect live source files (if present), compiled code, or runtime configuration.
    *   Use `ls -Rla /app` (or similar) to find source paths.
    *   Use `grep -R "keyword" /app` to search for code patterns.
    *   Use `node -e "fs.readFileSync(...).slice(...)"` to read specific snippets of JavaScript/TypeScript files in a running Node.js container.
4.  **Focus Areas**:
    *   **API Routers/Services**: Look for files defining API endpoints (e.g., `mounts.ts`, `compose.ts`, `mounts-router.ts`). These define input schemas (Zod/TRPC types) and business logic.
    *   **Database Schema**: Inspect `schema.ts` (or equivalent) files to understand table structures, column names (including `camelCase` vs. `snake_case`), and foreign key linkages (e.g., `composeId`, `applicationId`, `serviceType`).
    *   **Utility Functions**: Identify helper functions that perform core logic like file creation, path resolution, or remote execution (e.g., `utils.ts`, `mount.ts`).
5.  **Probing Unknown Schemas**: If API schemas are not explicitly documented, use intentionally malformed requests (e.g., empty JSON `{}`) against mutation endpoints to trigger detailed error messages (like Zod errors) that reveal required fields and expected types.
6.  **Database Inspection (Postgres Example)**:
    *   Connect to the database container: `docker exec <postgres-container-id> psql -U <user> -d <db>`
    *   List tables: `\dt`
    *   Describe table schema: `\d <table-name>`
    *   Query data (use double quotes for camelCase column names):
        ```sql
        SELECT "mountId", "type", "mountPath", "filePath", "serviceType", "composeId", "applicationId"
        FROM mount
        WHERE "composeId" = 'YOUR_COMPOSE_ID';
        ```
7.  **Verification**: Always cross-reference source code findings with live system behavior (logs, container mounts, host files) and database state.

## Watch Out For

-   **Version Mismatches**: Live server code might differ from the latest `main` branch in the source repository. Prioritize live container inspection for immediate issues.
-   **Compiled vs. Source**: In Node.js/TypeScript apps, `dist/` or `lib/` directories contain compiled JavaScript. Source is usually `src/`.
-   **Authorization**: Internal API endpoints might require specific headers (e.g., `x-api-key`) or JWT tokens. Inspect network traffic from the UI or check platform environment variables/secrets.
-   **Side Effects**: Be cautious when probing mutation endpoints. Always have a rollback plan or perform read-only checks first.
