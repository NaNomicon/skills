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

[![Weekly Installs](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fskills.sh%2Fapi%2Fsearch%3Fq%3Ddokploy-admin%26limit%3D10&label=Weekly%20Installs&query=%24.skills%5B0%5D.installs)](https://skills.sh/nanomicon/skills/dokploy-admin)
[![Socket](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fadd-skill.vercel.sh%2Faudit%3Fsource%3Dnanomicon%2Fskills%26skills%3Ddokploy-admin&label=Socket&query=%24%5B%22dokploy-admin%22%5D.socket.risk)](https://skills.sh/nanomicon/skills/dokploy-admin/security/socket)
[![Snyk](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fadd-skill.vercel.sh%2Faudit%3Fsource%3Dnanomicon%2Fskills%26skills%3Ddokploy-admin&label=Snyk&query=%24%5B%22dokploy-admin%22%5D.snyk.risk)](https://skills.sh/nanomicon/skills/dokploy-admin/security/snyk)
[![ATH](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fadd-skill.vercel.sh%2Faudit%3Fsource%3Dnanomicon%2Fskills%26skills%3Ddokploy-admin&label=ATH&query=%24%5B%22dokploy-admin%22%5D.ath.risk)](https://skills.sh/nanomicon/skills/dokploy-admin/security/agent-trust-hub)

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

[![Weekly Installs](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fskills.sh%2Fapi%2Fsearch%3Fq%3Ddev-machine-storage-cleanup%26limit%3D10&label=Weekly%20Installs&query=%24.skills%5B0%5D.installs)](https://skills.sh/nanomicon/skills/dev-machine-storage-cleanup)
[![Socket](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fadd-skill.vercel.sh%2Faudit%3Fsource%3Dnanomicon%2Fskills%26skills%3Ddev-machine-storage-cleanup&label=Socket&query=%24%5B%22dev-machine-storage-cleanup%22%5D.socket.risk)](https://skills.sh/nanomicon/skills/dev-machine-storage-cleanup/security/socket)
[![Snyk](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fadd-skill.vercel.sh%2Faudit%3Fsource%3Dnanomicon%2Fskills%26skills%3Ddev-machine-storage-cleanup&label=Snyk&query=%24%5B%22dev-machine-storage-cleanup%22%5D.snyk.risk)](https://skills.sh/nanomicon/skills/dev-machine-storage-cleanup/security/snyk)
[![ATH](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fadd-skill.vercel.sh%2Faudit%3Fsource%3Dnanomicon%2Fskills%26skills%3Ddev-machine-storage-cleanup&label=ATH&query=%24%5B%22dev-machine-storage-cleanup%22%5D.ath.risk)](https://skills.sh/nanomicon/skills/dev-machine-storage-cleanup/security/agent-trust-hub)

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

[![Weekly Installs](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fskills.sh%2Fapi%2Fsearch%3Fq%3Dbeads-hive-omo-workflow%26limit%3D10&label=Weekly%20Installs&query=%24.skills%5B0%5D.installs)](https://skills.sh/nanomicon/skills/beads-hive-omo-workflow)
[![Socket](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fadd-skill.vercel.sh%2Faudit%3Fsource%3Dnanomicon%2Fskills%26skills%3Dbeads-hive-omo-workflow&label=Socket&query=%24%5B%22beads-hive-omo-workflow%22%5D.socket.risk)](https://skills.sh/nanomicon/skills/beads-hive-omo-workflow/security/socket)
[![Snyk](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fadd-skill.vercel.sh%2Faudit%3Fsource%3Dnanomicon%2Fskills%26skills%3Dbeads-hive-omo-workflow&label=Snyk&query=%24%5B%22beads-hive-omo-workflow%22%5D.snyk.risk)](https://skills.sh/nanomicon/skills/beads-hive-omo-workflow/security/snyk)
[![ATH](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fadd-skill.vercel.sh%2Faudit%3Fsource%3Dnanomicon%2Fskills%26skills%3Dbeads-hive-omo-workflow&label=ATH&query=%24%5B%22beads-hive-omo-workflow%22%5D.ath.risk)](https://skills.sh/nanomicon/skills/beads-hive-omo-workflow/security/agent-trust-hub)

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

[![Weekly Installs](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fskills.sh%2Fapi%2Fsearch%3Fq%3Dtilth%26limit%3D10&label=Weekly%20Installs&query=%24.skills%5B0%5D.installs)](https://skills.sh/nanomicon/skills/tilth)
[![Socket](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fadd-skill.vercel.sh%2Faudit%3Fsource%3Dnanomicon%2Fskills%26skills%3Dtilth&label=Socket&query=%24%5B%22tilth%22%5D.socket.risk)](https://skills.sh/nanomicon/skills/tilth/security/socket)
[![Snyk](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fadd-skill.vercel.sh%2Faudit%3Fsource%3Dnanomicon%2Fskills%26skills%3Dtilth&label=Snyk&query=%24%5B%22tilth%22%5D.snyk.risk)](https://skills.sh/nanomicon/skills/tilth/security/snyk)
[![ATH](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fadd-skill.vercel.sh%2Faudit%3Fsource%3Dnanomicon%2Fskills%26skills%3Dtilth&label=ATH&query=%24%5B%22tilth%22%5D.ath.risk)](https://skills.sh/nanomicon/skills/tilth/security/agent-trust-hub)

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