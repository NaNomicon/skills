# OMO — Agent & Category Reference

## Architecture (3 Layers)

```
Planning Layer:   Prometheus → Metis → Momus
Execution Layer:  Atlas (conductor)
Worker Layer:     Sisyphus-Junior, Oracle, Explore, Librarian, Frontend
```

---

## Agent Roster

| Agent | Model | Role |
|-------|-------|------|
| Prometheus | Claude Opus 4.6 | Strategic planner — interview mode, ClearanceCheck flow |
| Metis | — | Gap analyzer — catches what Prometheus missed |
| Momus | GPT-5.4 | Ruthless plan reviewer — validates file refs, acceptance criteria |
| Atlas | Claude Sonnet 4.6 | Executor/conductor — delegates ALL code writing, never writes code itself |
| Sisyphus-Junior | Claude Sonnet 4.6 | Focused task worker — cannot delegate, must pass lsp_diagnostics |
| Oracle | GPT-5.4 | Architecture, debugging, complex logic consultation |
| Explore | Grok Code | Codebase grep — internal pattern discovery |
| Librarian | Gemini 3 Flash | External docs, OSS examples, library best practices |
| Frontend | Gemini 3.1 Pro | UI/UX, component work |

---

## Categories → Models

| Category | Model | Use for |
|----------|-------|---------|
| `visual-engineering` | Gemini 3.1 Pro | UI, CSS, animations, layout, design |
| `ultrabrain` | GPT-5.4 (xhigh) | Hard logic, algorithms, architecture decisions |
| `artistry` | Gemini 3.1 Pro (high) | Non-conventional problems, creative approaches |
| `deep` | GPT-5.3 Codex (medium) | Goal-oriented autonomous research + implementation |
| `quick` | Claude Haiku 4.5 | Trivial: single file, typo, simple config |
| `unspecified-high` | Claude Opus 4.6 (max) | Complex tasks without clear domain |
| `unspecified-low` | Claude Sonnet 4.6 | Low-complexity tasks without clear domain |
| `writing` | Gemini 3 Flash | Documentation, prose, technical writing |

---

## When to Use Which Entry Point

```
Simple/quick fix          → just describe it (Sisyphus handles or delegates)
Complex, tedious to explain → ulw (ultrawork mode)
Complex, precise multi-step  → @plan → Prometheus interview → hive_plan_write → hive_plan_approve → hive_tasks_sync
```

---

## Prometheus Interview Flow

1. **Interview**: Prometheus asks targeted questions (one at a time)
2. **ClearanceCheck**: Must pass all gates before writing plan:
   - Core objective defined?
   - Scope established?
   - No ambiguities remaining?
   - Technical approach decided?
   - Test strategy confirmed?
3. **MetisConsult**: Mandatory gap analysis (catches what interview missed)
4. **WritePlan**: Produces structured plan.md
5. **Present to user**: Optional MomusLoop for high accuracy
6. **Output**: Paste approved plan into `hive_plan_write` (do NOT use `/start-work`)

**Momus validation criteria**: ≥100% file refs verified, ≥80% tasks with clear source, ≥90% concrete acceptance criteria, zero assumption tasks.

---

## Atlas (OMO-only executor)

Atlas activates via `/start-work` (reads `.sisyphus/boulder.json`).

**Atlas rules**:
- MUST delegate ALL code writing to Sisyphus-Junior or specialists
- CAN read, run commands, search, review results
- After each task: extract learnings → categorize into Conventions/Successes/Failures/Gotchas/Commands
- Persists to `.sisyphus/notepads/{plan-name}/{learnings,decisions,issues,verification}.md`

**When to use Atlas vs Hive**:
- Atlas (`/start-work`): fast execution, no worktree isolation, good for sequential tasks
- Hive: parallel worktrees, persistent context across sessions, human approval gates

Do NOT mix: if you want Hive worktrees, use `hive_plan_write` — not `/start-work`.

---

## Session Continuity (boulder.json)

`.sisyphus/boulder.json` tracks active Atlas plan:
- `active_plan`, `session_ids`, `started_at`, `plan_name`
- `/start-work` auto-detects: RESUME MODE (boulder exists) vs INIT MODE (new)

For Hive-managed features: state lives in `.hive/` instead.

---

## task() Delegation Pattern

```typescript
// Correct: domain-matched category + relevant skills
task(category="visual-engineering", load_skills=["frontend-ui-ux"], prompt="...")
task(category="ultrabrain", load_skills=[], prompt="...")
task(category="quick", load_skills=["git-master"], prompt="...")

// Background agents (always background=true)
task(subagent_type="explore", run_in_background=true, load_skills=[], prompt="...")
task(subagent_type="librarian", run_in_background=true, load_skills=[], prompt="...")
```

Always store session_id for continuation:
```typescript
task(session_id="ses_abc123", load_skills=[], prompt="Fix: <specific error>")
```

---

## Hive vs OMO task() — Decision Rule

| Use Hive worktrees when | Use task() when |
|------------------------|-----------------|
| 3+ file changes | One-shot research or change |
| Need isolation (parallel foragers) | No parallelism needed |
| Context must survive across sessions | Single-session work |
| Human approval gate required | Trust agent to proceed |
| Audit trail needed (spec.md, report.md) | Speed > auditability |
