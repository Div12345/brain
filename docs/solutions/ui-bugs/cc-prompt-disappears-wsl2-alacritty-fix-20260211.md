---
module: System
date: 2026-02-11
problem_type: ui_bug
component: tooling
symptoms:
  - "Claude Code keyboard prompt disappears in long conversations"
  - "Must zoom out to tiny size to see the input prompt"
  - "TUI rendering degrades as conversation grows"
root_cause: config_error
resolution_type: environment_setup
severity: high
tags: [claude-code, wsl2, windows-terminal, alacritty, tui-rendering, conpty]
---

# Troubleshooting: Claude Code Prompt Disappears in Long Conversations on WSL2

## Problem
When running Claude Code on WSL2 through Windows Terminal, the keyboard input prompt becomes invisible as conversations grow longer. The user must zoom out to extremely small sizes to see it again, making CC unusable for extended sessions.

## Environment
- Module: System (terminal configuration)
- Platform: WSL2 (Ubuntu-24.04) on Windows 11
- Terminal: Windows Terminal (before fix), Alacritty 0.16.1 (after fix)
- Affected Component: Claude Code TUI rendering via ConPTY bridge
- Date: 2026-02-11

## Symptoms
- CC keyboard prompt/input area disappears as conversation length grows
- Must zoom terminal to very small size to see the prompt again
- Problem worsens progressively with conversation length
- Ctrl+L (redraw) provides temporary relief

## What Didn't Work

**Attempted Solution 1:** Investigated OMC HUD statusline as potential cause
- **Why it failed:** HUD was outputting an error (`[OMC] run /omc-setup to install properly`) but this was only when run without stdin. Inside CC, the HUD works fine — renders a single line. Not the cause.

**Attempted Solution 2:** Windows Terminal settings adjustments (AtlasEngine renderer, reduced history size)
- **Why it failed:** The root cause is in the ConPTY bridge layer between Windows Terminal and WSL2, not in WT's settings. CC produces ~4000-6700 scroll events/sec which overwhelms the bridge.

## Solution

Switch from Windows Terminal to **Alacritty for Windows** — a GPU-accelerated terminal emulator that handles high-frequency TUI redraws much better.

**Install:**
```
scoop install alacritty
# Or use existing installation at C:\Program Files\Alacritty\alacritty.exe
```

**Config file** at `%APPDATA%\alacritty\alacritty.toml`:
```toml
# Alacritty config — WSL2 + Claude Code

[window]
padding = { x = 4, y = 4 }
dynamic_padding = true

[scrolling]
history = 5000

[font]
size = 11.0

[font.normal]
family = "Cascadia Mono"

[terminal]
osc52 = "CopyPaste"

[terminal.shell]
program = "wsl.exe"
args = ["-d", "Ubuntu-24.04"]
```

**Critical gotchas:**
1. **Distro name must be exact** — use `wsl -l -v` to find it. `Ubuntu` != `Ubuntu-24.04`. Wrong name causes Alacritty to flash and exit silently.
2. **Font must exist on Windows** — missing font causes immediate crash with no visible error. Check with: `Add-Type -AssemblyName System.Drawing; (New-Object System.Drawing.Text.InstalledFontCollection).Families`
3. **Config format changed** — Alacritty 0.16+ uses TOML, not YAML. Old `[shell]` is now `[terminal.shell]`.
4. **No tabs/splits** — Alacritty is minimal by design. Use tmux inside WSL2 for panes.

## Why This Works

1. **Root cause:** Windows Terminal uses ConPTY (Windows Pseudo Console) as a bridge between WSL2's Linux PTY and the Windows rendering layer. CC's Ink-based TUI produces ~4000-6700 scroll events/sec. ConPTY struggles to relay these faithfully, causing the viewport to lose track of the cursor/prompt position in long conversations.

2. **Why Alacritty helps:** Alacritty also uses ConPTY (it's a Windows app), but its GPU-accelerated OpenGL renderer processes the high-frequency output much faster than Windows Terminal's renderer. The frame pipeline is: ConPTY -> Alacritty's render loop -> GPU. This keeps the viewport properly synced with CC's cursor position.

3. **Escalation path:** If Alacritty still has issues in very long sessions, the nuclear option is running a Linux terminal (Alacritty or Ghostty) inside WSL2 via WSLg, which bypasses ConPTY entirely. The CC team specifically recommends Ghostty for its DEC 2026 synchronized output support (zero flicker).

## Prevention

- Use Alacritty (or another GPU-accelerated terminal) instead of Windows Terminal for CC on WSL2
- Use `/compact` proactively in long CC conversations to reduce TUI rendering load
- Use `Ctrl+L` to force screen redraw if prompt disappears
- Pin Alacritty to taskbar for quick access
- Run `/terminal-setup` inside CC in Alacritty to configure Shift+Enter

## Related Issues

- See also: [CC Scrolling Fix for WSL + Windows Terminal](../2026-02-07-claude-code-scrolling-wsl-windows-terminal.md) — related scrollback/mouse capture fixes for the same environment
- GitHub: [TUI rendering broken in WSL2 #16501](https://github.com/anthropics/claude-code/issues/16501)
- GitHub: [Terminal rendering broken v2.0.73 Windows #14761](https://github.com/anthropics/claude-code/issues/14761)
- GitHub: [CC TUI ~4000-6700 scroll events/sec](https://youtrack.jetbrains.com/projects/IJPL/issues/IJPL-226186)
- CC dev recommendation: [Ghostty for zero flicker](https://news.ycombinator.com/item?id=46699072)
