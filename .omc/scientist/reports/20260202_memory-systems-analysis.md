# Memory/Context Systems Analysis for Claude/LLMs
Generated: 2026-02-02 20:15:30

## Executive Summary

Analysis of 15+ memory/context systems for Claude reveals a clear pattern: **complexity kills adoption, simplicity wins in production**. The most successful approaches leverage existing infrastructure (CLAUDE.md files, git, simple JSON/markdown) rather than requiring new databases or maintenance. Anthropic's official knowledge graph MCP is stable but criticized for memory separation issues. Third-party solutions show high innovation but variable maintenance commitment. Key finding: file-based append-only approaches aligned with existing workflows show highest real-world usage despite fewer GitHub stars.

---

## Tier 1: RECOMMENDED (Minimal, Low Friction, Stable)

| System | Approach | Fits Principles? | Stability | Verdict |
|--------|----------|------------------|-----------|---------|
| **CLAUDE.md files** | Project-scoped markdown configuration | ✅ Minimal, zero new habits, append-friendly, built into Claude Code | ✅ Official Anthropic feature, stable | **BEST for project context** - Read automatically every session, no setup beyond creating file |
| **Anthropic Memory MCP** | Local knowledge graph (memory.json) | ✅ Official, local storage, MIT license | ✅ Reference implementation, actively maintained | **BEST for official support** - Works across Claude Desktop/Code, but needs better project separation |
| **mcp-memory-service** | Auto-consolidation with quality scoring | ⚠️ More complex (HTTP server, multiple components) | ✅ Production-ready, frequent updates (v8.45.0 Jan 2026) | **BEST for enterprise** - Handles 13+ AI tools, 88% token reduction, but requires more infrastructure |
| **Context7 MCP** | Up-to-date documentation fetching | ✅ Ultra-minimal, zero storage, query-on-demand | ✅ Maintained by Upstash team, stable | **BEST for documentation** - Prevents outdated API hallucinations, no memory storage needed |

---

## Tier 2: CONSIDER (Tradeoffs Exist)

| System | Approach | Issues | Stability | Verdict |
|--------|----------|--------|-----------|---------|
| **claude-mem** | Hook-based auto-capture with SQLite+Chroma | ⚠️ Requires Bun runtime, port 37777 service, Node.js 18+ | ⚠️ Frequent updates but introduces bugs (Jan 2026 instability) | High token efficiency (10x savings) but **beta quality** - Windows issues persist, users requesting stable/nightly channels |
| **claude-memory-mcp (WhenMoon)** | Lightweight SQLite FTS5 | ✅ Only 2 dependencies, no embeddings | ⚠️ "Breaking changes between minor versions" | Simple architecture but **unstable API** - Good for experimentation, risky for production |
| **SimpleMem** | 3-view indexing (semantic/lexical/symbolic) | ⚠️ Requires OpenAI API, LanceDB vector store | ⚠️ Research-grade (arXiv Jan 2026) | Impressive benchmarks (43% F1, 12.5x faster) but **not minimal** - Adds vector DB complexity |
| **Khoj AI** | Self-hosted second brain | ⚠️ Full application stack, not just memory | ✅ Active development, cloud + self-host options | Feature-rich but **over-engineered** for pure memory needs - Better as full AI assistant replacement |

---

## Tier 3: AVOID (Anti-Patterns)

| System | Why Avoid |
|--------|-----------|
| **GraphRAG for generic memory** | Schema design becomes unmaintainable for messy, evolving human knowledge. Entity resolution and disambiguation overwhelm the approach. Works for domain-specific tasks only. |
| **Fine-tuning for memory** | Catastrophic forgetting remains unsolved. Each update overwrites prior knowledge. Not viable for continuous learning. |
| **Agentic RAG loops** | Inherits RAG's fragmentation problems while adding latency, token waste, and risk of infinite loops. Computational cost outweighs benefits. |
| **Vector-only search** | Fragments context, misses multi-hop reasoning, poor for "what contradictions exist?" queries. Good for retrieval, fails for reasoning over time. |
| **Custom research implementations** | Research benchmarks (isolated prompt pairs) don't transfer to real dialogue. MemoryLLM promising in theory but unproven in production. |

---

## Best Practices Observed

### From CLAUDE.md Implementations
- **Keep it lean**: 150-200 instructions max (context window cost every session)
- **Be specific**: "Use 2-space indentation" > "Format code properly"
- **Structure with headers**: Group related memories under markdown headings
- **Don't replace linters**: Never send LLM to do linter's job (expensive, slow)
- **Use file references**: Link to task-specific docs, let Claude decide relevance
- **Iterate over time**: Generated CLAUDE.md is starting point, refine based on actual usage
- **Organize large projects**: Use `.claude/rules/` directory for focused rule files

### From MCP Memory Systems
- **2-tier storage pattern**: Active context (CLAUDE.md ~150 lines) + searchable archive (state.json via MCP)
- **Progressive disclosure**: 3-layer retrieval (index → timeline → full details) saves 10x tokens
- **Confidence decay**: Keep low-confidence memories searchable but out of active briefings
- **Budget allocation**: Per-category line limits with intelligent reallocation (25 architecture, 30 progress)
- **Write-time deduplication**: Jaccard similarity 60%+ threshold prevents duplicates from accumulating
- **LLM consolidation**: Every 10 extractions or 80+ memories, trigger merge/drop/resolve via Haiku ($0.001/extraction)
- **Hybrid search**: Combine FTS5 keyword + semantic when pure vector search fails

### From Production Usage
- **Local-first wins**: Full control, privacy, no mandatory cloud infrastructure
- **Automatic > manual**: Systems requiring user curation fail in practice
- **Tag generously**: Better searchability across sessions (memory_related: retrieve by tag)
- **Fresh verification**: 5-minute staleness detection prevents outdated context
- **Graceful degradation**: Handle missing dependencies, provide fallbacks

### From Failure Modes
- **Context rot is real**: Even million-token windows struggle with signal/noise at scale
- **RAG works for retrieval, fails for reasoning**: "Pull documentation" ✓, "reason over disagreements" ✗
- **False memory marketing**: Most systems are retrieval tools, not genuine learning
- **Research ≠ production**: Clean benchmarks don't transfer to messy real data
- **Single-user designs fail**: Multi-agent systems need shared memory architecture

---

## Implementation Patterns Worth Stealing

### Pattern 1: Tiered Memory Hierarchy (claude-mem)
**How it works**:
- Tier 1 (CLAUDE.md): ~150 lines, read every session, automatic injection
- Tier 2 (.memory/state.json): Full store with every fact, accessible via MCP tools (search, timeline, get)
- Tier 3 (Archive): Confidence <0.3 memories remain searchable but excluded from active briefings

**Why it's good**:
- Prevents context window bloat while maintaining complete knowledge
- Progressive disclosure saves tokens (10x reduction)
- Balances immediacy (Tier 1) with completeness (Tier 2) and history (Tier 3)

### Pattern 2: Automated Consolidation (mcp-memory-service)
**How it works**:
- Every 10 extractions or 80+ active memories, trigger consolidation
- Haiku model ($0.001 cost) groups memories by type, identifies:
  - Overlapping entries → merge
  - Outdated entries → drop
  - Contradictions → resolve
- Result: 88% token reduction, fully automated "garbage collection for knowledge"

**Why it's good**:
- Zero manual maintenance burden
- Prevents exponential memory growth
- Uses cheap model for maintenance, reserves expensive models for generation
- Decay scoring + association discovery + compression + archival in one pass

### Pattern 3: Hook-Based Capture (claude-mem)
**How it works**:
5 lifecycle hooks inject memory operations automatically:
1. `SessionStart` - Load active memories into CLAUDE.md
2. `UserPromptSubmit` - Capture user intent/context
3. `PostToolUse` - Extract observations from tool outputs
4. `Summary` - Consolidate session learnings
5. `SessionEnd` - Archive and cleanup

**Why it's good**:
- Zero user action required (true zero-friction)
- Captures complete session context automatically
- Works with existing Claude Code workflow
- Provides clear extension points for customization

### Pattern 4: File-Based Blackboard (Our "Brain" Repo)
**How it works**:
- Git repository as coordination layer
- Directory structure encodes state (`tasks/pending/` → `tasks/active/` → `tasks/completed/`)
- Agents check state files (`context/active-agents.md`), claim tasks, commit work
- File-based messaging (`messages/outbox/MSG-<timestamp>-<from>-<to>.md`)

**Why it's good**:
- Leverages existing infrastructure (git, filesystem)
- Append-only friendly (git log = full history)
- Multi-agent coordination without custom protocols
- Debuggable (can inspect any file at any time)
- Works across different Claude interfaces (Desktop, Code, API)

### Pattern 5: Documentation-on-Demand (Context7)
**How it works**:
- No persistent storage at all
- Two tools: `resolve-library-id` (library name → Context7 ID) + `query-docs` (fetch current docs)
- Pulls version-specific documentation at query time
- Feeds LLM latest docs instead of relying on stale training data

**Why it's good**:
- Ultimate minimalism (zero storage, zero maintenance)
- Always up-to-date (no sync lag)
- No consolidation needed (stateless)
- Works across any MCP-compatible client
- Prevents hallucinated APIs that don't exist

### Pattern 6: Quality-Driven Retention (mcp-memory-service)
**How it works**:
- Multi-tier fallback: ONNX local SLM → cloud if needed
- Each memory gets quality score (freshness, relevance, usage frequency)
- Retention decisions based on quality + access patterns
- `access_count` and `last_accessed_at` tracking
- Low-quality memories archived, not deleted (searchable if explicitly queried)

**Why it's good**:
- Prevents accumulation of noise
- Rewards frequently-used knowledge (positive feedback loop)
- Balances recency bias with historical value
- Observable metrics (quality analytics dashboard)

### Pattern 7: Hybrid Search Strategy (claude-mem, claude-memory-mcp)
**How it works**:
- SQLite FTS5 for keyword/exact matching (fast, deterministic)
- Chroma/embeddings for semantic similarity (handles paraphrasing)
- Symbolic metadata (timestamps, entities, tags) for structured queries
- Query router decides which index(es) to use based on query type

**Why it's good**:
- FTS5 catches exact matches vectors miss
- Vectors catch semantic similarity keywords miss
- Metadata enables temporal/entity-based filtering
- Each index compensates for others' weaknesses
- Degrades gracefully if embedding service unavailable

### Pattern 8: Markdown + LLM Self-Management (Minimal POC)
**How it works**:
- Store memories in single markdown file
- LLM decides storage structure through tool use
- Autonomous behaviors emerge: decides when to check memories, finds relevant info naturally, recovers from errors
- ~150 lines Python, no database, no vector store

**Why it's good**:
- Simplest possible implementation
- Git-committable, scp-portable, human-readable
- LLM handles complexity, infrastructure stays simple
- Architectural flexibility (swap backend without changing interface)
- Perfect for prototyping and learning

---

## Architectural Tradeoffs

### Knowledge Graph vs Vector Store

| Dimension | Knowledge Graph | Vector Store |
|-----------|----------------|--------------|
| **Best for** | Complex relationships, reasoning chains | Semantic search, summarization |
| **Retrieval** | Logical connections, multi-hop traversal | Similarity-based, single-step |
| **Speed** | Slower for large graphs | Fast (milliseconds) |
| **Maintenance** | High (schema design, entity resolution) | Low (append embeddings) |
| **Context linking** | Excellent (explicit edges) | Poor (chunks isolated) |
| **Claude official choice** | ✓ (knowledge graph MCP) | Used in third-party tools |

**Recommendation**: Knowledge graphs for persistent memory with relationships (Anthropic's choice); vector stores for ephemeral semantic search. Hybrid approaches (both) show best results in practice.

### Local vs Cloud Storage

| Dimension | Local (file-based) | Cloud (managed service) |
|-----------|-------------------|------------------------|
| **Privacy** | Complete control | Trust provider |
| **Offline** | Works offline | Requires connectivity |
| **Scalability** | Manual (file size limits) | Automatic |
| **Maintenance** | User responsibility | Provider handles |
| **Cost** | Free (disk space) | Subscription fees |
| **Multi-device** | Sync via git/Dropbox | Native sync |

**Recommendation**: Local for "Brain" use case (privacy, git integration, multi-agent coordination). Cloud for enterprise teams needing centralized knowledge.

### Automatic vs Manual Memory

| Dimension | Automatic Capture | Manual Curation |
|-----------|------------------|----------------|
| **User burden** | Zero | High (compliance fatigue) |
| **Signal/noise** | Moderate (captures everything) | High (user filters) |
| **Adoption** | High (works immediately) | Low (requires discipline) |
| **Privacy control** | Requires opt-out tags (`<private>`) | Opt-in (explicit saves) |
| **Completeness** | High (nothing missed) | Low (users forget) |

**Recommendation**: Automatic with privacy tags (claude-mem pattern) wins in practice. Manual curation fails due to compliance fatigue.

---

## Evaluation Against "Brain" Principles

### Principle 1: Minimal (Not Over-Engineered)

**✅ PASS**:
- CLAUDE.md files (built-in, zero infrastructure)
- Context7 (stateless, query-on-demand)
- claude-memory-mcp (2 dependencies only)
- File-based blackboard (git + filesystem)

**❌ FAIL**:
- Khoj AI (full application stack)
- SimpleMem (requires LanceDB + OpenAI API)
- GraphRAG (schema design complexity)

### Principle 2: Low Friction (Zero New Habits)

**✅ PASS**:
- claude-mem (hooks capture automatically, zero user action)
- mcp-memory-service (auto-consolidation, no manual maintenance)
- CLAUDE.md (read automatically every session)
- Context7 (invoked by Claude when needed)

**❌ FAIL**:
- Manual memory curation systems (require user discipline)
- Systems requiring explicit save/load commands
- Complex query syntax requirements

### Principle 3: Append-Only Friendly

**✅ PASS**:
- File-based approaches (markdown, JSON - perfect for git)
- SQLite with append-only writes
- Knowledge graphs (add entities/relations, soft-delete for updates)
- Git-based blackboard pattern

**⚠️ MIXED**:
- Vector stores (embeddings append-only, but metadata updates)
- Consolidation systems (merge/drop operations not pure append)

**❌ FAIL**:
- Systems requiring in-place updates or schema migrations
- Binary database formats without export

### Principle 4: Actively Maintained

**✅ PASS (Jan 2026 activity)**:
- mcp-memory-service (v8.45.0, v8.43.0, v8.42.0 recent releases)
- Anthropic Memory MCP (official, reference implementation)
- Context7 (Upstash team, stable updates)
- claude-mem (frequent updates, though introducing bugs)

**⚠️ CAUTION**:
- claude-memory-mcp (active but "breaking changes between minor versions")
- SimpleMem (research-grade, arXiv Jan 2026, unclear production support)

**❌ CONCERN**:
- Projects with last update >6 months ago
- Research implementations without production roadmap

### Principle 5: Actually Used (Not Just Stars)

**✅ HIGH USAGE INDICATORS**:
- CLAUDE.md (official feature, documented best practices proliferation)
- mcp-memory-service (13+ AI tools integration, enterprise testimonials)
- Anthropic Memory MCP (official, cross-client compatibility)
- Context7 (Upstash-backed, Docker Hub presence)

**⚠️ MODERATE USAGE**:
- claude-mem (16k stars, active issues, community tooling like memory-visualizer)
- claude-memory-mcp (community plugins, marketplace presence)

**❓ UNCLEAR USAGE**:
- SimpleMem (research release, no production case studies yet)
- Newer projects (<3 months old)

---

## Red Flags & Warning Signs

### From claude-mem (Jan 2026)
- **Instability**: "Frequent updates introducing new bugs"
- **Platform issues**: "Persistent Windows issues" despite multiple fix attempts
- **User requests**: Beta/stable channel split requested (quality concerns)
- **Complexity creep**: Multiple runtimes (Bun, Node.js 18+), port management, auto-installers

### From General Claude Usage (Early 2026)
- **Token limits**: Even paid users hitting limits in 10-15 minutes
- **Memory failures**: "Loses the plot" in long conversations, forgets instructions
- **No support**: "No customer service even for paid subscriptions"
- **Billing issues**: Unauthorized charges, verification bugs

### From Memory System Research
- **False marketing**: "Most call retrieval 'memory' without genuine learning"
- **Research/production gap**: "Clean benchmarks don't transfer to messy real data"
- **Unmaintainable schemas**: "Generic human memory schema design nearly impossible"
- **Catastrophic forgetting**: "Fine-tuning overwrites prior knowledge, remains unsolved"

### From MCP Ecosystem
- **Breaking changes**: Minor version updates changing APIs
- **Project separation**: "Memory overlap for similar projects" (Anthropic MCP issue)
- **Dependency sprawl**: Some systems require 5+ external services
- **Configuration complexity**: Multi-file JSON configs across different OS paths

---

## Recommendations for "Brain" System

### Tier 1: Immediate Implementation (High Value, Low Risk)

1. **CLAUDE.md files**: Already using `.claude/` - extend with project-scoped memory
   - Store: Architecture decisions, agent coordination protocols, common patterns
   - Format: Structured markdown with headers (150-line budget)
   - Update: Via git commits (append-only friendly)

2. **Context7 MCP**: Zero infrastructure, immediate value for documentation queries
   - Prevents outdated API hallucinations
   - No storage/maintenance burden
   - Works across Desktop + Code

3. **File-based state tracking**: Already doing this well
   - Keep: `context/session-state.md`, `context/active-agents.md`
   - Enhance: Add `context/learnings.md` for discovered patterns
   - Pattern: Directory structure encodes state (pending/active/completed)

### Tier 2: Strategic Enhancement (High Value, Moderate Effort)

4. **Anthropic Memory MCP**: Official support, stable, but wait for project separation fix
   - Monitor: GitHub issues for "memory overlap for similar projects"
   - Timing: Implement when separation issue resolved
   - Benefit: Cross-client memory (Desktop ↔ Code ↔ API)

5. **Selective hook-based capture**: Steal claude-mem's pattern without full complexity
   - Implement: Lightweight SessionEnd hook that appends learnings to `context/learnings.md`
   - Avoid: Complex worker service, multiple databases, auto-installers
   - Keep: Simple filesystem operations

### Tier 3: Future Exploration (If Specific Need Emerges)

6. **mcp-memory-service**: Only if need multi-tool coordination beyond Claude
   - Trigger: If integrating Cursor/VS Code/Windsurf alongside Claude
   - Caution: Adds infrastructure complexity (HTTP server, consolidation scheduler)
   - Benefit: 88% token reduction through auto-consolidation

7. **Hybrid search**: Only if git grep / file search proves insufficient
   - Start: SQLite FTS5 for keyword search (no vectors yet)
   - Add vectors: Only when semantic search becomes critical need
   - Avoid: Jumping straight to vector store without proven need

### Tier 4: Avoid (Anti-Patterns for "Brain")

- ❌ GraphRAG: Schema maintenance nightmare for evolving knowledge
- ❌ claude-mem full install: Unstable, over-engineered for our needs
- ❌ Cloud-dependent systems: Violates local-first principle
- ❌ Manual curation: Compliance fatigue guarantees failure
- ❌ Research implementations: Production-readiness unproven

---

## Specific "Brain" Implementation Sketch

### Proposed Enhancement: Memory Layer

```
/home/div/brain/
├── context/
│   ├── session-state.md          # (existing) Recovery state
│   ├── active-agents.md          # (existing) Who's working on what
│   ├── learnings.md              # (NEW) Discovered patterns, solutions
│   ├── decisions.md              # (NEW) Why we chose X over Y
│   └── predictions.md            # (existing) Anticipatory assistance
├── .claude/
│   ├── CLAUDE.md                 # (NEW) Project-scoped memory (150-line budget)
│   └── rules/                    # (NEW) Focused rule files for large contexts
│       ├── coordination.md       # Multi-agent protocols
│       ├── architecture.md       # System design principles
│       └── workflows.md          # Common patterns
└── tools/
    └── mcps/
        └── context7-config.json  # (NEW) Documentation fetching
```

### Memory Capture Workflow

**Automatic (Zero Friction)**:
- Git commits already capture all state changes (append-only ✓)
- Agents already update `context/active-agents.md` when claiming tasks
- Session state already tracked in `context/session-state.md`

**Enhanced (Minimal New Habits)**:
- When completing task: Append to `context/learnings.md` if discovered reusable pattern
- When making architectural choice: Append to `context/decisions.md` with rationale
- CLAUDE.md auto-read every session (zero action required)

**Query-Time (On-Demand)**:
- Context7 MCP: Automatically fetches docs when Claude encounters library usage
- Git log/grep: Existing for finding past decisions/patterns
- File search: Existing for locating relevant context

### Token Budget Allocation

```markdown
# CLAUDE.md (150-line budget)

## Architecture Principles (25 lines)
- Multi-interface coordination: Desktop, Code, Overnight
- File-based blackboard pattern for state
- Append-only git workflow for all changes

## Agent Coordination Protocols (30 lines)
- Check context/active-agents before starting
- Move tasks: pending → active → completed
- Commit frequently for coordination
- See @.claude/rules/coordination.md for full protocols

## Common Patterns (30 lines)
- Task claiming workflow
- Handoff procedure
- Question generation → prompts/pending/
- See context/learnings.md for discovered solutions

## Critical Constraints (15 lines)
- Check context/off-limits before modifications
- Never modify active agent's workspace
- Log all operations to logs/

## Quick Reference (20 lines)
- context/ - Shared state
- tasks/ - Work queue
- knowledge/ - Research findings
- prompts/ - User Q&A
```

### Consolidation Strategy (Borrowed from mcp-memory-service)

**Trigger**: When `context/learnings.md` exceeds 100 entries
**Action**: Spawn Haiku agent to consolidate
**Process**:
1. Group learnings by topic
2. Merge duplicates/overlaps
3. Identify outdated patterns (replaced by better solutions)
4. Update CLAUDE.md with top 10 most-used patterns
5. Archive full history in `knowledge/patterns-archive.md`

**Cost**: ~$0.01 per consolidation
**Frequency**: ~1x per week at current activity level

---

## Metrics for Success

### Leading Indicators (What to Track)

| Metric | How to Measure | Target |
|--------|---------------|--------|
| **Context re-explanation frequency** | Count times agent asks for info in `context/` files | <1 per session |
| **CLAUDE.md reference rate** | Grep for "according to CLAUDE.md" in agent responses | >3 per session |
| **Learning capture rate** | New entries in `context/learnings.md` per week | 5-10 |
| **Decision documentation rate** | New entries in `context/decisions.md` per week | 2-5 |
| **Context7 query rate** | Check MCP logs for `query-docs` invocations | >0 when coding |
| **Token efficiency** | Avg tokens/session before vs after | -20% reduction |

### Lagging Indicators (Outcomes)

| Metric | How to Measure | Target |
|--------|---------------|--------|
| **Anticipatory accuracy** | Predictions in `context/predictions.md` that came true | >30% |
| **Agent coordination smoothness** | Handoff failures (check `context/handoff.md`) | <1 per week |
| **Knowledge reuse** | References to `context/learnings.md` solutions | >2 per week |
| **Onboarding speed** | New agent time-to-productivity (inferred from first commit) | <15 min |

### Anti-Metrics (Warning Signs)

| Metric | Threshold | Action |
|--------|-----------|--------|
| **CLAUDE.md bloat** | >200 lines | Trigger consolidation |
| **Learnings stagnation** | <2 new entries/week for 3 weeks | Review capture process |
| **Context staleness** | File unchanged >2 weeks | Archive or delete |
| **Coordination collisions** | >2 agents editing same file | Improve claiming protocol |

---

## Migration Path (Minimal Disruption)

### Phase 1: Foundation (Week 1)
- [ ] Create `.claude/CLAUDE.md` with current architecture + protocols
- [ ] Add `context/learnings.md` and `context/decisions.md`
- [ ] Install Context7 MCP (no code changes, just config)
- [ ] Document current patterns in learnings.md (bootstrap)

### Phase 2: Habit Formation (Weeks 2-4)
- [ ] Agents append to learnings.md when solving novel problems
- [ ] Agents append to decisions.md when making tradeoff choices
- [ ] Monitor CLAUDE.md reference rate (success metric)
- [ ] Refine CLAUDE.md based on actual usage

### Phase 3: Optimization (Month 2)
- [ ] First consolidation when learnings.md hits 100 entries
- [ ] Evaluate Context7 query logs (is it helping?)
- [ ] Consider `.claude/rules/` split if CLAUDE.md exceeds 150 lines
- [ ] Measure token efficiency improvement

### Phase 4: Evaluation (Month 3)
- [ ] Review all metrics (leading + lagging indicators)
- [ ] Decide: Keep as-is / Enhance with Anthropic MCP / Scale back
- [ ] Document lessons in `knowledge/memory-system-retrospective.md`

---

## Conclusion

**Winning Strategy**: Combine CLAUDE.md (built-in, zero friction) + file-based state tracking (already doing well) + Context7 MCP (documentation on-demand) + lightweight learnings capture (append-only to markdown).

**Why This Wins**:
- ✅ Minimal: Leverages existing infrastructure (git, filesystem, Claude Code)
- ✅ Low friction: Automatic reading (CLAUDE.md), append-only writes (learnings.md)
- ✅ Append-friendly: Everything is markdown/JSON in git
- ✅ Stable: CLAUDE.md official, Context7 backed by Upstash, file operations bulletproof
- ✅ Actually used: Patterns proven across documentation sources

**Avoid**: Over-engineering with databases, vector stores, or research implementations before proven need. Start simple, enhance based on measured constraints.

**Next Action**: Create CLAUDE.md and bootstrap learnings.md with existing tribal knowledge from current `context/` files.

---

## Sources

### Memory Systems & Documentation
- [MCP Memory Service](https://github.com/doobidoo/mcp-memory-service)
- [Claude Memory MCP by WhenMoon](https://github.com/WhenMoon-afk/claude-memory-mcp)
- [claude-mem Repository](https://github.com/thedotmack/claude-mem)
- [SimpleMem: Efficient Memory for LLM Agents](https://github.com/aiming-lab/SimpleMem)
- [Khoj AI - Self-hosted Second Brain](https://github.com/khoj-ai/khoj)
- [Anthropic Knowledge Graph Memory Server](https://www.pulsemcp.com/servers/modelcontextprotocol-knowledge-graph-memory)
- [Context7 MCP - Up-to-date Documentation](https://github.com/upstash/context7)

### Best Practices & Architecture
- [Using CLAUDE.md Files](https://claude.com/blog/using-claude-md-files)
- [The Architecture of Persistent Memory for Claude Code](https://dev.to/suede/the-architecture-of-persistent-memory-for-claude-code-17d)
- [Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [Why LLM Memory Still Fails - A Field Guide](https://dev.to/isaachagoel/why-llm-memory-still-fails-a-field-guide-for-builders-3d78)
- [Claude Code Best Practices: Memory Management](https://cuong.io/blog/2025/06/15-claude-code-best-practices-memory-management)

### Technical Deep Dives
- [MCP Memory Service: An AI Engineer's Deep Dive](https://skywork.ai/skypage/en/MCP-Memory-Service:%20An%20AI%20Engineer's%20Deep%20Dive/1972459747590451200)
- [Knowledge Graph vs Vector Database for RAG](https://www.meilisearch.com/blog/knowledge-graph-vs-vector-database-for-rag)
- [How Claude's Memory and MCP Work](https://www.mintlify.com/blog/how-claudes-memory-and-mcp-work)
- [AI Apps with MCP Memory Benchmark & Tutorial in 2026](https://research.aimultiple.com/memory-mcp/)

### User Experience & Issues
- [claude-mem Beta Testing Strategy Proposal](https://github.com/thedotmack/claude-mem/issues/624)
- [Claude Code Review 2026](https://aitoolanalysis.com/claude-code/)
- [Claude Devs Complain About Usage Limits](https://www.theregister.com/2026/01/05/claude_devs_usage_limits/)
- [Feature Request: Persistent Memory Between Sessions](https://github.com/anthropics/claude-code/issues/14227)
