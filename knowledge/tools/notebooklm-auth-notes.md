# NotebookLM Auth Notes

## Current Working Procedure (2026-02-08)

### Quick Reference
```bash
# 1. Run nlm.exe login on Windows (from WSL)
powershell.exe -Command "& 'C:\Users\din18\.local\bin\nlm.exe' login"

# 2. It will crash at line 229 — this is EXPECTED
#    Cookies are extracted before the crash

# 3. Save via MCP save_auth_tokens tool with:
#    - cookies: Cookie header string (SID, HSID, SSID, APISID, SAPISID, etc.)
#    - csrf_token: from traceback output (AE_H9g...)
#    - session_id: from existing auth.json or traceback

# 4. Verify with notebook_list call
```

### Auth File Location
- **Windows:** `C:\Users\din18\.notebooklm-mcp-cli\auth.json`
- **WSL path:** `/mnt/c/Users/din18/.notebooklm-mcp-cli/auth.json`

### Known Issues

1. **nlm.exe login crashes at line 229** (`login_callback` in main.py)
   - Cookies ARE extracted before the crash
   - The crash happens at the "Successfully authenticated" print statement
   - auth.json may NOT be updated despite successful cookie extraction
   - Workaround: read csrf_token from traceback output, use save_auth_tokens MCP

2. **Cookie expiry** — Google session cookies last hours, not days
   - Always verify auth with `notebook_list` before starting work
   - If expired: re-run the 4-step procedure above

3. **Port 9222 conflict** (historical)
   - Old `notebooklm-mcp-auth.exe` conflicted with Claude Desktop debug mode
   - Current `nlm.exe` approach avoids this — uses its own Chrome instance

### Key Cookies (what matters)
The essential cookies for NLM auth are: SID, HSID, SSID, APISID, SAPISID,
__Secure-1PAPISID, __Secure-3PAPISID, __Secure-1PSID, __Secure-3PSID,
OSID, __Secure-OSID, SIDCC, __Secure-1PSIDCC, __Secure-3PSIDCC, __Secure-1PSIDTS

### Tools
- **nlm.exe:** `/mnt/c/Users/din18/.local/bin/nlm.exe` (Windows binary)
- **MCP save:** `mcp__notebooklm-mcp__save_auth_tokens` (cookies + csrf_token + session_id)
- **MCP verify:** `mcp__notebooklm-mcp__notebook_list`

## Related Beads
- brain-zpd (closed): WSL Cookie Bridge solution
- brain-qms: NotebookLM Library Pipeline
