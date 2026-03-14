# macOS Storage Cleanup

Platform-specific guidance for macOS development machines.

## macOS Investigation

**System-wide analysis:**
```bash
du -sh /Library/* 2>/dev/null | sort -rh | head -20
du -sh ~/Library/* 2>/dev/null | sort -rh | head -20
```

**Developer-specific locations:**
```bash
du -sh ~/Library/Developer 2>/dev/null
du -sh ~/Library/Application\ Support 2>/dev/null
du -sh ~/Library/Caches 2>/dev/null
```

---

## iOS Simulators — Often 20-100 GB

**List installed runtimes:**
```bash
xcrun simctl list runtimes
```

**Delete runtimes (if unused):**
```bash
xcrun simctl runtime delete all          # Remove all
xcrun simctl runtime delete "iOS-18-0"   # Remove specific
```

**⚠️ The SIP Problem:**
- `xcrun simctl runtime delete` only unregisters runtimes
- Actual `.asset` files remain in `/System/Library/AssetsV2/`
- Files are SIP-protected
- Requires Recovery Mode to fully delete

**To fully remove (requires SIP disable):**
1. Restart to Recovery (Apple Silicon: hold power button → Options)
2. Terminal: `csrutil disable`
3. Restart normally: `sudo rm -rf /System/Library/AssetsV2/com_apple_MobileAsset_iOSSimulatorRuntime/*.asset`
4. Recovery again: `csrutil enable`

---

## ~/Library Structure

The `~/Library` folder often contains 50-150GB.

| Location | Typical Size | What It Is | Safe to Clean? |
|----------|--------------|------------|----------------|
| `Caches/` | 2-10 GB | App caches | Generally safe |
| `Developer/Xcode/DerivedData/` | 1-10 GB | Xcode build cache | Safe to delete |
| `Application Support/` | 10-50 GB | App data | ⚠️ Check per app |
| `Containers/` | 10-30 GB | Sandboxed app data | Deleting = reset app |
| `CloudStorage/` | 10-50 GB | iCloud/Google Drive | ❌ User data |
| `Android/sdk` | 10-25 GB | Android SDK | ✅ If not doing Android |
| `pnpm/store` | 5-15 GB | pnpm cache | `pnpm store prune` |
| `Parallels/` | 5-20 GB | VM data | Delete unused VMs |

---

## /Library — System-wide

| Location | Typical Size | Safe to Remove? |
|----------|--------------|-----------------|
| `Application Support/Adobe` | 2-4 GB | Only if no Adobe apps |
| `Developer/CommandLineTools` | 1-2 GB | ❌ Keep for builds |
| `Frameworks/Python.framework` | 1 GB | ✅ If using pyenv/uv |
| `Frameworks/GStreamer.framework` | 500 MB - 1 GB | Check if OBS/video apps need it |
| `Java` | 300-500 MB | ✅ If not developing Java |
| `Updates/*` | Varies | Some are SIP-protected |

---

## /System/Library — SIP Protected

**⚠️ Most files are protected by System Integrity Protection.**

| Location | Typical Size | Can Delete? |
|----------|--------------|-------------|
| `AssetsV2/com_apple_MobileAsset_iOSSimulatorRuntime` | 20-50 GB | Requires disabling SIP |

If `rm` fails with "Operation not permitted" — it's SIP-protected. Don't force.

---

## Homebrew Cleanup

```bash
brew cleanup --prune=all                 # Remove old versions
brew autoremove                          # Remove unused dependencies
```

**Check Homebrew size:**
```bash
du -sh ~/Library/Caches/Homebrew
du -sh /opt/homebrew 2>/dev/null || du -sh /usr/local/Homebrew 2>/dev/null
```

---

## Common macOS Cache Locations

| Location | Typical Size | Cleanup |
|----------|--------------|---------|
| `~/Library/Caches/go-build` | 500 MB - 2 GB | Safe to delete |
| `~/Library/Caches/Homebrew` | 500 MB - 2 GB | `brew cleanup` |
| `~/Library/Caches/pip` | 100 MB - 1 GB | `pip cache purge` |
| `~/Library/Caches/ms-playwright` | 500 MB - 2 GB | Safe if not testing |
| `~/Library/Caches/BraveSoftware` | 500 MB - 2 GB | Clear in browser |
| `~/Library/Developer/Xcode/DerivedData` | 1-10 GB | Safe to delete |

---

## IDE/Editor Data (if unused)

- Cursor: `~/Library/Application Support/Cursor`
- VS Code: `~/Library/Application Support/Code`
- Zed: `~/Library/Application Support/Zed`
- JetBrains: `~/Library/Application Support/JetBrains`

---

## Checking Rarely Used Apps

```bash
mdfind 'kMDItemContentType == "com.apple.application-bundle"' -onlyin /Applications | \
  while read app; do
    name=$(basename "$app" .app)
    lastUsed=$(mdls -name kMDItemLastUsedDate -raw "$app" 2>/dev/null)
    size=$(du -sh "$app" 2>/dev/null | cut -f1)
    echo -e "$size\t$lastUsed\t$name"
  done | sort -t$'\t' -k2
```

---

## Safety Zones — macOS Specific

### Never Delete

- `/System/*` — macOS core, SIP-protected
- `/Library/Apple/*` — Apple system frameworks
- `~/Library/Keychains/` — Keychain data (irreplaceable)

### Check Before Deleting

- `~/Library/Application Support/` — May contain user data
- `~/Library/Caches/` — Some apps store state here
- `~/Library/Containers/` — Deleting resets sandboxed apps

---

## Recovery — macOS Specific

### If App Won't Launch

1. Clear caches: `~/Library/Caches/<app>/`
2. Remove preferences: `~/Library/Preferences/<app>*`
3. Remove container: `~/Library/Containers/<app>/` (full reset)
4. Reinstall app

### If System Acts Weird

1. Reboot first — many issues resolve
2. Run Disk Utility → First Aid
3. Reset PRAM/NVRAM: `Cmd+Option+P+R` at boot
4. Safe boot: Hold Shift at boot, then reboot normally