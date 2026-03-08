# MCP method reference

Use this as the default control plane for Dokploy operations.

## Best-fit tasks

- Create/list/update projects and environments
- Create/configure/deploy/redeploy applications
- Create/deploy/start/stop databases
- Create/update/validate domains
- Update build/source/env settings

## Canonical MCP workflow

1. Inspect existing project/environment/resource
2. Create missing resource
3. Configure source/build/env/domain
4. Deploy or redeploy
5. Verify monitoring/logs/reachability

## Representative MCP operations

- Projects: `dokploy-mcp_project-all`, `dokploy-mcp_project-one`, `dokploy-mcp_project-create`
- Apps: `dokploy-mcp_application-create`, `dokploy-mcp_application-one`, `dokploy-mcp_application-saveBuildType`, `dokploy-mcp_application-saveEnvironment`, `dokploy-mcp_application-deploy`, `dokploy-mcp_application-redeploy`
- Databases: `dokploy-mcp_postgres-create`, `dokploy-mcp_postgres-deploy`, `dokploy-mcp_mysql-create`, `dokploy-mcp_mysql-deploy`
- Domains: `dokploy-mcp_domain-create`, `dokploy-mcp_domain-update`, `dokploy-mcp_domain-validateDomain`, `dokploy-mcp_domain-byApplicationId`

## MCP safety rules

- Always read current state first
- Confirm IDs before write operations
- Use smallest mutation possible
- Verify with monitoring/logs plus real reachability
