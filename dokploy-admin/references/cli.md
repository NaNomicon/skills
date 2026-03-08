# CLI method reference

Use only when Dokploy CLI is already present and authenticated.

## When CLI is appropriate

- Existing admin workflow is terminal-first
- Environment already has stable CLI setup
- CLI path is simpler than hand-built API calls

## Preconditions

- Verify CLI exists and is authenticated
- Confirm target environment/project context
- Confirm command supports requested operation

## CLI workflow

1. Inspect/list current resources
2. Apply minimal configuration changes
3. Trigger deploy/redeploy if needed
4. Re-check state and logs
5. Validate external reachability

## CLI safety

- Don’t assume CLI availability; verify first
- Avoid command chains that hide failures
- Prefer explicit commands over ambiguous shortcuts
- Keep secrets out of shell history/output

## Escalation rule

If CLI output is insufficient or contradicts runtime behavior, move to MCP/API reads or SSH/Docker diagnostics as needed.
