# Skills Collection

This repository contains my reusable skills for agentic workflows.

## Skills

### `dokploy-admin`

Use for Dokploy deployment, operations, and troubleshooting across MCP, API, CLI, and SSH/Docker. Select the safest effective control plane, apply minimal changes, and verify real runtime outcomes.

**Install:** 
```sh
npx skills add https://github.com/NaNomicon/skills --skill dokploy-admin
```

**Path:** `dokploy-admin/SKILL.md`

### `dev-machine-storage-cleanup`

Use when storage is low on development machines. Systematic approach to find and safely reclaim disk space. Covers caches, dependencies, Docker, iOS simulators, and build artifacts with platform-specific guidance for macOS and Linux. **Core principle:** Analyze first, clean selectively, always confirm with user.

**Install:** 
```sh
npx skills add https://github.com/NaNomicon/skills --skill dev-machine-storage-cleanup
```

**Path:** `dev-machine-storage-cleanup/SKILL.md`

### `beads-hive-omo-workflow`

Use for ALL feature-level and project-level work that spans multiple files, tasks, or agents. Covers the full Beads→Hive→OMO stack: project backlog (bd CLI), feature execution (Hive worktrees + batched parallelism), and agent orchestration (OMO categories + delegation). Load when planning a feature, running parallel worktrees, using bd/Beads commands, reserving files, coordinating multiple subagents, or deciding between `@plan` vs `hive_plan_write` vs `task()`.

**Install:** 
```sh
npx skills add https://github.com/NaNomicon/skills --skill beads-hive-omo-workflow
```

**Path:** `beads-hive-omo-workflow/SKILL.md`

### `tilth`

Runs tilth CLI for structural code navigation — reads files with smart outlining, searches symbols/text/regex, finds files by glob, and maps codebases. Use instead of read/grep/find for all source code exploration.

**Install:** 
```sh
npx skills add https://github.com/NaNomicon/skills --skill tilth
```

**Path:** `tilth/SKILL.md`
