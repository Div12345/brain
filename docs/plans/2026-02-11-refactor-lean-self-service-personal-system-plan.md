---
title: Lean Self-Service Personal System Redesign
type: refactor
date: 2026-02-11
status: phase-4-complete
principles: [self-service, programmatic, lean, compounding, agent-optional]
---

# Lean Self-Service Personal System Redesign

## The Deeper Problem

It's not "cooking needs fixing" or "day planner is unused." The deeper problem is: **the system stores prose but the user needs queryable state.** Every domain has the same structural gap:

| Domain | What's stored | What's needed |
|--------|-------------|---------------|
| Cooking | Prose list of 75 ingredients | "What can I make?" (computed from inventory × recipes) |
| Day planning | Free-form daily notes | "What should I do now?" (computed from energy × tasks × time) |
| Research | Session logs + notes | "What have I tried? What's next?" (computed from experiments × results) |
| Brain repo | Task files + context docs | "What's the highest-impact action?" (computed from priority × blockers × capacity) |

**In every case**: raw data exists, but the "what should I do" layer is manually curated by an agent instead of computed from structured data.

---

## Universal Architecture

Every domain follows the same 5-layer stack:

```
┌─────────────────────────────────────┐
│  5. VIEW — "What should I do?"      │  ← Dataview queries, Command Centers
│     Computed, never hand-written     │
├─────────────────────────────────────┤
│  4. RULES — Matching / filtering    │  ← "Recipe needs X, Y, Z ingredients"
│     Encoded as frontmatter + logic  │     "Task needs Low energy + 15 min"
├─────────────────────────────────────┤
│  3. REGISTRY — Structured data      │  ← Notes with typed properties
│     Each entity = a note w/ schema  │     Queryable by Dataview
├─────────────────────────────────────┤
│  2. CAPTURE — Fast structured input │  ← Templater templates, < 30 sec
│     Adds/modifies registry entries  │
├─────────────────────────────────────┤
│  1. FEEDBACK — Learning loop        │  ← "I ate X" → update inventory
│     Each interaction updates state  │     "Experiment failed" → update log
└─────────────────────────────────────┘
```

**The principle**: Views are ALWAYS computed from Registry + Rules. Never manually written. If you see a hand-curated list, that's a design bug.

---

## Layer 3: The Registry Problem (Queryable Entities)

This is the foundation. Everything else depends on getting this right.

### Design Options for Obsidian

**Option A: One note per entity**
```
Projects/cooking/ingredients/zhoug-sauce.md
---
name: Zhoug Sauce
brand: Trader Joe's
location: fridge
category: sauce
have: true
qty: 8oz
always_stock: true
---
```

- Pro: First-class Obsidian citizen. Backlinks show which recipes use it. Properties UI makes editing trivial (toggle `have` checkbox). Dataview queries work perfectly.
- Con: 75 ingredient files feels like a lot. But Obsidian handles thousands of notes fine.

**Option B: Single file with inline Dataview fields**
```
- Zhoug Sauce (TJ's) [location:: fridge] [have:: true] [category:: sauce]
```

- Pro: Everything visible in one file. Quick visual scan.
- Con: Inline fields are fragile. No backlinks. No Properties UI. Editing means finding the right line.

**Option C: YAML data file + Dataview JS**
```json
// cooking-data.json
{"ingredients": [{"name": "Zhoug", "have": true, ...}]}
```

- Pro: Proper structured data. Easy for scripts to read/write.
- Con: Not Obsidian-native. No links, no Properties UI, needs JS.

### Decision: Option A (one note per entity) everywhere

**Why**: Obsidian is a note-first tool. Fighting it with JSON or inline hacks creates a system that's "lean" but fragile. One-note-per-entity means:

1. **Properties panel** — toggle `have` with a checkbox click. No editing markdown.
2. **Backlinks** — open Zhoug Sauce → see every recipe and meal log that references it
3. **Dataview** — `FROM "Projects/cooking/ingredients" WHERE have = true` just works
4. **Templates** — `(TEMPLATE) Ingredient.md` creates a new one in 10 seconds
5. **Mobile** — Obsidian mobile Properties panel is touch-friendly

**The "75 files" objection**: You never browse the `ingredients/` folder. You interact through Views (Dataview queries in Command Center). The files are a database, not a reading list.

### This pattern applies universally:

| Domain | Entity folder | Note = | Key properties |
|--------|--------------|--------|---------------|
| Cooking | `ingredients/` | One ingredient | `have`, `location`, `category`, `always_stock` |
| Cooking | `recipes/` | One recipe | `ingredients` (list), `energy`, `time`, `tags` |
| Research | `experiments/` | One experiment | `target`, `method`, `status`, `r2`, `mae` |
| Day planning | `Daily/` (already exists) | One day | `energy`, `sleep`, `tasks` |
| Brain repo | `tasks/` (already exists) | One task | `priority`, `status`, `blockers`, `energy_needed` |

**Same architecture. Same query patterns. Different domains.**

---

## Layer 4: Rules (The Matching Logic)

Rules answer: "Given this state, what's actionable?"

### Cooking: "What can I make?"

Each recipe note has an `ingredients` property (list of links to ingredient notes):

```yaml
# recipes/potato-tacos.md
---
name: Potato Tacos
energy: low
time: 15
ingredients:
  - "[[taco-shells]]"
  - "[[potatoes]]"
  - "[[red-onion]]"
  - "[[cheese-shredded]]"
  - "[[hot-sauce]]"
always_available:
  - "[[salt]]"
  - "[[oil]]"
---
```

Dataview query in Command Center:
```dataview
TABLE energy, time
FROM "Projects/cooking/recipes"
WHERE all(ingredients, (i) =>
  contains(this.file.outlinks, i) AND
  meta(i).have = true
)
SORT energy ASC
```

This **computes** "what can I make" from (inventory state × recipe requirements). No agent needed. Updates instantly when you toggle an ingredient's `have` property.

### Day planning: "What should I do?"

Tasks have `energy_needed` property. Daily note has `energy` property.

```dataview
TABLE energy_needed, est_minutes
FROM "tasks/pending"
WHERE energy_needed <= this.energy
SORT priority DESC
```

Open today's daily note → set energy level (1-5) → see tasks that match.

### Research: "What have I tried?"

```dataview
TABLE target, method, status, r2
FROM "Projects/arterial analysis/experiments"
WHERE target = "cSBP"
SORT date DESC
```

Open Command Center → see all experiments for current target → know what's been done and what worked.

### Brain repo: "What's highest impact?"

```dataview
TABLE priority, status, blockers
FROM "tasks/pending"
WHERE !blockers OR length(blockers) = 0
SORT priority ASC
```

---

## Layer 2: Capture (< 30 Seconds)

Every capture template follows: **pre-fill everything possible, user only adds the delta.**

### Grocery Trip Template
```markdown
<%*
// Get all ingredients where always_stock = true
const items = dv.pages('"Projects/cooking/ingredients"')
  .where(p => p.always_stock === true)
  .sort(p => p.location);
-%>
# Grocery Trip — <% tp.date.now("YYYY-MM-DD") %>

## Check what you bought:
<% items.forEach(item => { %>
- [ ] [[<%= item.file.name %>]] (<%= item.location %>)
<% }) %>

## New items (add below):
-

<%*
// On template close: for each checked item, set have = true
// This requires Templater + MetaEdit or Dataview JS
-%>
```

**Interaction**: Open template → see always-stock items as checklist → check what you bought → properties auto-update.

### Daily Note Template
```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
energy:
sleep:
---
# <% tp.date.now("dddd, MMMM D") %>

## Plan
> Energy: (set above, tasks auto-filter below)

```dataview
TASK FROM "tasks/pending"
WHERE energy_needed <= this.energy AND !completed
SORT priority ASC
LIMIT 5
```

## Log
- <% tp.date.now("HH:mm") %>

## Meals
-

## End
>
```

### Experiment Log Template
```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
target:
method:
status: running
r2:
mae:
script:
notebook:
---
# Experiment:

## Hypothesis
>

## Setup
- Script: `scripts/`
- Data: `data/processed/`

## Results
(fill when complete)

## What I Learned
>
```

---

## Layer 5: Views (Command Centers)

Command Centers become **pure view layers** — no hand-written content except the structure. All data is Dataview-computed.

### Cooking Command Center

```markdown
# Cooking

## What Can I Make Now
```dataview (recipes where all ingredients have = true, sorted by energy)```

## Quick Always-Options
- Dosa + pickle + yogurt
- Smoothie (frozen fruit + milk + chia)
- Naan plate (frozen naan + hummus + zhoug + pickled jalapeños)

## Fridge (have now)
```dataview (ingredients WHERE location = "fridge" AND have = true)```

## Need to Restock
```dataview (ingredients WHERE have = false AND always_stock = true)```

## Recent Meals
```dataview (meals from last 7 daily notes)```

## [[Projects/cooking/shopping|Shopping Rules]] · [[Projects/cooking/recipes|All Recipes]]
```

### Daily Dashboard

```markdown
# Today

## Energy-Matched Tasks
```dataview (pending tasks WHERE energy_needed <= today's energy)```

## Schedule
```dataview (calendar events if integrated, else manual)```

## Open Loops
```dataview (tasks carried forward from yesterday, uncompleted)```
```

---

## Layer 1: Feedback (Compounding)

Each interaction feeds back into the registry:

| Action | Updates | How |
|--------|---------|-----|
| Bought groceries | Ingredient `have: true` | Toggle property in note |
| Used something up | Ingredient `have: false` | Toggle property in note |
| Ate a meal | Daily note meal log | Tag `#meal` with recipe link |
| Ran experiment | Experiment note `status: complete` | Fill in results |
| Finished task | Task note `status: done` | Move to completed/ |
| Logged energy | Daily note `energy: 3` | Fill property |

**The compounding part**: Over time, you accumulate:
- Meal frequency data → "You eat dosa 5x/week, tacos 1x"
- Energy patterns → "You're high-energy Tue/Thu, low Mon/Fri"
- Experiment history → "Ridge regression consistently outperforms for cSBP"
- Task completion patterns → "You complete morning tasks, carry forward evening ones"

Agents can mine this data for insights. But the system works without them because the Views are computed from structured data, not agent analysis.

---

## What This Means for Each Domain

### Cooking: The Full Stack

```
ingredients/ (75 notes, each with have/location/category properties)
recipes/ (current stacks converted to notes with ingredients list)
Command Center.md (pure Dataview — "what can I make", "need to restock")
shopping.md (Dataview — ingredients where have=false AND always_stock=true)
```

**Migration**: Convert current inventory.md → 75 ingredient notes (scripted). Convert stacks.md → 9 recipe notes. Rewrite Command Center with Dataview queries.

### Day Planning: The Full Stack

```
Daily/2026-02-11.md (energy, sleep properties + task log + meal log)
Dashboard/Tasks.md (Dataview — energy-matched pending tasks)
Meta/Templates/(TEMPLATE) Daily.md (minimal template with Dataview task view)
```

**Migration**: Update daily template. Add energy/sleep properties. Add Dataview task matching.

### Research: The Full Stack

```
experiments/ (one note per experiment with target/method/status/results)
Command Center.md (Dataview — experiments by target, sorted by performance)
AAA_detection_personal/ (Plotivy folder structure for code/data)
```

**Migration**: Create experiments/ folder. Convert session logs to experiment notes. Apply Plotivy structure to code repo.

### Brain Repo: The Full Stack

```
tasks/ (already structured — add energy_needed, priority properties)
context/State.md (single source of truth — current focus + blockers)
docs/ (plans, solutions, brainstorms — already working)
```

**Migration**: Add properties to task files. Consolidate context/ files. Clean dead files.

---

## Implementation Strategy

**Phase 0: Prove the pattern** — ✅ COMPLETE (2026-02-11)
- [x] 82 ingredient notes created (77 from inventory + 5 always-stock items marked `have: false`)
- [x] 9 recipe notes created with ingredient links and component tables
- [x] Command Center rewritten with pure Dataview queries
- [x] Shopping.md updated with auto-computed restock list
- [x] Templates updated: Ingredient, Recipe/Stack, Daily (with energy), Grocery Trip (new)
- [x] Migration script: `tools/scripts/migrate-cooking.py`

**Phase 1: Cooking fixes** — ✅ COMPLETE (2026-02-11)
- [x] Fixed data model: unified ingredients + needs_restock into single list
- [x] Created 25 missing ingredient notes (all referenced by recipes, have: false)
- [x] Switched "What Can I Make" to DataviewJS (DQL can't dereference links)
- [x] Added "What's Missing per Recipe" view (1-3 ingredients away)
- [x] Total: 107 ingredient notes, 9 recipes, all properly linked
- [x] Fix script: `tools/scripts/fix-recipes.py`

**Phase 2: Daily planning** — ✅ COMPLETE (2026-02-11)
- [x] Daily template updated with `energy` and `sleep` properties
- [x] Energy-matched task Dataview query added to daily template
- [ ] 1-week trial (user needs to use it)

**Phase 3: Research** — ✅ COMPLETE (2026-02-11)
- [x] Experiment Log template updated for ML research (target, method, r2, mae, rmse)
- [x] experiments/ folder created under arterial analysis
- [x] 3 seed experiment notes from known results (cSBP, cPP, cfPWV baselines)
- [x] Command Center updated with Dataview experiment tracking queries
- [ ] Plotivy folder structure for code repo (separate task — requires work in AAA repo)

**Phase 4: Interaction automation** — ✅ COMPLETE (2026-02-11)
- [x] QuickAdd macros configured: New Ingredient, New Recipe, Grocery Trip, New Experiment, Log Meal
- [x] Bases views created: `Ingredient Manager.base` (4 views: All, Restock, In Stock, By Location)
- [x] Bases views created: `Experiment Tracker.base` (3 views: All, Best Results, By Status)
- [x] Templater folder templates: ingredients/ → Ingredient template, recipes/ → Stack template, experiments/ → Experiment Log
- [x] Cooking Stack template fixed: removed stale `needs_restock` field
- [x] CodeGraphContext MCP server installed (`uv tool install`) and configured (`.mcp.json`)

**Phase 5: Brain repo** — PENDING (lower priority, system works without this)

**Phase 6: Cross-cutting** — PENDING (slash commands, "without agent" docs)

---

## Full-Stack Reference (What's Built)

### Cooking Domain — Complete Stack

| Layer | Component | Human Access | Agent Access |
|-------|-----------|-------------|-------------|
| **Registry** | 107 ingredient notes in `Projects/cooking/ingredients/` | Properties panel (toggle `have`) | Obsidian MCP `obsidian_read_note`, filesystem |
| **Registry** | 9 recipe notes in `Projects/cooking/recipes/` | Open note, read component table | Obsidian MCP, filesystem read |
| **Rules** | Recipe `ingredients` list → links to ingredient notes | Automatic via Dataview | Parse frontmatter YAML |
| **Views** | Command Center (`Projects/cooking/Command Center.md`) | Open note → see computed views | Read note via MCP |
| **Views** | `Ingredient Manager.base` — spreadsheet with 4 views | Open .base file in Obsidian | Read .base YAML |
| **Capture** | QuickAdd: "New Ingredient" → creates note in ingredients/ | `Ctrl+P` → QuickAdd → New Ingredient | Obsidian MCP `obsidian_update_note` |
| **Capture** | QuickAdd: "Grocery Trip" → pre-filled restock checklist | `Ctrl+P` → QuickAdd → Grocery Trip | Create note via MCP with template |
| **Capture** | QuickAdd: "Log Meal" → appends to daily note ## Meals | `Ctrl+P` → QuickAdd → Log Meal | Append to daily note via MCP |
| **Capture** | Templater folder template: ingredients/ auto-applies | Create any note in ingredients/ | Write file to ingredients/ path |
| **Feedback** | Toggle `have` property after cooking/shopping | Properties panel checkbox | `obsidian_manage_frontmatter` |

### Research Domain — Complete Stack

| Layer | Component | Human Access | Agent Access |
|-------|-----------|-------------|-------------|
| **Registry** | Experiment notes in `Projects/arterial analysis/experiments/` | Properties panel | Obsidian MCP, filesystem |
| **Rules** | Frontmatter: target, method, status, r2, mae, rmse | Visible in Properties | Parse YAML |
| **Views** | Command Center with Dataview queries by target | Open Command Center | Read via MCP |
| **Views** | `Experiment Tracker.base` — 3 views (All, Best, By Status) | Open .base file | Read .base YAML |
| **Capture** | QuickAdd: "New Experiment" → creates in experiments/ | `Ctrl+P` → QuickAdd | Create note via MCP |
| **Capture** | Templater folder template: experiments/ auto-applies | Create any note in experiments/ | Write to experiments/ path |
| **Feedback** | Update status/r2/rmse after running experiment | Edit properties | `obsidian_manage_frontmatter` |

### Day Planning Domain — Partial Stack

| Layer | Component | Human Access | Agent Access |
|-------|-----------|-------------|-------------|
| **Registry** | Daily notes in `Daily/YYYY-MM-DD.md` | Daily note plugin | Obsidian MCP |
| **Rules** | `energy` property → filters tasks by energy_needed | Set energy, tasks auto-filter | Read/write frontmatter |
| **Views** | Dataview query in daily template | Embedded in daily note | Read daily note |
| **Capture** | Daily note template with energy/sleep fields | Core daily note plugin | Create note via MCP |
| **Feedback** | Log energy, meals, completions in daily note | Edit note | Append via MCP |

### Installed Tools & Plugins

| Tool | Location | Purpose |
|------|----------|---------|
| QuickAdd 2.11.0 | OneVault plugin | 5 macros: New Ingredient, New Recipe, Grocery Trip, New Experiment, Log Meal |
| Templater 2.18.1 | OneVault plugin | Folder templates: ingredients/, recipes/, experiments/ |
| Dataview | OneVault plugin | Query engine for all computed views |
| Bases (core) | Obsidian core | Spreadsheet views: Ingredient Manager, Experiment Tracker |
| CodeGraphContext | `~/.local/bin/cgc` | MCP server for code graph analysis (`.mcp.json`) |

### Key File Paths (OneVault)

```
Projects/cooking/
├── Command Center.md          ← DataviewJS: "What Can I Make", restock, fridge/freezer/pantry
├── shopping.md                ← Dataview: auto-computed restock list
├── Ingredient Manager.base    ← Bases: spreadsheet view for bulk editing
├── ingredients/               ← 107 notes (one per ingredient)
│   ├── zhoug-sauce.md
│   ├── black-beans-canned.md
│   └── ...
└── recipes/                   ← 9 notes (one per recipe/stack)
    ├── desi-mex-black-bean-tacos.md
    └── ...

Projects/arterial analysis/
├── Command Center.md          ← Dataview: experiments by target, best results
├── Experiment Tracker.base    ← Bases: spreadsheet + kanban by status
└── experiments/               ← 3 seed notes
    ├── csbp-stepwise-ols-baseline.md
    ├── cpp-stepwise-ols-baseline.md
    └── cfpwv-stepwise-ols-baseline.md

Meta/Templates/
├── (TEMPLATE) Cooking Ingredient.md
├── (TEMPLATE) Cooking Stack.md
├── (TEMPLATE) Grocery Trip.md
├── (TEMPLATE) Daily.md
└── Experiment Log.md
```

---

## Anti-Patterns to Avoid

1. **Don't build what you won't maintain** — If 75 ingredient files feels like too much, start with 20 (the ones you actually use) and add as needed
2. **Don't over-query** — Dataview is powerful but slow queries make Obsidian laggy. Keep queries scoped to specific folders.
3. **Don't automate capture you can do in 2 taps** — Toggling `have: false` in Properties panel IS the automation. You don't need a script for that.
4. **Don't fight Obsidian** — If it requires a plugin that breaks every update, it's not lean. Stick to core Obsidian + Dataview + Templater.
5. **Don't optimize for agents** — The system should work for YOU first. Agent-queryable is a bonus, not the goal.

---

## Open Design Questions

1. **Ingredient granularity**: Is "Zhoug Sauce" one note, or is "Trader Joe's Zhoug 8oz" the note? (Recommendation: brand-agnostic names, brand in a property)
2. **Recipe vs meal**: A "recipe" is reusable. A "meal" is an instance. Do meals get their own notes or just daily log entries? (Recommendation: just daily log entries with recipe links)
3. **Dataview performance**: 75 ingredient notes + 9 recipe notes with cross-queries — test if this is fast enough on the user's machine
4. **Mobile workflow**: Does the user capture groceries on mobile? If so, Properties panel must work well on phone.
5. **Stale data**: What happens when inventory gets out of date? (Recommendation: weekly "inventory check" template — open, scan, toggle anything that changed)

---

## Success Criteria

- [ ] "What can I cook?" answered in <10 seconds by opening one note (no agent)
- [ ] "What should I do today?" answered by setting energy level in daily note (no agent)
- [ ] "What experiments have I run on cSBP?" answered by one Dataview query (no agent)
- [ ] Grocery trip captured in <2 minutes with a template
- [ ] Daily note filled in <2 minutes
- [ ] Experiment logged in <1 minute (template pre-fills metadata)
- [ ] Agent slash commands (`/cook`, `/day`, `/research-status`) exist for ENHANCED mode
- [ ] Each domain's Command Center has zero hand-curated lists — all computed

## References

- [Plotivy Research Data Organization](https://plotivy.app/blog/research-data-organization-guide)
- [Compound Engineering](https://every.to/guides/compound-engineering)
- Obsidian Dataview docs: field types, FROM/WHERE/SORT, inline fields
- Obsidian Templater docs: tp.date, tp.file, dynamic templates
- Obsidian Properties: typed frontmatter, checkbox/date/number types
