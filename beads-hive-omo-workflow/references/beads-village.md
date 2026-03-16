# beads-village — MCP Coordination Reference

## When to Load This File

Load this file for the **normal agent-facing workflow**:

- joining the workspace/team
- claiming or creating shared work
- reserving files before edit
- messaging teammates or other agents
- completing work and syncing state
- inspecting live coordination state, priorities, or dashboards

In this environment, beads-village runs over the **Beads / `bd` backend**. If you need raw CLI fallback, Dolt details, or direct backend maintenance, load `references/beads.md`.

---

## What beads-village Owns

beads-village is the **primary coordination surface** for this workflow.

| Concern | beads-village responsibility |
|---------|------------------------------|
| Agent/workspace join | Register agent identity, role, workspace, team |
| Shared task state | List ready work, claim work, add work, complete work |
| Reservations | Lock and release files for active work |
| Communication | Team messaging and inbox |
| Operational visibility | Workspace status, priorities, insights, dashboards |
| Backend bridge | Uses Beads / `bd` underneath when configured |

Rule of thumb: **Claim in beads-village, execute in Hive or OMO, reserve through beads-village.**

---

## Session Entry

`beads-village_init(...)` is the required entry point.

```python
beads-village_init(role="be", team="default")
```

Important options:

- `role`: `fe`, `be`, `mobile`, `devops`, `qa`
- `team`: logical team name (default: `default`)
- `leader=true`: enables assignment/coordinator behavior
- `start_tui=true`: if leader, auto-launch the dashboard TUI

Typical session start:

```python
beads-village_init(role="be", team="default")
beads-village_status(include_bv=true)
beads-village_ls(status="ready")
beads-village_claim()
```

Use `beads-village_status(include_agents=true, include_bv=true)` when you need the broader workspace/team picture.

---

## Core Task Lifecycle

### 1. Inspect or create work

```python
beads-village_ls(status="ready")
beads-village_show(id="bd-42")
beads-village_add(title="Implement auth middleware", typ="task", pri=2, tags=["be", "auth"])
```

Use `beads-village_add(...)` when the shared work item does not exist yet.

### 2. Claim work

```python
beads-village_claim()
```

`claim()`:

- auto-syncs first
- filters by role if one was set at init
- claims the next ready task
- marks it `in_progress`

If you are coordinating work for others, use `beads-village_assign(id="bd-42", role="fe")`.

### 3. Reserve files before edit

```python
beads-village_reservations()
beads-village_reserve(paths=["src/auth/middleware.ts"], reason="implementing JWT middleware", ttl=600)
```

**Iron law:** reserve before edit. Release when done or when pausing.

### 4. Execute in Hive or OMO

- **Hive** for feature plans, worktrees, batched task execution
- **OMO `task()`** for one-shot research or focused changes

beads-village does **not** replace Hive planning or OMO delegation. It owns the coordination layer around them.

### 5. Release if pausing or blocked

```python
beads-village_release(paths=["src/auth/middleware.ts"])
beads-village_msg(subj="Blocked: auth dependency unresolved", to="all", importance="high")
```

There is no dedicated `beads-village_block(...)` tool in the current surface. If a Hive worker is blocked, pair the release/message step with:

```python
hive_worktree_commit(status="blocked", blocker={...})
```

### 6. Complete work

```python
beads-village_done(id="bd-42", msg="Completed auth middleware")
```

`done(...)` is the canonical completion step for shared task state. It auto-releases files and syncs.

Use explicit `beads-village_sync()` when you need an extra sync outside the normal completion path.

---

## Essential Tool Surface

### Membership and overview

| Tool | Purpose |
|------|---------|
| `beads-village_init(...)` | Join workspace; must be called first |
| `beads-village_status(...)` | Show workspace, agents, and Beads Village status |
| `beads-village_village_tui()` | Launch the live dashboard TUI |

### Task queue and ownership

| Tool | Purpose |
|------|---------|
| `beads-village_ls(status="ready")` | List claimable work |
| `beads-village_show(id="...")` | Show full issue details |
| `beads-village_claim()` | Claim next ready task |
| `beads-village_add(...)` | Create new task/bug/feature/epic/chore |
| `beads-village_assign(id="...", role="...")` | Assign work to a role (leader only) |
| `beads-village_done(id="...", msg="...")` | Complete task; auto-releases and syncs |

### File reservations

| Tool | Purpose |
|------|---------|
| `beads-village_reservations()` | Inspect active locks |
| `beads-village_reserve(paths=[...], reason="...", ttl=600)` | Acquire file locks |
| `beads-village_release(paths=[...])` | Release some or all locks |

### Messaging and coordination

| Tool | Purpose |
|------|---------|
| `beads-village_msg(subj="...", to="all")` | Send message to team or specific role/agent |
| `beads-village_inbox(unread=true)` | Check unread messages |

### Maintenance and planning helpers

| Tool | Purpose |
|------|---------|
| `beads-village_sync()` | Sync with git / backend state |
| `beads-village_doctor()` | Check or repair database health |
| `beads-village_cleanup(days=2)` | Remove old closed issues |
| `beads-village_bv_insights()` | Bottlenecks, keystones, graph insights |
| `beads-village_bv_plan()` | Parallel execution plan with tracks |
| `beads-village_bv_priority(limit=5)` | Priority recommendations |
| `beads-village_bv_diff(since=..., as_of=...)` | Compare issue changes between revisions |

---

## Reservations and Conflict Resolution

### Worker checklist

```python
1. beads-village_init(...)                                  # join workspace
2. beads-village_inbox(unread=true)                         # check messages
3. beads-village_reservations()                             # inspect locks
4. beads-village_reserve(paths=[FILES], reason=TASK, ttl=600)
5. [DO WORK]                                                # edit only reserved files
6. beads-village_release(paths=[FILES])                     # if pausing / partial / blocked
7. beads-village_done(id="...", msg="Done")              # complete, auto-release, sync
```

### If reserve returns conflicts

```text
beads-village_reserve(...) returns conflicts?
├── Expiring soon? → wait, retry
├── Other files available? → reserve those first
├── Need coordination? → message the team / locking owner
└── Fully blocked? → release what you hold, message the block, use Hive blocked flow if applicable
```

Never force-edit a reserved file.

### Recovery

| Problem | Fix |
|---------|-----|
| Stale lock suspicion | `beads-village_reservations()` then retry `beads-village_reserve(...)` |
| Lost local session | `beads-village_init(...)` again, inspect locks, release/re-reserve as needed |
| Health or storage issues | `beads-village_doctor()` then `beads-village_sync()` |

---

## Role and Task Metadata

Use role tags consistently when creating work:

- `fe`
- `be`
- `mobile`
- `devops`
- `qa`

Useful `beads-village_add(...)` fields:

- `title`: actionable task title
- `typ`: `task` | `bug` | `feature` | `epic` | `chore`
- `pri`: `0` critical, `1` high, `2` normal, `3` low, `4` backlog
- `tags`: role and area tags
- `deps`: dependency IDs in `type:id` format
- `parent`: parent issue ID

Example:

```python
beads-village_add(
    title="Implement auth middleware",
    typ="task",
    pri=2,
    tags=["be", "auth"],
    deps=["discovered-from:bd-20"]
)
```

---

## Relationship to Hive and OMO

Use beads-village with the following boundary:

- **beads-village** → coordination, reservations, claiming, completion, messaging
- **Hive** → feature plans, task graph inside the feature, worktree execution, merge flow
- **OMO** → delegation, research, one-shot execution

One-line rule: **beads-village tracks the shared work; Hive or OMO performs the work.**

---

## Relationship to Beads / bd Backend

In this workflow, beads-village is the **primary interface** and Beads / `bd` is the **backend/fallback layer**.

Drop down to `references/beads.md` when you need:

- raw `bd` queries or labels/dependency operations
- direct `.beads/` / Dolt inspection
- export and raw sync rituals
- backend diagnostics or maintenance beyond the MCP surface
