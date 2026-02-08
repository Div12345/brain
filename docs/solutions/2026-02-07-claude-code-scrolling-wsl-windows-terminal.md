---
title: Claude Code Scrolling Fix for WSL + Windows Terminal
category: ui-bugs
tags: [claude-code, wsl, windows-terminal, tmux, scrolling, alternate-screen-buffer]
module: terminal-configuration
symptoms:
  - Input box captures scroll instead of terminal
  - Cannot scroll back to see previous Claude messages
  - Mouse wheel scrolls input history, not output
  - Lost scrollback after TUI app runs
date: 2026-02-07
---

# Claude Code Scrolling Fix for WSL + Windows Terminal

## Problem Summary

When running Claude Code on WSL through Windows Terminal, scrolling doesn't work properly:
- Mouse wheel scrolls through the input box history instead of the terminal output
- Cannot scroll back to see previous messages/responses
- After Claude Code exits, terminal scrollback is cleared

## Root Causes

1. **Alternate Screen Buffer**: Claude Code's TUI (built on Ink/React) uses the terminal's alternate screen buffer, which doesn't preserve scrollback
2. **Mouse Event Capture**: The TUI captures mouse events for its input box, preventing native terminal scroll
3. **Insufficient History**: Default Windows Terminal scrollback may be too small

## Solution

### 1. Windows Terminal - Increase Scrollback

Edit Windows Terminal settings (`settings.json`):

```json
{
    "guid": "{your-wsl-profile-guid}",
    "historySize": 50000,
    "name": "Ubuntu-24.04",
    "source": "Microsoft.WSL"
}
```

Path: `%LOCALAPPDATA%\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json`

### 2. Bash Wrapper - Disable Alternate Screen

Add to `~/.bashrc`:

```bash
# Fix: Disable alternate screen buffer for TUI apps (enables scrollback)
claude() {
    printf '\e[?1049l'
    command claude "$@"
    printf '\e[?1049l'
}
```

The escape sequence `\e[?1049l` disables alternate screen buffer switching.

### 3. Tmux Configuration (if using tmux)

Create/edit `~/.tmux.conf`:

```tmux
# Enable mouse support
set -g mouse on

# Large scrollback buffer
set -g history-limit 50000

# Disable alternate screen buffer for TUI apps
set -ga terminal-overrides ',xterm*:smcup@:rmcup@'
set -ga terminal-overrides ',screen*:smcup@:rmcup@'

# Better scroll behavior
bind -n WheelUpPane if-shell -F -t = "#{mouse_any_flag}" "send-keys -M" "if -Ft= '#{pane_in_mode}' 'send-keys -M' 'select-pane -t=; copy-mode -e; send-keys -M'"
bind -n WheelDownPane select-pane -t= \; send-keys -M

# Vi keys in copy mode
setw -g mode-keys vi
```

The `smcup@:rmcup@` overrides disable alternate screen for apps inside tmux.

## Verification

1. Open new terminal tab (to load Windows Terminal changes)
2. Source bashrc: `source ~/.bashrc`
3. If using tmux: `tmux kill-server && tmux new -s main`
4. Run `claude` and generate output
5. Scroll with mouse wheel or Shift+PageUp/PageDown

## Key Learnings

| Issue | Root Cause | Fix |
|-------|------------|-----|
| Lost scrollback | Alternate screen buffer | Escape sequence `\e[?1049l` |
| Short history | Default buffer size | Increase `historySize` to 50000 |
| Tmux no scroll | Mouse disabled by default | `set -g mouse on` |
| TUI clears buffer | smcup/rmcup sequences | Override in terminal-overrides |

## Related Issues

- [GitHub #21386](https://github.com/anthropics/claude-code/issues/21386) - Option to disable mouse capture
- [GitHub #23581](https://github.com/anthropics/claude-code/issues/23581) - Add option to disable mouse tracking in TUI

## Prevention Checklist

- [ ] New WSL setup: Add historySize to Windows Terminal profile
- [ ] New machine: Copy tmux.conf with alternate screen overrides
- [ ] Add claude wrapper to dotfiles repo
