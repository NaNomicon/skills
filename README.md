# Skills Collection

This repository contains reusable skills for agentic workflows. Each skill is opinionated: it is meant to trigger in a specific situation, steer the model toward a better operating pattern, and reduce repeated decision-making during real work.

## How to use this repository

- Browse the index below to find the skill that matches the job.
- Each skill entry explains **what it is**, **when to use it**, and **why it exists**.
- Install a skill directly from this repository with:

```sh
npx skills add https://github.com/NaNomicon/skills --skill <skill-name>
```

## Skill Index

| Skill | Best for | Reach for it when |
| --- | --- | --- |
| `dokploy-admin` | Dokploy deployment and operations | You need to operate or troubleshoot Dokploy safely across MCP, API, CLI, or SSH/Docker |
| `dev-machine-storage-cleanup` | Low disk space on dev machines | A machine is running out of storage and you need a safe, structured cleanup flow |
| `beads-hive-omo-workflow` | Multi-step, multi-agent feature execution | Work spans multiple files, agents, or worktrees and needs beads-village / Hive / OMO coordination |
| `tilth` | Structural code navigation | You need to read, search, trace, or map code without falling back to raw `read` / `grep` / `find` |

---

## `dokploy-admin`

![Weekly Installs](badges/dokploy-admin/weekly-installs.svg)
![Security Audit](badges/dokploy-admin/security-audit.svg)
![Listing Status](badges/dokploy-admin/listing-status.svg)

**What it is**  
A Dokploy operations skill for deployment, runtime operations, and troubleshooting. It helps the model choose the safest effective control plane in order: MCP first, then API, then CLI, then SSH/Docker as the deepest fallback.

**When to use it**  
Use it when the task involves Dokploy services, applications, deployments, logs, environment configuration, or operational debugging.

**Why use it**  
Dokploy work often has multiple possible access paths. This skill exists to prevent unsafe guesswork, minimize blast radius, and keep changes grounded in real runtime verification instead of configuration-only assumptions.

**Install**

```sh
npx skills add https://github.com/NaNomicon/skills --skill dokploy-admin
```

**Path:** `dokploy-admin/SKILL.md`

---

## `dev-machine-storage-cleanup`

![Weekly Installs](badges/dev-machine-storage-cleanup/weekly-installs.svg)
![Security Audit](badges/dev-machine-storage-cleanup/security-audit.svg)
![Listing Status](badges/dev-machine-storage-cleanup/listing-status.svg)

**What it is**  
A safe cleanup workflow for development machines with low disk space. It covers the usual high-impact culprits: Docker data, language package caches, simulator artifacts, SDK/tooling caches, and build outputs.

**When to use it**  
Use it when a development machine is low on storage, showing disk warnings, slowing down because the drive is nearly full, or when you want to reclaim space before or after heavy project work.

**Why use it**  
Storage cleanup is risky when done ad hoc. This skill exists to enforce an analyze-first workflow: inspect usage, explain the tradeoffs, and confirm before deleting anything. It is designed to reclaim space without casually breaking local development environments.

**Install**

```sh
npx skills add https://github.com/NaNomicon/skills --skill dev-machine-storage-cleanup
```

**Path:** `dev-machine-storage-cleanup/SKILL.md`

---

## `beads-hive-omo-workflow`

![Weekly Installs](badges/beads-hive-omo-workflow/weekly-installs.svg)
![Security Audit](badges/beads-hive-omo-workflow/security-audit.svg)
![Listing Status](badges/beads-hive-omo-workflow/listing-status.svg)

**What it is**  
A workflow skill for multi-file and multi-agent execution using the **beads-village → Hive → OMO** stack. It treats `beads-village` as the primary coordination layer, Hive as the feature execution/worktree layer, and OMO as the delegation and one-shot execution layer. Raw Beads / `bd` remains documented as backend and fallback context.

**When to use it**  
Use it when work spans multiple files, tasks, or agents; when you need reservations or shared task state; when using `beads-village` MCP tools or Hive worktrees; or when deciding whether a unit of work belongs in `beads-village`, `hive_*`, or OMO `task()`.

**Why use it**  
This skill exists to keep coordination boundaries clear. Without it, agents tend to blur ownership between backlog state, worktree execution, and one-shot delegation. The skill gives a consistent rule: claim in beads-village, execute in Hive or OMO, and treat raw `bd` as backend/fallback rather than the default interface.

**Install**

```sh
npx skills add https://github.com/NaNomicon/skills --skill beads-hive-omo-workflow
```

**Path:** `beads-hive-omo-workflow/SKILL.md`

---

## `tilth`

![Weekly Installs](badges/tilth/weekly-installs.svg)
![Security Audit](badges/tilth/security-audit.svg)
![Listing Status](badges/tilth/listing-status.svg)

**What it is**  
A structural code navigation skill built around the `tilth` CLI. It covers smart file reading, symbol-aware search, literal/regex search, file discovery, and codebase mapping.

**When to use it**  
Use it whenever you need to explore source code: reading a file, tracing a symbol, searching code patterns, finding files, or understanding project structure.

**Why use it**  
This skill exists because raw `read`, `grep`, and `find` lose structure and waste tokens. `tilth` gives richer results with better boundaries, which makes code exploration faster, more reliable, and easier to scale across larger repositories.

**Install**

```sh
npx skills add https://github.com/NaNomicon/skills --skill tilth
```

**Path:** `tilth/SKILL.md`
