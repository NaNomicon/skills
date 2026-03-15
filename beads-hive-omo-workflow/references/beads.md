# Beads Village — bd CLI Reference

## Where Beads Lives

```
.beads/                   # Committed to git (config.yaml, README.md, hooks/)
.beads/dolt/              # Gitignored — managed by Dolt (the versioned DB)
.beads/.gitignore         # Excludes: dolt/, ephemeral.sqlite3, backup/, .sync.lock
.reservations/            # LOCAL only — NOT synced via Dolt (agent-machine-local)
.mail/                    # Messages
```

`.beads/` skeleton is checked into git. Issue state lives in Dolt, synced separately.

---

## Essential bd Commands

Always use `--json` for programmatic use.

```bash
# Session start
bd sync                                          # = bd dolt pull + bd dolt push
bd ready --json                                  # Show unblocked (no-dep) issues

# Issue management
bd create "Title" -t task -p 2 --json            # Create (types: bug|feature|task|epic|chore)
bd update <id> --claim --json                    # Claim atomically
bd close <id> --reason "Done" --json             # Complete
bd show <id> --json                              # Full issue details

# Dependencies
bd update <id> --deps discovered-from:<parent>   # Link related work

# Sync
bd dolt push                                     # Push issue state to remote
bd dolt pull                                     # Pull latest from remote

# Health
bd doctor                                        # Check DB health
```

**Priorities**: 0=Critical, 1=High, 2=Medium (default), 3=Low, 4=Backlog

---

## Agent Issue Workflow

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

## Reserve / Release Protocol

### Iron Law

```
RESERVE BEFORE EDIT. RELEASE WHEN DONE. NO EXCEPTIONS.
```

Reservations use `O_CREAT|O_EXCL` for atomicity — safe for parallel agents on the **same machine**. They are NOT distributed across machines (local filesystem only, under `.reservations/`).

### Worker Checklist

```
1. init()                                          # Register (idempotent)
2. inbox(unread=true)                              # Check messages
3. reservations()                                  # Check existing locks
4. reserve(paths=[FILES], reason=TASK, ttl=600)    # Lock files you will edit
5. [DO WORK]                                       # Edit ONLY reserved files
6. release()                                       # Unlock all
7. msg(subj="Done: SUMMARY", global=true, to="all") # Notify team
```

**Blocked?** → `release()` first → `msg(subj="Blocked: REASON", ...)` → `hive_worktree_commit(status="blocked")`

**Resuming?** → Start from step 1. Previous reservations may have expired.

### Conflict Resolution

```
reserve() returns conflicts?
├── Expires soon (< 2 min)? → Wait, retry
├── Can work on other files? → Reserve those first, come back
├── Urgent? → msg(to="locking-agent") → Wait for inbox() response
└── Fully blocked? → release() → hive_worktree_commit(status="blocked")
```

Never force-edit a reserved file.

### Recovery

| Problem | Fix |
|---------|-----|
| Stale lock | `reservations()` then retry `reserve()` |
| Lost session | `init()` → `release()` → re-reserve |
| Tool errors | `doctor()` then `sync()` |

---

## Multi-Dev Sync

- Dolt syncs **issue state** across developers (`bd sync` = dolt pull + push)
- Reservations protect **parallel agents on the same machine** (Hive foragers in worktrees)
- Cross-machine file conflicts are normal git merge territory — Beads doesn't solve those

### Session start
```bash
bd sync                  # Get latest issues from team
bd ready --json          # Pick unblocked work
```

### Session end
```bash
bd close <id>            # Mark complete
git pull --rebase        # Get latest code
bd dolt push             # Push issue state
git push                 # Push code
```

---

## Hive Bridge Tools (auto-activate when `.hive/` exists)

- `hive_lock(paths, task, ttl=900)` — Reserve files for a Hive task
- `hive_unlock()` — Release all Hive-tagged locks
- `hive_status_bridge()` — Combined Hive + Beads status

---

## Session Completion Ritual (Landing the Plane)

Work is NOT done until `git push` succeeds:

1. `bd create` for any remaining/discovered issues
2. Run quality gates (tests, linters)
3. `bd close <id>` for completed work
4. `git pull --rebase && bd dolt push && git push`
5. Verify: `git status` shows "up to date with origin"
