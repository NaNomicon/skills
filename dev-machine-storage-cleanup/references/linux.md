# Linux Storage Cleanup

Platform-specific guidance for Linux development machines.

## Linux Investigation

**System-wide analysis:**
```bash
df -h                                    # Disk usage
du -sh /* 2>/dev/null | sort -rh | head -20
du -sh /var/* 2>/dev/null | sort -rh | head -20
```

**User directory:**
```bash
du -sh ~/* 2>/dev/null | sort -rh | head -20
du -sh ~/.cache/* 2>/dev/null | sort -rh | head -20
du -sh ~/.local/share/* 2>/dev/null | sort -rh | head -20
```

---

## Package Manager Caches

### Debian/Ubuntu (apt/dpkg)

```bash
du -sh /var/cache/apt/archives           # Package cache
du -sh /var/lib/apt/lists                # Package lists

sudo apt clean                           # Clean package cache
sudo apt autoclean                       # Clean obsolete packages
sudo apt autoremove                      # Remove unused dependencies
```

### Fedora/RHEL (dnf)

```bash
du -sh /var/cache/dnf

sudo dnf clean all                       # Clean all caches
sudo dnf autoremove                      # Remove unused dependencies
```

### Arch Linux (pacman)

```bash
du -sh /var/cache/pacman/pkg

sudo pacman -Sc                          # Clean uninstalled package cache
sudo pacman -Scc                         # Clean all package cache (aggressive)
sudo pacman -Rns $(pacman -Qdtq)         # Remove orphaned packages
```

### openSUSE (zypper)

```bash
sudo zypper clean --all
```

---

## Journal Logs

Systemd journals can grow large over time.

```bash
journalctl --disk-usage                  # Check size
sudo journalctl --vacuum-size=500M       # Limit to 500MB
sudo journalctl --vacuum-time=7d         # Keep last 7 days only
```

---

## Old Kernels

Old kernel versions can accumulate.

**Debian/Ubuntu:**
```bash
dpkg --list | grep linux-image           # List installed kernels
sudo apt autoremove --purge              # Usually removes old kernels
```

**Fedora:**
```bash
sudo dnf remove --oldinstallonly         # Remove old kernels
```

**Arch:**
```bash
sudo pacman -Rns $(pacman -Qdtq)         # Orphans include old kernels
```

---

## /var Analysis

Common large directories in `/var`:

| Location | Typical Size | What It Is | Safe to Clean? |
|----------|--------------|------------|----------------|
| `/var/log` | 1-5 GB | System logs | Generally safe (archive old) |
| `/var/cache` | 1-5 GB | Package caches | Use package manager |
| `/var/tmp` | Varies | Temp files | Usually safe |
| `/var/lib/docker` | 5-50 GB | Docker data | Use `docker system prune` |
| `/var/lib/snapd` | 5-15 GB | Snap packages | `snap set system refresh.retain=2` |

---

## Snap Packages (Ubuntu)

Snaps keep multiple versions by default.

```bash
snap list --all                          # List snaps
snap set system refresh.retain=2         # Keep only 2 versions

# Remove old snap versions
for snap in $(snap list --all | grep disabled | awk '{print $1}'); do
  sudo snap remove "$snap"
done
```

---

## Flatpak

```bash
flatpak list --app                       # List installed
flatpak uninstall --unused               # Remove unused runtimes
```

---

## Common Linux Cache Locations

| Location | Typical Size | Cleanup |
|----------|--------------|---------|
| `~/.cache/` | 1-10 GB | Generally safe to clean |
| `~/.cache/pip` | 500 MB - 2 GB | `pip cache purge` |
| `~/.cache/npm` | 1-5 GB | `npm cache clean --force` |
| `~/.cache/yarn` | 1-5 GB | `yarn cache clean` |
| `~/.cache/go-build` | 500 MB - 2 GB | `go clean -cache` |
| `~/.cargo/` | 1-5 GB | `cargo cache -a` |
| `~/.local/share/Trash/` | Varies | Empty trash |

---

## Trash

```bash
du -sh ~/.local/share/Trash              # User trash size
rm -rf ~/.local/share/Trash/*            # Empty trash
```

---

## Temporary Files

```bash
du -sh /tmp /var/tmp 2>/dev/null

# These clear on reboot, but can clean manually:
sudo rm -rf /tmp/*                       # Be careful with running processes
sudo rm -rf /var/tmp/*
```

---

## Find Large Files

```bash
# Files > 100MB in home
find ~ -type f -size +100M 2>/dev/null | head -20

# Recently modified large files
find ~ -type f -mtime -7 -size +50M 2>/dev/null
```

---

## Safety Zones — Linux Specific

### Never Delete

- `/boot/` — Kernel and bootloader (system won't boot)
- `/etc/` — System configuration
- `/root/` — Root user home
- `/proc/`, `/sys/`, `/dev/` — Virtual filesystems

### Check Before Deleting

- `/var/lib/` — Application data, databases
- `/var/log/` — Logs may be needed for debugging
- `/usr/local/` — Manually installed software
- `~/.local/share/` — Application data

### System Protected

If `rm` fails with "Permission denied" even with sudo — check file attributes:
```bash
lsattr /path/to/file                     # Check attributes
chattr -i /path/to/file                  # Remove immutable flag (use caution)
```

---

## Recovery — Linux Specific

### If System Won't Boot

1. Boot from live USB
2. Mount the root partition
3. Check `/var/log/` for errors
4. Reinstall kernel if needed: `sudo apt install --reinstall linux-image-generic`

### If Package Manager Broken

**Debian/Ubuntu:**
```bash
sudo dpkg --configure -a
sudo apt --fix-broken install
```

**Arch:**
```bash
sudo pacman -Fy                           # Refresh file database
sudo pacman -Syyuu                        # Full upgrade
```