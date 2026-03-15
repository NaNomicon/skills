---
name: beads-hive-omo-workflow
description: "Use for ALL feature-level and project-level work that spans multiple files, tasks, or agents. Load this skill when: planning a feature, running parallel worktrees, using bd/Beads commands, reserving files, coordinating multiple subagents, or deciding between @plan vs hive_plan_write vs task(). Covers the full Beads→Hive→OMO stack: project backlog (bd CLI), feature execution (Hive worktrees + batched parallelism), and agent orchestration (OMO categories + delegation). Also load when resuming interrupted Hive work or debugging a blocked forager."
---

# Beads → Hive → OMO Workflow

Three-layer coordination stack for feature development with parallel agents.

## The Stack

```
Beads Village (bd CLI)     — Project backlog: WHAT to work on, issue tracking, file locking
Hive (opencode-hive)       — Feature execution: HOW to build it (git worktrees, batched parallelism)
OMO (oh-my-openagent)      — Agent layer: WHO builds it (models, categories, delegation)
```

**Iron Rule**: A unit of work is either Hive-managed (worktree) OR OMO `task()` — never both.

---

## Choosing Your Entry Point

| Situation | Route |
|-----------|-------|
| Ambiguous requirements | `@plan` → Prometheus interview → approved plan → `hive_plan_write` |
| Clear requirements, 3+ file changes | `hive_feature_create` directly |
| One-shot research or single change | `task()` delegation — skip Hive entirely |
| Resuming interrupted work | `hive_status` first; check `.hive/` + `bd ready --json` |

> **Do NOT** route `@plan` → `/start-work` when using Hive worktrees. `/start-work` activates Atlas (OMO-only pipeline). Instead: Prometheus produces a plan → you paste it into `hive_plan_write`.

---

## Session Lifecycle

### Start of session
```bash
bd sync                # Pull latest issue state from remote
bd ready --json        # See unblocked issues

# Then one of:
hive_status()          # Check if continuing a feature
hive_feature_create(name="...")  # Start new feature
```

### Core workflow (6 steps)

**1. Create feature**
```
hive_feature_create(name="user-auth")
```

**2. Write plan** ← HARD GATE: requires `## Discovery` section ≥100 chars
```
hive_plan_write(content="## Discovery\n<context, assumptions>\n## Tasks\n...")
```
For ambiguous scope: run `@plan` first, then paste Prometheus output here.

**3. Human approves**
```
hive_plan_approve()
```

**4. Generate tasks from plan**
```
hive_tasks_sync()
```

**5. Execute in batches**

Tasks within a batch run **in parallel**. Batches run **sequentially** — context from batch N flows into batch N+1 via `hive_context_write`.

```
# Batch 1 (parallel)
hive_worktree_create(task="01-extract-auth-logic")
hive_worktree_create(task="02-setup-jwt-utils")
hive_worktree_create(task="03-write-tests")

# After batch 1 completes + orchestrator verifies
hive_context_write(name="batch-1-results", content="...")

# Batch 2 (context-aware, parallel)
hive_worktree_create(task="04-wire-middleware")
hive_worktree_create(task="05-integration-test")
```

After each batch: run full build + test suite (orchestrator tier). See `references/hive.md` → Two-tier Verification.

**6. Merge completed tasks**
```
hive_merge(task="01-extract-auth-logic")
hive_merge(task="02-setup-jwt-utils")
```

### End of session
```bash
bd close <id>                            # Close completed Beads issue
git pull --rebase && bd dolt push && git push
```
Never stop before pushing — work stranded locally = invisible to team.

---

## File Locking (Parallel Foragers)

Every forager must reserve files before editing — prevents conflicts when multiple worktrees touch the same files.

```
reserve(paths=["src/auth/middleware.ts"], reason="implementing JWT middleware", ttl=600)
# ... do work ...
release()
```

**RESERVE BEFORE EDIT. RELEASE WHEN DONE. No exceptions.**

If `reserve()` returns conflicts: see `references/beads.md` → Conflict Resolution.

---

## Blocked Worker Protocol

1. **Worker**: `hive_worktree_commit(status="blocked", blocker={reason, options, recommendation})`
2. **Swarm**: asks user via `question()` tool (NOT plain text)
3. **Resume**: `hive_worktree_create(task="...", continueFrom="blocked", decision="<answer>")`

A new forager spawns in the **same worktree** with the decision as context.

---

## Context Persistence

Decisions and findings that must survive session restarts:
```
hive_context_write(name="architecture-decisions", content="...")
```
Stored in `.hive/features/<name>/contexts/` — this is the Royal Jelly. Read it before planning the next batch.

---

## Beads vs GitHub Issues

| GitHub Issues | Beads (bd) |
|---------------|------------|
| Human coordination | Agent runtime |
| PR linking, team discussion | Task dispatch, file locking |
| Persistent, public record | Per-session agent coordination |

**Hand-off pattern**: Human creates GH Issue → agent `bd create` with dep link → agent works → PR uses `closes #N` → agent `bd close`

---

## Reference Files

Load the relevant reference when you need deeper detail:

| Reference | When to load |
|-----------|-------------|
| `references/beads.md` | bd CLI commands, reserve/release protocol, conflict resolution, sync |
| `references/hive.md` | Bee roles, .hive/ structure, agent configs, batched parallelism details |
| `references/omo.md` | OMO agents (Prometheus/Atlas/etc.), categories→models, delegation patterns |
