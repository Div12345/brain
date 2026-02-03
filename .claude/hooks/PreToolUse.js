/**
 * PreToolUse Hook - Automatic Context Injection
 *
 * Fires before EVERY tool call to inject session context automatically.
 * Solves the abandoned conversation problem by re-injecting context
 * before each tool execution, regardless of model attention.
 *
 * Location: .claude/hooks/PreToolUse.js
 * Reads: context/session-handoff.md
 * Injects: Brief summary (Current Focus + Recent Decisions)
 *
 * Implementation: 2026-02-03
 * Research: knowledge/research/automatic-context-injection-mechanisms.md
 */

export default async function PreToolUse(input) {
  const { tool } = input;

  // Only inject on tools that need context (not on every tool)
  // Read/Edit/Write: Need to know what we're working on
  // Bash: May need context for commands
  // Task: Delegating to agents needs context
  const contextTools = ['Read', 'Edit', 'Write', 'Bash', 'Task'];

  if (!contextTools.includes(tool)) {
    return {}; // No injection needed for other tools
  }

  // Dynamic import for Node.js modules
  const fs = await import('fs/promises');
  const path = await import('path');

  // Path to session handoff file
  const handoffPath = path.join(process.cwd(), 'context/session-handoff.md');

  let context = '';

  try {
    // Read the session handoff file
    context = await fs.readFile(handoffPath, 'utf-8');
  } catch (err) {
    // File doesn't exist or can't be read - no context to inject
    // This is fine - not all projects will have this file
    return {};
  }

  // Extract key sections to inject (token-efficient)
  // Only inject what's needed, not the full file
  const lines = context.split('\n');

  // Find Current Focus section
  const focusStartIdx = lines.findIndex(l => l.includes('## Current Focus'));
  const focusEndIdx = lines.findIndex((l, i) => i > focusStartIdx && l.startsWith('##'));
  const focusLines = focusStartIdx >= 0 && focusEndIdx >= 0
    ? lines.slice(focusStartIdx, focusEndIdx).join('\n')
    : '';

  // Find Recent Decisions section (last 10 lines to save tokens)
  const decisionsStartIdx = lines.findIndex(l => l.includes('## Recent Decisions'));
  const decisionsEndIdx = lines.findIndex((l, i) => i > decisionsStartIdx && l.startsWith('##'));
  const decisionsLines = decisionsStartIdx >= 0
    ? lines.slice(decisionsStartIdx, decisionsEndIdx >= 0 ? decisionsEndIdx : decisionsStartIdx + 15).join('\n')
    : '';

  // Build brief context summary
  const briefContext = `
## Session Context (auto-injected via PreToolUse hook)

${focusLines}

${decisionsLines}

**Note**: Full context available in context/session-handoff.md
**Hook**: This context is automatically injected before every Read/Edit/Write/Bash/Task to ensure continuity across abandoned sessions.
  `.trim();

  // Return context injection
  return {
    hookSpecificOutput: {
      additionalContext: briefContext
    }
  };
}
