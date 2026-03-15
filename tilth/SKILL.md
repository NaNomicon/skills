---
name: tilth
description: Runs tilth CLI for structural code navigation — reads files with smart outlining, searches symbols/text/regex, finds files by glob, and maps codebases. Use instead of read/grep/find for all source code exploration.
---
# tilth — structural code intelligence (v0.5.1)

> **⚠️ MANDATORY: Use `tilth` instead of `read`, `grep`, `find`, `cat`**
>
> Every time you reach for `read`, ask: *can tilth do this?* It almost always can, and does it better — structural outlines, tree-sitter symbol search, and token-aware output in one call.
>
> **`read` is only acceptable when:** tilth is not installed, file is binary/image/PDF, or you need raw bytes.

---

## Quick Reference

| Task | Command |
|------|---------|
| Read a file | `tilth src/foo.py` |
| Read lines 100–200 | `tilth src/foo.py --section 100-200` |
| Read markdown section | `tilth README.md --section "## API"` |
| Force full content | `tilth src/foo.py --full` |
| Find symbol definition | `tilth handleAuth --scope src/` |
| Search literal text | `tilth "TODO: fix" --scope src/` |
| Regex search | `tilth "/pattern/" --scope src/` |
| Case-insensitive regex | `tilth "/pattern/i" --scope src/` |
| Find files by glob | `tilth "*.test.ts" --scope src/` |
| Codebase map | `tilth --map --scope src/` |
| Limit output tokens | `tilth handleAuth --scope src/ --budget 2000` |

---

## Query Auto-Classification

tilth has a single `<query>` argument. It classifies automatically — no mode flags needed:

| Priority | Pattern | Classification |
|----------|---------|----------------|
| 1 | `*`, `?`, `{`, `[` (no spaces) | **Glob** — file search |
| 2 | Contains `/` or starts with `./` `../` | **File path** — read file |
| 3 | Starts with `.` and resolves to a file | **File path** (dotfile) |
| 4 | Pure digits (`404`, `200`) | **Content search** |
| 5 | Looks like a filename (has extension) | **File path** if exists on disk |
| 6 | `/pattern/` or `/pattern/i` | **Regex search** |
| 7 | Identifier (starts with letter/`_`/`$`/`@`, no spaces) | **Symbol search** |
| 8 | Everything else | **Content search** |

If a path-like query doesn't resolve to a file, tilth falls through to symbol → content search.

---

## Commands

### Read a file

```bash
tilth <path>                          # smart view: full if small, outline if large
tilth <path> --section 45-89          # exact line range
tilth <path> --section "## Foo"       # markdown heading section
tilth <path> --full                   # force full content even if large
```

- Files **< ~6000 tokens**: full content with line numbers.
- Files **> ~6000 tokens**: structural outline with line ranges — functions, classes, imports. Use `--section` to drill into specific ranges.
- Outlined files append a `> Related: ...` hint listing imported/related files.

**Example — large file auto-outline:**

```
$ tilth src/server.rs
# src/server.rs (1,247 lines, ~18.2k tokens) [outline]

[1-15]    imports: hyper(3), tokio, serde_json, crate::config
[17-34]   struct ServerConfig
[36-89]   impl ServerConfig
  [38-52]   fn from_env() -> Result<Self>
  [54-89]   fn validate(&self) -> Result<()>
[91-340]  struct HttpServer
  [105-180] async fn start(&self) -> Result<()>
  [182-260] async fn handle_request(&self, req: Request) -> Response

> Related: src/config.rs, src/router.rs
```

Then drill in: `tilth src/server.rs --section 105-180`

### Search for symbols

```bash
tilth <symbol> --scope <dir>          # definitions first, then usages
```

- Uses **tree-sitter AST** to find definitions first, then usages — not just string matching.
- Expanded results include the full function/class body inline — often no separate read needed.
- Expanded definitions include a `── calls ──` footer with resolved callees (file, line, signature). Follow these to trace call chains without extra searches.
- A `── siblings ──` footer shows nearby definitions in the same scope.

**Example:**

```
$ tilth handleAuth --scope src/
# Search: "handleAuth" in src/ — 6 matches (2 definitions, 4 usages)

## src/auth.ts:44-89 [definition]
  [24-42]  fn validateToken(token: string)
→ [44-89]  export fn handleAuth(req, res, next)
  [91-120] fn refreshSession(req, res)

  44 │ export function handleAuth(req, res, next) {
  45 │   const token = req.headers.authorization?.split(' ')[1];
  ...
  89 │ }

── calls ──
  validateToken  src/auth.ts:24-42  fn validateToken(token: string): Claims | null
  refreshSession src/auth.ts:91-120  fn refreshSession(req, res)

## src/routes/api.ts:34 [usage]
→ [34]   router.use('/api/protected/*', handleAuth);
```

**Key:** The `── calls ──` footer gives you the exact file and line range for each callee. Drill directly with `tilth src/auth.ts --section 24-42` instead of searching again.

### Content and regex search

```bash
tilth "TODO: fix" --scope <dir>       # literal text search
tilth "/<regex>/" --scope <dir>       # regex search (wrap in slashes)
tilth "/<regex>/i" --scope <dir>      # case-insensitive regex
```

Content search finds literal strings, comments, and text. Regex uses full regex syntax inside `/slashes/`.

### Find files by glob

```bash
tilth "*.test.ts" --scope src/        # find test files
tilth "**/*.{json,toml}" --scope .    # brace expansion
```

Glob results include token estimates per file — use these to plan reads.

### Codebase map

```bash
tilth --map --scope src/              # structural overview
```

Shows directory tree with token estimates. **Use once per session** to orient yourself, then switch to targeted searches.

---

## Flags Reference

| Flag | Effect |
|------|--------|
| `--scope <dir>` | Directory to search within (default: `.`) |
| `--section <range>` | Line range (`45-89`) or markdown heading (`"## Foo"`) |
| `--budget <N>` | Max tokens in response — reduces detail to fit |
| `--full` | Force full output, override smart view |
| `--json` | Machine-readable JSON output |
| `--map` | Generate structural codebase map |
| `--edit` | Enable edit mode: hashline output + tilth_edit tool |

---

## Workflow

### The optimal pattern

1. **Search first.** `tilth handleAuth --scope src/` finds definitions with full source inline — often no read needed.
2. **Read outlined files in sections.** Note `[start-end]` line ranges from outlines, drill with `--section`.
3. **Follow `── calls ──` footers.** Don't search for callees — follow the file:line directly.
4. **Don't re-read expanded results.** If search showed the full body, answer from that output.

### Replacing grep/find/cat

| Shell command | tilth equivalent |
|---------------|------------------|
| `grep -rn "text" src/` | `tilth "text" --scope src/` |
| `grep -rnE "a\|b\|c" src/` | `tilth "/a\|b\|c/" --scope src/` |
| `grep -rni "text" src/` | `tilth "/text/i" --scope src/` |
| `find src/ -name "*.ts"` | `tilth "*.ts" --scope src/` |
| `cat src/foo.py` | `tilth src/foo.py` |
| `head -200 src/big.rs` | `tilth src/big.rs --section 1-200` |

---

## Pitfalls

### Classification surprises
- **Numbers** → content search, not symbol. `tilth 404` searches text.
- **Spaces** → content search. `tilth "import { X }"` is content, not symbol.
- **Existing filenames** → file read. `tilth README` reads the file.
- **Globs with spaces** aren't globs. `tilth "my file.*"` is content search.
- **Dotfiles** → file read. `tilth .env` reads `.env` if it exists.

### Common mistakes
- Using `--full` on a 2000-line file when `--section` would suffice → wastes tokens.
- Re-reading a file already shown in search output → wastes tokens.
- Running `grep` in bash when `tilth` does the same with structure → wastes calls.
- Not using `--budget` for quick lookups → unbounded output.
- Using `--map` repeatedly → expensive, use once then search.

---

## Decision Tree

```
What do you need?
├── Understanding a symbol (function, class, variable)?
│   └── tilth <symbol> --scope <dir>
│       └── Follow ── calls ── footers for callees
├── Reading a file?
│   ├── Small/medium → tilth <path>              (auto full)
│   ├── Large file → tilth <path>                (auto outline)
│   │   └── Need specific lines → tilth <path> --section 45-89
│   └── Markdown section → tilth <path> --section "## Heading"
├── Searching for text/patterns?
│   ├── Literal → tilth "text" --scope <dir>
│   ├── Regex → tilth "/pattern/" --scope <dir>
│   └── Case-insensitive → tilth "/pattern/i" --scope <dir>
├── Finding files?
│   ├── By extension → tilth "*.test.ts" --scope src/
│   └── By path → tilth "src/**/*.rs" --scope .
└── First time in codebase?
    └── tilth --map --scope src/    (once, then search)
```
