---
name: analyze-obsidian-vault-patterns
priority: 4
estimated_tokens: 40000
mode: autonomous
timeout: 30m
backend: desktop
model_hint: sonnet
tags: [obsidian, analysis, knowledge]
depends_on: []
ce_aware: true
---

# Analyze Obsidian Vault Structure and Patterns

## Goal
Analyze the Obsidian vault at ~/vault/ to understand its structure, identify patterns in note-taking, and suggest improvements for knowledge management.

## Analysis Tasks
1. **Structure mapping** — Count notes by folder, identify the organizational hierarchy
2. **Link analysis** — Find the most connected notes (hub notes), identify orphan notes with no links
3. **Tag usage** — What tags exist? Which are most used? Are there inconsistencies?
4. **Recent activity** — What notes were modified in the last 7 days? What topics are active?
5. **Template patterns** — Are there recurring structures? Could templates help?

## IMPORTANT: Use Desktop's Obsidian MCP Tools
Claude Desktop runs on Windows and has Obsidian MCP tools. Use these instead of bash/file commands:
- `obsidian_list_notes` — List all notes in the vault
- `obsidian_read_note` — Read a specific note's content
- `obsidian_global_search` — Search across all notes
- `obsidian_manage_tags` — Get tag information
- `obsidian_manage_frontmatter` — Read note metadata

Do NOT use bash commands or file paths - the vault is accessed via Obsidian REST API on localhost:27124.

## Output
Write findings to stdout with:
- Vault statistics (note count, folder structure)
- Top 10 hub notes and orphan notes
- Tag analysis with suggested consolidation
- Recommendations for better knowledge organization
