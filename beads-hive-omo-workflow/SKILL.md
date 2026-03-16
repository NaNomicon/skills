---
name: beads-hive-omo-workflow
description: "Use for feature-level or project-level work that spans multiple files, tasks, or agents. Load when using beads-village MCP tools, Hive worktrees, file reservations, shared task coordination, or deciding between `beads-village`, `hive_*`, and OMO `task()`. Also load when resuming blocked Hive work or when Beads / `bd` backend fallback may be needed behind a beads-village-managed workflow."
---

# beads-village → Hive → OMO Workflow

Three-layer coordination stack for feature development with parallel agents.

> Historical note: the skill name stays `beads-hive-omo-workflow` for compatibility. The workflow itself is now **beads-village-first**.

## The Stack

```
beads-village (MCP)      — Project/shared coordination: claim, task state, reservations, messaging, sync
Hive (opencode-hive)     — Feature execution: plans, execution tasks, worktrees, batched parallelism
OMO (oh-my-openagent)    — Agent layer: delegation, research, one-shot execution
Beads / bd               — Backend/CLI under beads-village (fallback + implementation detail)
```

**Primary rule**: **Claim in beads-village, execute in Hive or OMO, reserve through beads-village.**

**Iron Rule**: A unit of work is either Hive-managed (worktree) OR OMO `task()` — never both.

**Boundary rule**: Hive manages **feature execution tasks**. beads-village manages **project/shared coordination, reservations, and completion state**.

---

## Responsibility Split

| Concern | Primary owner | Typical tools |
|---------|----------------|---------------|
| Ready/claimed/done project work | beads-village | `beads-village_claim`, `beads-village_ls`, `beads-village_add`, `beads-village_done` |
| File reservations and messaging | beads-village | `beads-village_reserve`, `beads-village_release`, `beads-village_msg`, `beads-village_inbox` |
| Feature plan + execution tasks | Hive | `hive_feature_create`, `hive_plan_write`, `hive_tasks_sync`, `hive_worktree_*` |
| Worktree execution | Hive | `hive_worktree_start`, `hive_worktree_create`, `hive_merge` |
| Research / one-shot execution | OMO | `task()` |
| Backend / CLI fallback | Beads / `bd` | `bd ...` commands in `references/beads.md` |

If you are unsure who owns something:
- **shared coordination / locking** → beads-village
- **feature plan / worktree execution** → Hive
- **one-shot work or delegation** → OMO

For exact MCP coordination semantics, load `references/beads-village.md`. Load `references/beads.md` only when you need backend or raw CLI fallback behavior.

---

## Choosing Your Entry Point

| Situation | Route |
|-----------|-------|
| Ambiguous requirements | `@plan` → Prometheus interview → approved plan → `hive_plan_write` |
| Clear feature, 3+ file changes | inspect ready work with `beads-village_ls(status="ready")` / `beads-village_show(...)` → `beads-village_claim()` → `hive_feature_create` |
| One-shot research or single change | `beads-village_claim()` if tracking exists → `task()` delegation — skip Hive entirely |
| Resuming interrupted work | `beads-village_status(include_bv=true)` + `hive_status` |
| Need to create shared work first | `beads-village_add(...)` then claim/assign as needed |

> **Do NOT** route `@plan` → `/start-work` when using Hive worktrees. `/start-work` activates Atlas (OMO-only pipeline). Instead: Prometheus produces a plan → you paste it into `hive_plan_write`.

---

## Session Lifecycle

### Start of session

```bash
beads-village_init(role="be", team="default")        # or the role/team that fits the task
beads-village_ls(status="ready")                      # inspect claimable work
beads-village_claim()                                  # claim next ready task when appropriate

# Then choose an execution lane:
hive_status()                                          # continue existing feature work
hive_feature_create(name="...")                        # start new feature work
task(...)                                              # one-shot research / change, skip Hive
```

### Core workflow (7 steps)

**1. Enter through beads-village**

Inspect existing work first. If it already exists, claim it. If it does not, create it and then claim it:

```bash
beads-village_ls(status="ready")
beads-village_show(id="bd-42")
beads-village_claim()

# If no shared work item exists yet:
beads-village_add(title="...", typ="task", tags=["be"])
beads-village_claim()
```

Use beads-village as the source of truth for shared task state.

**2. Choose the execution lane**

- **Hive** when the work needs a feature plan, worktrees, or 3+ coordinated file changes
- **OMO `task()`** when the work is one-shot research or a focused change

**3. Reserve before edit**

Reserve files through beads-village before any worker edits them:

```bash
beads-village_reserve(paths=["src/auth/middleware.ts"], reason="implementing JWT middleware", ttl=600)
# ... do work ...
beads-village_release(paths=["src/auth/middleware.ts"])
```

If you are finishing the task with `beads-village_done(...)`, explicit release may be unnecessary because completion auto-releases; use `release()` when pausing, blocking, or partially finishing.

**4. If Hive lane: create and approve the feature plan**

```bash
hive_feature_create(name="user-auth")
hive_plan_write(content="## Discovery\n<context, assumptions>\n## Tasks\n...")
hive_plan_approve()
hive_tasks_sync()
```

`hive_plan_write` requires a `## Discovery` section ≥100 chars.

**5. Execute Hive tasks in batches**

Tasks within a batch run **in parallel**. Batches run **sequentially** — context from batch N flows into batch N+1 via `hive_context_write`.

**Tool names**:
- `hive_worktree_start(task)` — start a **new** pending/in_progress task
- `hive_worktree_create(task, continueFrom="blocked", decision)` — resume a **blocked** task ONLY

`hive_worktree_start` does NOT directly spawn the worker — it returns a delegation response with a forager prompt. The orchestrator must then call `task()` to spawn each forager.

**For parallel execution, issue all `task()` calls in the SAME response:**

```bash
# Step 1: Set up all worktrees for the batch (sequential — fast metadata ops)
hive_worktree_start(task="01-extract-auth-logic")  # returns forager prompt 1
hive_worktree_start(task="02-setup-jwt-utils")      # returns forager prompt 2
hive_worktree_start(task="03-write-tests")          # returns forager prompt 3

# Step 2: Spawn ALL foragers in SAME response → OpenCode runs them concurrently
task(prompt="<forager-prompt-1>", run_in_background=true)
task(prompt="<forager-prompt-2>", run_in_background=true)
task(prompt="<forager-prompt-3>", run_in_background=true)

# After all complete:
hive_context_write(name="batch-1-results", content="...")

# Batch 2 (new batch, context-aware)
hive_worktree_start(task="04-wire-middleware")
hive_worktree_start(task="05-integration-test")
task(prompt="<forager-prompt-4>", run_in_background=true)
task(prompt="<forager-prompt-5>", run_in_background=true)
```

After each batch: run full build + test suite (orchestrator tier). See `references/hive.md` → Two-tier Verification.

**6. Merge completed Hive work**

```bash
hive_merge(task="01-extract-auth-logic")
hive_merge(task="02-setup-jwt-utils")
```

**7. Finish through beads-village**

```bash
beads-village_done(id="<issue-id>", msg="Completed feature work")

# Optional only when you need an extra sync outside normal completion:
beads-village_sync()
```

Use `beads-village_done(...)` as the canonical completion step for shared task state. It is the normal finish path and already handles the standard completion/sync behavior. Use explicit `beads-village_sync()` only when you need an extra sync outside that path. Mention raw `bd` completion/sync only when you explicitly need backend fallback behavior.

### End of session

```bash
beads-village_done(id="<issue-id>", msg="Done")      # marks complete, auto-releases, syncs
# If you still need maintenance or diagnostics:
beads-village_doctor()
beads-village_cleanup(days=2)
```

Never stop with claimed work half-finished and uncommunicated — release, block, or complete it explicitly through beads-village.

---

## File Locking (Parallel Workers)

Every worker must reserve files through beads-village before editing — this prevents conflicts when multiple worktrees or agents touch the same files.

```bash
beads-village_reservations()
beads-village_reserve(paths=["src/auth/middleware.ts"], reason="implementing JWT middleware", ttl=600)
# ... do work ...
beads-village_release(paths=["src/auth/middleware.ts"])
```

**RESERVE BEFORE EDIT. RELEASE WHEN DONE. No exceptions.**

If `beads-village_reserve(...)` returns conflicts: see `references/beads-village.md` → Conflict Resolution.

---

## Blocked Worker Protocol

1. **Worker**: if coordination is blocked, optionally notify via `beads-village_msg(subj="Blocked: ...", to="all")`
2. **Worker**: `hive_worktree_commit(status="blocked", blocker={reason, options, recommendation})`
3. **Swarm**: asks user via `question()` tool (NOT plain text)
4. **Resume**: `hive_worktree_create(task="...", continueFrom="blocked", decision="<answer>")`

A new forager spawns in the **same worktree** with the decision as context.

---

## Context Persistence

Decisions and findings that must survive session restarts:

```bash
hive_context_write(name="architecture-decisions", content="...")
```

Stored in `.hive/features/<name>/contexts/` — this is the Royal Jelly. Read it before planning the next batch.

---

## beads-village vs GitHub Issues

| GitHub Issues | beads-village |
|---------------|---------------|
| Human coordination | Agent-facing coordination layer |
| PR linking, team discussion | Claiming, reservations, messaging, completion |
| Persistent, public record | Runtime workflow over the Beads backend |

**Hand-off pattern**: Human creates GH Issue → agent `beads-village_add(...)` or matching task → agent works → PR uses `closes #N` → agent `beads-village_done(...)`

---

## Reference Files

Load the relevant reference when you need deeper detail:

| Reference | When to load |
|-----------|-------------|
| `references/beads-village.md` | Primary MCP coordination surface: init, claim/done flow, reservations, messaging, sync, and operational helpers |
| `references/beads.md` | Beads / `bd` backend and raw CLI fallback: Dolt state, issue schema, export/sync, labels, deps, and backend maintenance |
| `references/hive.md` | Bee roles, `.hive/` structure, agent configs, batched parallelism details |
| `references/omo.md` | OMO agents (Prometheus/Atlas/etc.), categories → models, delegation patterns |

Load `references/beads-village.md` first for normal workflow. When the text says `bd`, read it as **backend/fallback context** unless it explicitly says to use the raw CLI.
