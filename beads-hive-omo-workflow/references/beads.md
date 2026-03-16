# Beads / bd — Backend & Fallback CLI Reference

## When to Load This File

Load this file when you need the **raw `bd` CLI**, the `.beads/` backend layout, Dolt-backed issue state, exports, or backend diagnostics.

For the normal agent-facing workflow — claiming work, reservations, messaging, and shared coordination — load `references/beads-village.md` first.

## Where Beads Lives

```
.beads/                   # Committed to git (config.yaml, README.md, hooks/)
.beads/dolt/              # Gitignored — managed by Dolt (the versioned DB)
.beads/.gitignore         # Excludes: dolt/, ephemeral.sqlite3, backup/, .sync.lock
```

`.beads/` skeleton is checked into git. Issue state lives in Dolt, synced separately.

`/.reservations` and `/.mail` belong to the **beads-village runtime layer**, not the raw `bd` backend. See `references/beads-village.md` for those.

---

## Essential bd Commands

Always use `--json` for programmatic use.

```bash
# Session start
bd sync                                          # Sync local Dolt DB
bd ready --json                                  # Show unblocked (no-dep) issues

# Issue management
bd create "Title" -t task -p 2 --json            # Create (types: bug|feature|task|epic|chore)
bd update <id> --claim --json                    # Claim atomically
bd close <id> --reason "Done" --json             # Complete
bd show <id> --json                              # Full issue details

# Dependencies
bd update <id> --deps discovered-from:<parent>   # Link related work

# Backup (JSONL to git — no Dolt remote needed)
bd export -o .beads/issues.jsonl                 # Snapshot issue state to file
git add .beads/issues.jsonl                      # Stage for commit

# Health
bd doctor                                        # Check DB health
```

**Priorities**: 0=Critical, 1=High, 2=Medium (default), 3=Low, 4=Backlog

**Types**: `bug` | `feature` | `task` | `epic` | `chore` | `decision`

**Statuses**: `open` | `in_progress` | `blocked` | `deferred` | `closed`

---

## Comments

Add notes, status updates, or rationale to an issue. Useful for agents to leave decision trails.

```bash
bd comments <id>                          # List all comments (JSON: --json)
bd comments add <id> "text"               # Add a comment
bd comments add <id> -f notes.txt         # Add comment from file
bd comments add <id> "text" --author "Agent-Hive"  # Set explicit author
```

Returns: `{id, issue_id, author, text, created_at}`

Use comments to: record blocked-worker rationale, document decisions, log agent progress notes.

---

## Labels (Tags / Scopes)

Free-form strings, multiple per issue. Primary scoping mechanism for agent role filtering.

```bash
bd create "..." --labels fe,auth,sprint-3    # Assign at creation
bd label add bd-42 backend                   # Add label
bd label remove bd-42 sprint-2               # Remove label
bd label propagate bd-42                     # Push parent labels to all children
bd label list bd-42                          # Labels on one issue
bd label list-all                            # All labels in use across DB
```

Common patterns:
- **Role**: `fe`, `be`, `mobile`, `devops`, `qa` — used by agents to filter `bd ready --label fe`
- **Area**: `auth`, `payments`, `infra`
- **Sprint/milestone**: `sprint-3`, `v1.2`

Agents filter by role label: `bd ready --label fe --json` shows only frontend-tagged ready tasks.

---

## Dependencies & Relationships

### Blocking deps (hard — blocks `bd ready`)

```bash
bd dep bd-xyz --blocks bd-abc        # bd-xyz must close before bd-abc is ready
bd dep add bd-abc bd-xyz             # Same (bd-abc depends on bd-xyz)
bd dep remove bd-abc bd-xyz          # Remove blocking dep
```

A task won't appear in `bd ready` until ALL its blockers are closed.

### Soft relationships (non-blocking)

```bash
bd dep relate bd-abc bd-xyz          # Bidirectional relates_to (no blocking)
bd dep unrelate bd-abc bd-xyz        # Remove relates_to link
```

### Discovery trail

```bash
bd create "..." --deps discovered-from:bd-20   # Audit trail: found while working on bd-20
```

### Visualize

```bash
bd dep tree bd-42                    # Full dependency tree
bd dep list bd-42                    # Direct deps + dependents
bd dep cycles                        # Detect circular dependencies
```

---

## Hierarchy (Epics / Parent-Child)

```bash
bd create "Feature: Auth" -t epic               # Create epic
bd create "Extract JWT" --parent bd-10          # Child of epic
bd children bd-10                               # List children
bd epic bd-10                                   # Epic-specific commands
```

Swarms are structured coordination groups (spawner + fanout/fanin gates):

```bash
bd swarm                             # Swarm management
```

---

## Query Language

Powerful compound filtering — agents use this to find exactly the right tasks:

```bash
bd query "priority<=1 AND label=fe AND status=open"
bd query "type=bug AND created>2026-03-01"
bd query "NOT assignee=none AND status!=closed"
bd query "label=auth OR label=payments"
bd query "title=login"                    # Contains search
bd query "parent=bd-10"                   # All children of epic
```

Supported fields: `status`, `priority`, `type`, `assignee`, `label`, `title`, `description`,
`notes`, `created`, `updated`, `closed`, `id`, `parent`, `pinned`, `ephemeral`

---

## Custom Metadata

Arbitrary key-value on any issue — useful for agent-specific data:

```bash
bd create "..." --metadata '{"team":"platform","sprint":3}'
bd update bd-42 --set-metadata team=platform
bd update bd-42 --set-metadata sprint=3
bd update bd-42 --unset-metadata sprint
```

Queryable: `bd query "metadata.team=platform"`

---

## Scheduling & Estimates

```bash
bd create "..." --due +2w              # Due in 2 weeks
bd create "..." --defer tomorrow       # Hidden from bd ready until tomorrow
bd create "..." --estimate 60          # 60 minute estimate
bd update bd-42 --due "next monday"
bd update bd-42 --defer "2026-04-01"   # Defer until date (clears: --defer "")
```

Deferred issues are invisible to `bd ready` until the date passes.

---

## External References

Link to GitHub Issues, Jira, etc.:

```bash
bd create "..." --external-ref gh-9    # Links to GitHub issue #9
bd create "..." --external-ref jira-ABC-123
bd update bd-42 --external-ref gh-15
```

---

## Issue Creation Conventions

Soft rules — not enforced by bd, but agents should follow them for consistent, queryable issues.

### Priority

| Priority | When to use |
|----------|-------------|
| P0 (0) | Production outage, security hole, data loss |
| P1 (1) | Blocking a release, major UX broken, critical path |
| P2 (2) | Normal feature work, planned improvements (default) |
| P3 (3) | Nice-to-have, cleanup, refactor with no deadline |
| P4 (4) | Backlog — no timeline, future consideration |

When in doubt, use P2. Agents should NOT self-escalate to P0/P1 without clear justification.

### Labels / Tags

Every issue SHOULD have:
1. **Role label** — at least one of: `fe`, `be`, `mobile`, `devops`, `qa` (enables `bd ready --label <role>`)
2. **Area label** — domain scoping: `auth`, `payments`, `infra`, `api`, etc. (optional but useful)
3. **Sprint/milestone** — if known: `sprint-3`, `v1.2` (add when planning, propagate from epic)

After setting labels on an epic: `bd label propagate <epic-id>` pushes labels to all children.

### Hierarchy

| Issue type | MUST | MUST NOT |
|------------|------|----------|
| `epic` | `--acceptance "..."` (done criteria) | `--parent` |
| `task` (under epic) | `--parent <epic-id>` | Create without parent if epic exists |
| `bug` | `--description` (steps to repro) | — |
| Discovered sub-task | `--deps discovered-from:<current-id>` | — |

Rule: if a Hive feature exists, create a matching `epic` and parent all tasks under it.

### Dependencies

| Dep type | When | Command |
|----------|------|---------|
| `blocks` | B cannot start until A finishes (hard gate) | `bd dep bd-A --blocks bd-B` |
| `discovered-from` | Found while working on another task | `--deps discovered-from:bd-A` at create time |
| `relates_to` | Informational, non-blocking | `bd dep relate bd-A bd-B` |
| `waits-for` | Fanout gate (swarm pattern) | `--waits-for <spawner-id>` |

Don't over-block — only add `blocks` deps when parallelism would cause real conflicts.

### Metadata

Use `--metadata` / `--set-metadata` for structured data agents and queries need:

```bash
bd create "..." --metadata '{"team":"platform","sprint":3,"hive-feature":"user-auth"}'
bd update bd-42 --set-metadata pr=123          # Link PR when created
bd update bd-42 --set-metadata github-issue=9  # Also use --external-ref gh-9
```

Recommended keys (conventions, not required):
- `team` — owning team (`platform`, `growth`, `infra`)
- `sprint` — sprint number (integer)
- `hive-feature` — matching Hive feature name (links bd issue ↔ .hive/features/<name>)
- `pr` — PR number once opened
- `github-issue` — GH issue number (supplement to `--external-ref gh-N`)

All metadata fields are queryable: `bd query "metadata.team=platform"`

### GitHub Issue ↔ Beads Sync (Convention)

No automated sync exists — this is a manual hand-off:

1. Human opens GH Issue #N
2. Agent creates bd task: `bd create "..." --external-ref gh-N --set-metadata github-issue=N`
3. Agent works, opens PR with `Closes #N` in body
4. Agent closes bd task: `bd close <id>`

The `--external-ref gh-N` is the canonical link. Always set it when a GH issue exists.

---

## Raw CLI Task Selection Patterns

Use these patterns only when you are operating directly on raw `bd` without the beads-village MCP layer.

```bash
# All ready tasks for my role
bd ready --label be --json

# Critical tasks first
bd query "priority=0 AND status=open" --json

# Ready tasks I previously started
bd query "assignee=me AND status=in_progress" --json

# What's blocking a specific task
bd dep list bd-42 --json

# Ready tasks in an epic
bd ready --json | jq '[.[] | select(.parent == "bd-10")]'

# Find duplicate/similar issues before creating
bd find-duplicates "title of new issue"
```

Raw CLI equivalent of the normal beads-village claim flow: `bd ready --json` → pick by priority+label → `bd update <id> --claim` → work → `bd close <id>`

---

## Raw CLI Fallback Workflow

When the MCP layer is unavailable and you must work directly against the backend:

1. `bd ready --json` → pick unblocked issue
2. `bd update <id> --claim` → claim (atomic)
3. Work on it
4. Found new work? → `bd create "Title" -p N --deps discovered-from:<id>`
5. `bd close <id> --reason "Done"`

Rules:
- ✅ Always use `--json` for scripting
- ✅ Link discovered work with `discovered-from` deps
- ❌ Do NOT create markdown TODO lists for project tracking
- ❌ Do NOT use two tracking systems in parallel

---

## Multi-Dev Sync

- Dolt syncs **issue state** across developers (`bd sync` = dolt pull + push)
- Reservations are handled by the **beads-village** coordination layer (same-machine/workspace runtime)
- Cross-machine file conflicts are normal git merge territory — Beads doesn't solve those

### Fallback session start
```bash
bd sync                  # Get latest issues from team
bd ready --json          # Pick unblocked work
```

### Fallback session end
```bash
bd close <id>                              # Mark complete
bd export -o .beads/issues.jsonl           # Snapshot issue state
git add .beads/issues.jsonl
git pull --rebase && git commit -m 'chore(beads): sync issues' && git push
```

---

## Session Completion Ritual (Landing the Plane)

Fallback/backend ritual when you are operating directly on raw `bd` state:

Work is NOT done until `git push` succeeds:

1. `bd create` for any remaining/discovered issues
2. Run quality gates (tests, linters)
3. `bd close <id>` for completed work
4. `bd export -o .beads/issues.jsonl && git add .beads/issues.jsonl`
5. `git pull --rebase && git commit -m 'chore(beads): sync issues' && git push`

In the normal beads-village-first workflow, prefer `beads-village_done(...)` / `beads-village_sync()` and only drop to this raw CLI path when you explicitly need backend fallback.
