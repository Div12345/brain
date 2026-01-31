# Tools Building Framework

> When the system identifies a gap, it builds tools to fill it.

## Philosophy

**"The best tool is one you don't have to think about."**

Build only when:
1. Gap is clearly identified and documented
2. No existing solution fits (checked GitHub, npm, PyPI)
3. Minimal implementation can solve the problem
4. It matches user's "low friction" principle

## Tool Types

| Type | Location | Purpose |
|------|----------|---------|
| **MCP Server** | `tools/mcps/` | New capabilities for Claude |
| **Plugin** | `tools/plugins/` | Claude Code extensions |
| **Hook** | `tools/hooks/` | Hookify rules for behavior modification |
| **Command** | `tools/commands/` | Custom slash commands |
| **Config** | `tools/configs/` | Configuration templates |
| **Script** | `tools/scripts/` | Automation scripts |

## MCP Server Template

```javascript
// tools/mcps/[name]/index.js
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({
  name: "[name]",
  version: "0.1.0",
}, {
  capabilities: {
    tools: {},
  },
});

// Define tools
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: "[tool_name]",
    description: "[what it does]",
    inputSchema: {
      type: "object",
      properties: {
        // params
      },
    },
  }],
}));

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  // implementation
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

## Plugin Template

```markdown
<!-- tools/plugins/[name]/commands/[command].md -->
---
name: [command-name]
description: [what it does]
---

# /[name]:[command]

[Instructions for Claude when this command is invoked]
```

## Hook Template

```markdown
<!-- tools/hooks/[name].local.md -->
---
name: [hook-name]
enabled: true
event: bash|file|stop|prompt
action: warn|block
pattern: [regex]
---

[Message to show when triggered]
```

## Tool Development Workflow

1. **Identify Gap**
   - Document in `inspirations/tools.md`
   - Link to experiment that revealed it

2. **Research Existing Solutions**
   - Search GitHub for similar tools
   - Check npm/PyPI registries
   - Review Reddit/HN discussions
   - Document findings in `inspirations/github-repos.md`

3. **Design Minimal Solution**
   - Create spec in `tools/[type]/[name]/SPEC.md`
   - Define success criteria
   - Plan rollback strategy

4. **Build**
   - Implement in appropriate location
   - Include tests where possible
   - Document usage in README.md

5. **Test in Isolation**
   - Run experiment (see `experiments/`)
   - Measure against success criteria
   - Don't integrate until validated

6. **Integrate**
   - Add to appropriate config
   - Update `context/ecosystem.md`
   - Document in `meta/structure.md`

7. **Monitor**
   - Track usage
   - Collect feedback
   - Iterate or deprecate

## Safety Rules

| Rule | Implementation |
|------|----------------|
| **Sandbox first** | Test in isolated environment |
| **Version everything** | Git commit each change |
| **Reversible** | Keep previous version accessible |
| **Minimal scope** | Don't over-engineer |
| **Document why** | Every tool has purpose documented |

## Tools Wishlist

(Agents add ideas here based on gaps discovered)

| Gap | Proposed Tool | Priority | Status |
|-----|---------------|----------|--------|
| - | - | - | - |

---

*Tools are experiments. Build, measure, learn, iterate.*
