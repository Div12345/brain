# Knowledge Directory

Agents write discovered insights here. This is the **compounding memory** of the system.

## Structure

```
knowledge/
├── patterns/       # Recurring themes, behaviors, correlations
├── insights/       # Synthesized understanding from analysis
├── questions/      # Open questions worth investigating
└── summaries/      # Condensed views of larger analyses
```

## File Naming

`topic-YYYY-MM-DD.md` - e.g., `vault-analysis-2026-01-31.md`

## Required Frontmatter

```yaml
---
created: YYYY-MM-DD
agent: name
sources: [files read]
confidence: high|medium|low
supersedes: [previous-file.md]  # if updating old knowledge
---
```

## Linking Convention

Use `[[wikilinks]]` to cross-reference within this repo.
Use full paths for external references.

## Versioning

Don't edit old knowledge files. Create new ones with `supersedes:` in frontmatter.
Old files stay for history. Agents should read the latest (by date) for each topic.
