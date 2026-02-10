# Obsidian Vault Delegation: Quick Reference

**TL;DR:** Use Claude Desktop for Obsidian operations. Direct access via Claude Code is fastest.

---

## Decision Tree

```
Need to read/write Obsidian vault?
│
├─ Currently in Claude Code? → Use direct MCP (fastest)
│  │ mcp__obsidian__obsidian_read_note("path/to/note.md")
│  │ mcp__obsidian__obsidian_update_note(...)
│  │ mcp__obsidian__obsidian_global_search(...)
│
├─ Need to delegate to other interface?
│  │
│  ├─ Claude Desktop available? → Use Desktop (reliable)
│  │  │ mcp__claude-desktop__claude_desktop_send(
│  │  │     message="Read X.md...",
│  │  │     wait_for_response=true,
│  │  │     timeout=30
│  │  │ )
│  │
│  ├─ Need quick operation via Gemini CLI?
│  │  │ ⚠️ WARNING: Use only for simple reads
│  │  │ gemini -p "Read Dashboard/State.md" [might timeout]
│  │
│  └─ Need OpenCode help? → Use for code, NOT vault
│     │ ❌ Don't delegate vault ops to OpenCode
│     │ ✅ Use for: linting, refactoring, analysis
│
└─ If uncertain → Use Claude Desktop + Desktop Desktop connector toggle first
```

---

## Interface Reliability Matrix

| Task | Claude Code | Desktop | OpenCode | Gemini CLI |
|------|:---:|:---:|:---:|:---:|
| Read note | ✅✅ | ✅ | ❌ | ⚠️ |
| Write note | ✅✅ | ✅ | ❌ | ⚠️ |
| Search vault | ✅✅ | ✅ | ❌ | ⚠️ |
| Manage tags | ✅✅ | ✅ | ❌ | ⚠️ |
| List notes | ✅✅ | ✅ | ❌ | ⚠️ |

**Legend:** ✅✅ = Direct + fast | ✅ = Delegated, works | ⚠️ = Timeout risk | ❌ = Doesn't work

---

## Patterns

### Pattern 1: Direct Read (Claude Code)
```python
from mcp__obsidian__obsidian_read_note import obsidian_read_note

content = obsidian_read_note(filePath="Dashboard/State.md")
print(content['content'])
```
**Speed:** <100ms | **Reliability:** 99.9% | **Use for:** Immediate needs

---

### Pattern 2: Delegate to Desktop
```python
from mcp__claude-desktop__claude_desktop_send import claude_desktop_send

response = claude_desktop_send(
    message="Read Dashboard/State.md and summarize the current status",
    wait_for_response=True,
    timeout=30
)
print(response['response'])
```
**Speed:** 1-3s | **Reliability:** 98% | **Use for:** Desktop context needed, or freeing up Claude Code

---

### Pattern 3: Setup Desktop First (Session Start)
```python
# Before first vault operation in session
from mcp__claude-desktop__claude_desktop_toggle_connector import toggle
from mcp__claude-desktop__claude_desktop_reload_mcp import reload

toggle(connector_name="obsidian", enable=True)
reload()

# Now Desktop can access obsidian MCP
```
**When:** Once per Desktop session | **Why:** Ensures obsidian connector is active

---

## Common Operations

### Read a Note
```python
# Claude Code (fastest)
mcp__obsidian__obsidian_read_note(filePath="path/to/note.md")

# Claude Desktop (if delegating)
desktop_send(message="Read path/to/note.md and tell me the content")
```

### Search Vault
```python
# Claude Code
mcp__obsidian__obsidian_global_search(
    query="ADHD",
    searchInPath="Projects/"
)

# Claude Desktop
desktop_send(message="Search the vault for 'ADHD' in the Projects folder")
```

### Update State
```python
# Claude Code (atomic)
mcp__obsidian__obsidian_update_note(
    targetType="filePath",
    targetIdentifier="Dashboard/State.md",
    modificationType="wholeFile",
    wholeFileMode="overwrite",
    content="# New state\n\nUpdated: 2026-02-10"
)

# Claude Desktop (if Desktop needs to update)
desktop_send(message="Update Dashboard/State.md with: ...")
```

### Manage Tags
```python
# Claude Code
mcp__obsidian__obsidian_manage_tags(
    filePath="Projects/phd/session-2026-02-10.md",
    operation="add",
    tags=["session", "2026-02-10", "active"]
)
```

---

## Troubleshooting

### "Obsidian MCP error" in Claude Desktop?
```bash
# Step 1: Toggle connector off and on
mcp__claude-desktop__claude_desktop_toggle_connector(
    connector_name="obsidian",
    enable=False
)
# Wait 2 seconds
mcp__claude-desktop__claude_desktop_toggle_connector(
    connector_name="obsidian",
    enable=True
)

# Step 2: Reload MCP config
mcp__claude-desktop__claude_desktop_reload_mcp()

# Step 3: Retry operation
```

### OpenCode can't find Obsidian MCP?
**Expected behavior.** OpenCode runs in isolated environment. Use Claude Code or Desktop instead.

### Gemini CLI timeout on vault ops?
**Expected behavior.** Gemini optimized for fast text ops, not I/O. Use 120+ second timeout or delegate to Desktop.

---

## Performance Notes

| Operation | Time | Best Interface |
|-----------|------|---|
| Read single note | ~50ms | Claude Code |
| Write single note | ~100ms | Claude Code |
| Search vault (5 matches) | ~200ms | Claude Code |
| Read via Desktop | ~1-2s | Desktop |
| Vault setup (toggle + reload) | ~500ms | Desktop |
| Gemini spawn for task | ~3-5s | Gemini CLI |

---

## Rules of Thumb

1. **Same session, same interface?** Use direct MCP (Claude Code)
2. **Need Desktop context?** Delegate to Desktop via `claude_desktop_send()`
3. **Quick question on CLI?** Use Gemini CLI, but expect 1-3s latency
4. **OpenCode involved?** Don't ask it to read vault; ask for code analysis
5. **Vault state changes?** Write via Claude Code or Desktop (both reliable)

---

## See Also

- Full test results: `2026-02-10-delegation-test-obsidian-vault-operations.md`
- Obsidian vault rules: `Meta/Vault Rules.md` (in vault)
- Dashboard/State.md: Current session state
