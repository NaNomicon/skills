---
name: dev-machine-storage-cleanup
description: "Use when the user needs to analyze disk usage and reclaim storage on development machines. ALWAYS use this skill when the user says: 'disk full', 'out of space', 'low disk', 'running out of space', 'free up space', 'clean up disk', 'storage warning', 'need more space', 'disk almost full', 'cleanup storage', or mentions their disk is full/slow. Covers Docker, npm/pip/cargo caches, iOS Simulators, Android SDK, build artifacts, and platform-specific cleanup for macOS and Linux. Follows safe workflow: ANALYZE, PRESENT, EXPLAIN, CONFIRM (never auto-deletes)."
---

# Dev Machine Storage Cleanup

## Overview

Development machines accumulate large caches, dependencies, and build artifacts that consume significant storage. This skill provides a systematic approach to identify and safely reclaim disk space.

**Core principle:** Analyze first, clean selectively. Never delete without understanding impact.

## When to Use

- Disk space warnings or low storage alerts
- System running slow due to full disk
- Before/after major project work to free space
- Routine maintenance on dev machines

## Platform Detection

```bash
uname -s  # Darwin = macOS, Linux = Linux
```

**Read platform-specific reference after detecting OS:**
- macOS → `references/macos.md`
- Linux → `references/linux.md`

---

## Universal Investigation Workflow

**Disk overview:**
```bash
df -h                                    # Overall disk usage
docker system df                         # Docker storage breakdown (if Docker installed)
```

**Find large directories:**
```bash
du -sh /* 2>/dev/null | sort -rh | head -20      # Root level
du -sh ~/* 2>/dev/null | sort -rh | head -20     # Home directory
```

**Developer caches (universal):**
```bash
du -sh ~/.npm ~/.cache/pip ~/.cargo ~/go/pkg/mod ~/.cache 2>/dev/null | sort -rh
```

---

## Quick Reference — Universal Targets

| Area | Typical Size | Risk Level | Cleanup Command |
|------|--------------|------------|-----------------|
| **Docker** | 5-50 GB | Medium | `docker system prune -af --volumes` |
| **uv cache** | 5-20 GB | Low | `uv cache prune` (keeps active) |
| **npm cache** | 1-5 GB | Low | `npm cache clean --force` |
| **pip cache** | 500 MB - 2 GB | Low | `pip cache purge` |
| **go mod cache** | 1-5 GB | Low | `go clean -modcache` |
| **cargo cache** | 500 MB - 2 GB | Low | `cargo cache -a` |
| **pnpm store** | 5-15 GB | Low | `pnpm store prune` |
| **Build artifacts** | 1-20 GB | Low | Project-specific (`target/`, `dist/`, `build/`) |
| **Old project deps** | 5-50 GB | Low | Delete `node_modules/`, `venv/` in inactive projects |

---

## Docker Cleanup

Docker is often the biggest storage consumer on dev machines.

**Analyze:**
```bash
docker system df                          # Storage breakdown
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
docker volume ls
```

**Clean:**
```bash
# Remove unused images, containers, networks, build cache
docker system prune -af --volumes

# Or selectively:
docker image prune -a                     # Unused images only
docker volume prune                       # Unused volumes only
docker builder prune -a                   # Build cache only
```

**⚠️ Warning:** `--volumes` deletes data volumes. Check for databases, persistent data before running.

---

## Developer Cache Cleanup

### Node.js / npm / pnpm
```bash
npm cache clean --force                   # npm cache
yarn cache clean                          # yarn cache
pnpm store prune                          # pnpm (safe, keeps active packages)

# Find old node_modules
find ~ -type d -name "node_modules" 2>/dev/null | head -20
```

### Python / pip / uv
```bash
pip cache purge                           # pip cache
uv cache prune                            # uv (safe, keeps active)

# Find old venvs
find ~ -type d -name "venv" -o -name ".venv" 2>/dev/null | head -20
```

### Go
```bash
go clean -modcache                        # Module cache (~1-5 GB typically)
```

### Rust / Cargo
```bash
cargo cache -a                            # Or: rm -rf ~/.cargo/registry/cache
```

---

## Build Artifact Cleanup

Common build directories that can be deleted in inactive projects:

| Pattern | Language/Framework |
|---------|-------------------|
| `target/` | Rust, Maven |
| `dist/`, `build/` | JavaScript, TypeScript |
| `__pycache__/`, `*.pyc` | Python |
| `.gradle/` | Gradle (Java/Kotlin) |
| `out/` | Various |

```bash
# Find large build directories
find ~ -type d \( -name "target" -o -name "dist" -o -name "build" -o -name ".gradle" \) 2>/dev/null | \
  xargs -I{} du -sh {} 2>/dev/null | sort -rh | head -20
```

---

## Safety Principles

1. **NEVER auto-clean** — Always present findings and get explicit user confirmation
2. **Explain WHY** — For each target, explain what it is and why safe/risky
3. **Analyze first, clean selectively** — Never delete without understanding impact
4. **Verify before delete** — Cross-check independently
5. **Conservative defaults** — When in doubt, don't delete
6. **Network awareness** — Re-downloading caches can take hours; valuable cache is worth keeping
7. **Check for active processes** — Some caches may be in use by running services

---

## Safety Zones — Universal

### Never Delete

- `~/.ssh/` — SSH keys (irreplaceable)
- `~/.gnupg/` — GPG keys (irreplaceable)
- `~/.password-store/` — Password store (irreplaceable)
- `~/.config/` — App configs (check contents first)
- `~/.local/share/keyrings/` — Encryption keys

### Check Before Deleting

- `~/.local/share/` — App data (verify app not active)
- `~/.aws/`, `~/.kube/` — Cloud credentials
- Project directories with active git work

### System Protected

On any system, if `rm` fails with "Operation not permitted" or "Permission denied" — stop. The system is protecting critical files.

---

## Common Mistakes

- Deleting `node_modules` in active projects without reinstalling
- Running `docker system prune --volumes` without checking for data volumes
- Clearing caches mid-build (can corrupt build state)
- Deleting unknown directories without investigation
- Using `rm -rf` on active caches (e.g., uv while MCP servers running)
- Rushing disk scans (can miss important storage consumers)

---

## Workflow

```
1. ANALYZE → Run investigation commands, identify storage consumers
2. PRESENT → Show findings with sizes and explanations
3. EXPLAIN → For each item, explain what it is and why safe/risky to delete
4. CONFIRM → Ask user which items to clean
5. EXECUTE → Run cleanup commands only for confirmed items
6. VERIFY → Check results, report space reclaimed
```

---

## Reboot Recommendation

Some cleanup only completes after reboot:
- Temp directories (`/tmp`, `/var/tmp`, `/private/var/folders` on macOS)
- Swap files release
- Filesystem snapshots may consolidate

**Action**: Remind user: "Recommend reboot to complete cleanup — some caches only clear on restart."

---

## Platform-Specific References

After detecting the platform, read the appropriate reference file:

- **macOS** → `references/macos.md` — iOS Simulators, ~/Library, SIP protection, Homebrew
- **Linux** → `references/linux.md` — Package managers, journal logs, old kernels, /var

---

## References

- `references/macos.md` — macOS-specific cleanup (iOS Simulators, SIP, ~/Library structure)
- `references/linux.md` — Linux-specific cleanup (apt/dnf/pacman, journal, kernels)