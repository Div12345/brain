Loaded cached credentials.
Hook registry initialized with 0 hook entries
Server 'paper-search' supports tool updates. Listening for changes...
Server 'obsidian' supports tool updates. Listening for changes...
Server 'obsidian' supports resource updates. Listening for changes...
Server 'zotero' supports tool updates. Listening for changes...
Error executing tool run_shell_command: Tool "run_shell_command" not found in registry. Tools must use the exact names that are registered. Did you mean one of: "search_file_content", "search_pubmed", "search_iacr"?
Attempt 1 failed: You have exhausted your capacity on this model. Your quota will reset after 0s.. Retrying after 225.35581399999998ms...
Attempt 2 failed: You have exhausted your capacity on this model. Your quota will reset after 0s.. Retrying after 5.141630999999999ms...
Error executing tool zotero_get_item_fulltext: Tool execution denied by policy.
Attempt 1 failed: You have exhausted your capacity on this model. Your quota will reset after 1s.. Retrying after 1660.77644ms...
Error executing tool zotero_get_item_metadata: Tool execution denied by policy.
Error executing tool search_pubmed: Tool execution denied by policy.
Attempt 1 failed: You have exhausted your capacity on this model. Your quota will reset after 0s.. Retrying after 991.72834ms...
Attempt 1 failed: You have exhausted your capacity on this model. Your quota will reset after 1s.. Retrying after 1382.3715009999999ms...
Attempt 2 failed: You have exhausted your capacity on this model. Your quota will reset after 1s.. Retrying after 1744.2133580000002ms...
Error when talking to Gemini API Full report available at: /tmp/gemini-client-error-Turn.run-sendMessageStream-2026-02-02T04-12-00-598Z.json TerminalQuotaError: You have exhausted your capacity on this model. Your quota will reset after 21h36m23s.
    at classifyGoogleError (file:///home/div/.nvm/versions/node/v24.13.0/lib/node_modules/@google/gemini-cli/node_modules/@google/gemini-cli-core/dist/src/utils/googleQuotaErrors.js:214:28)
    at retryWithBackoff (file:///home/div/.nvm/versions/node/v24.13.0/lib/node_modules/@google/gemini-cli/node_modules/@google/gemini-cli-core/dist/src/utils/retry.js:130:37)
    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
    at async GeminiChat.makeApiCallAndProcessStream (file:///home/div/.nvm/versions/node/v24.13.0/lib/node_modules/@google/gemini-cli/node_modules/@google/gemini-cli-core/dist/src/core/geminiChat.js:421:32)
    at async GeminiChat.streamWithRetries (file:///home/div/.nvm/versions/node/v24.13.0/lib/node_modules/@google/gemini-cli/node_modules/@google/gemini-cli-core/dist/src/core/geminiChat.js:253:40)
    at async Turn.run (file:///home/div/.nvm/versions/node/v24.13.0/lib/node_modules/@google/gemini-cli/node_modules/@google/gemini-cli-core/dist/src/core/turn.js:66:30)
    at async GeminiClient.processTurn (file:///home/div/.nvm/versions/node/v24.13.0/lib/node_modules/@google/gemini-cli/node_modules/@google/gemini-cli-core/dist/src/core/client.js:458:26)
    at async GeminiClient.sendMessageStream (file:///home/div/.nvm/versions/node/v24.13.0/lib/node_modules/@google/gemini-cli/node_modules/@google/gemini-cli-core/dist/src/core/client.js:554:20)
    at async file:///home/div/.nvm/versions/node/v24.13.0/lib/node_modules/@google/gemini-cli/dist/src/nonInteractiveCli.js:177:34
    at async main (file:///home/div/.nvm/versions/node/v24.13.0/lib/node_modules/@google/gemini-cli/dist/src/gemini.js:474:9) {
  cause: {
    code: 429,
    message: 'You have exhausted your capacity on this model. Your quota will reset after 21h36m23s.',
    details: [ [Object], [Object] ]
  },
  retryDelayMs: 77783510.66389899
}
An unexpected critical error occurred:[object Object]
