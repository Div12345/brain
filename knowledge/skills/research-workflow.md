# Skill: Research Workflow

> Triggered when: paper analysis, literature review, methodology questions

## When to Use

- User mentions a paper, author, or methodology
- User is working on `[[arterial_analysis]]` ML methodology
- User says "research", "paper", "literature", "find papers"

## Workflow Steps

### 1. Check Existing Knowledge
```
1. Search Zotero (mcp__zotero__zotero_search_items)
2. Search Obsidian literature notes (mcp__obsidian__obsidian_global_search)
3. Check knowledge/patterns/ for prior analysis
```

### 2. If Paper Not Found
```
1. Offer to search (mcp__paper-search__search_semantic_scholar)
2. Download if available (mcp__paper-search__download_paper)
3. Create literature note in Obsidian
```

### 3. Synthesize
```
1. Extract key claims
2. Connect to existing notes ([[wikilinks]])
3. Identify methodology patterns
4. Note open questions
```

### 4. Store Pattern
```
1. If new methodology insight → add to knowledge/patterns/
2. If resolves open question → update session-handoff.md
```

## Anti-Patterns (Don't Do)

- Don't summarize without reading
- Don't claim expertise on genuinely uncertain methodology questions
- Don't create notes for papers user hasn't shown interest in

## Success Metrics

| Metric | Target |
|--------|--------|
| Relevant papers surfaced | User says "useful" |
| Avoided re-searching | Checked Zotero/Obsidian first |
| Connected to existing work | Used wikilinks |

## Example Usage

```
User: "I'm trying to figure out nested CV with stability selection"

Claude:
1. Search Zotero for "stability selection" → found Meinshausen 2009
2. Search Obsidian → found Literature Notes/Meinshausen_2009_Stability Selection.md
3. Read existing note
4. Surface: "You have a literature note on this. Key insight: [X].
   Open question in your notes: [Y]. Want me to search for papers
   that address [Y]?"
```

## Last Used

- 2026-02-02: Analyzed stability selection papers for arterial_analysis

## Effectiveness Log

| Date | Invoked By | Useful? | Notes |
|------|------------|---------|-------|
| (to be filled after use) | | | |
