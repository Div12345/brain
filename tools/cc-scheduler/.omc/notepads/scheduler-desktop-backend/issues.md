# Issues and Blockers

## Gemini API Capacity Exhaustion (2026-02-05)

### Problem
Attempted to execute task 064 (review-desktop-pipeline) through the desktop backend but hit repeated 429 errors:
- Error: "No capacity available for model gemini-3-pro-preview on the server"
- Status: RESOURCE_EXHAUSTED
- Reason: MODEL_CAPACITY_EXHAUSTED

### Impact
- Cannot test Gemini→Desktop pipeline with real tasks
- Desktop backend is blocked on Gemini API availability
- Retries (attempt 1, 2, 3+) all failed with same capacity error

### Timeline
- 10:07:52 - Started gemini process
- 10:10:39 - Attempt 1 failed (429)
- 10:11:20 - Attempt 1 retry failed (429)
- 10:11:27 - Attempt 2 failed (429)
- 10:11:52 - Attempt 1 further retry failed (429)
- 10:12:04 - Attempt 2 retry failed (429)
- Process terminated without completing

### Evidence
Output file: `/tmp/claude-1000/-home-div-brain/tasks/bca4a69.output` (31KB, 585 lines)
- Contains 429 error stack traces
- Shows retry backoff attempts
- No final Success/Duration report (crashed before completion)

### Observations
During retry attempts, Gemini attempted some file operations that failed:
- `Error executing tool read_file: File path must be within workspace directories`
- `Error executing tool replace: A secondary check by an LLM determined that no changes were necessary`
- These suggest Gemini was trying to work but couldn't due to API capacity

### Workarounds
1. Wait for Gemini API capacity to return
2. Use alternative model (if gemini-cli supports other models)
3. Test desktop backend with simpler task that doesn't require Gemini execution
4. Use direct Desktop MCP tools to bypass Gemini orchestration layer

### Next Steps
- [ ] Check if Gemini API has capacity limits we can monitor
- [ ] Consider fallback to gemini-flash or other model tier
- [ ] Document which tasks are safe to run during capacity constraints
- [ ] Test if direct Desktop MCP bypass works for simple tasks
