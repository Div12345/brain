#!/bin/bash
# Sequential orchestration evaluation runner
# Tests different Gemini models steering Desktop through scenarios
# MUST run sequentially — Desktop is a single resource

set -euo pipefail

LOG_DIR="$HOME/brain/logs/gemini/eval-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$LOG_DIR"
RESULTS_FILE="$LOG_DIR/results.jsonl"

cd "$HOME/brain"

run_scenario() {
    local scenario_name="$1"
    local model="$2"
    local prompt="$3"
    local timeout="${4:-180}"
    local log_file="$LOG_DIR/${scenario_name}-${model}.log"

    echo "=== Running: $scenario_name with $model ===" | tee -a "$log_file"
    echo "Started: $(date)" | tee -a "$log_file"

    # Run with timeout
    timeout "${timeout}s" gemini -p "$prompt" --yolo --model "$model" 2>&1 | tee -a "$log_file" || true

    local exit_code=$?
    echo "Exit code: $exit_code" >> "$log_file"
    echo "Finished: $(date)" >> "$log_file"

    # Extract result markers from output
    local status="UNKNOWN"
    if grep -q "SCENARIO_PASS" "$log_file"; then
        status="PASS"
    elif grep -q "SCENARIO_FAIL" "$log_file"; then
        status="FAIL"
    elif grep -q "EXPERIMENT_COMPLETE" "$log_file"; then
        status="PASS"
    fi

    local turns=$(grep -oP 'TURNS_USED:\s*\K\d+' "$log_file" || echo "0")
    local quality=$(grep -oP 'FINAL_QUALITY:\s*\K\d+' "$log_file" || echo "0")

    # Log result as JSONL
    echo "{\"scenario\":\"$scenario_name\",\"model\":\"$model\",\"status\":\"$status\",\"turns\":$turns,\"quality\":$quality,\"exit_code\":$exit_code}" >> "$RESULTS_FILE"

    echo "Result: $status (turns=$turns, quality=$quality)" | tee -a "$log_file"
    echo ""

    # Brief cooldown between scenarios to let Desktop settle
    sleep 5
}

# ============================================================
# SCENARIO 1: Simple single-turn (baseline)
# ============================================================
SCENARIO_1_PROMPT='You have claude_desktop MCP tools. Do this sequence:
1. Call claude_desktop_new
2. Call claude_desktop_send with message="What are the three laws of thermodynamics? List them numbered." wait_for_response=true timeout=60
3. Read response with claude_desktop_read
4. Check: does response contain all 3 laws numbered? If yes: print SCENARIO_PASS. If no: print SCENARIO_FAIL
5. Print TURNS_USED: 1
6. Print FINAL_QUALITY: <1-5 based on completeness>'

# ============================================================
# SCENARIO 2: Multi-turn refinement
# ============================================================
SCENARIO_2_PROMPT='You have claude_desktop MCP tools. Complete this multi-turn task:

GOAL: Get Claude Desktop to write a Python function that validates email addresses with comprehensive edge case handling.

PROTOCOL:
1. claude_desktop_new (fresh conversation)
2. claude_desktop_send asking for an email validation function
3. claude_desktop_read the response
4. EVALUATE: Does it handle: empty string, missing @, multiple @, unicode, very long addresses, common TLDs?
5. If not comprehensive enough, send a follow-up asking for specific improvements
6. Repeat evaluation up to 3 times max
7. When done, print:
   - TURNS_USED: <number of send/read cycles>
   - FINAL_QUALITY: <1-5>
   - SCENARIO_PASS if quality >= 3, else SCENARIO_FAIL'

# ============================================================
# SCENARIO 3: Error recovery
# ============================================================
SCENARIO_3_PROMPT='You have claude_desktop MCP tools. Test error recovery:

1. claude_desktop_new
2. claude_desktop_send with message="Write a very long essay about the history of computing, at least 2000 words." wait_for_response=false timeout=10
3. Wait 5 seconds
4. Call claude_desktop_status to check if generating
5. Call claude_desktop_read_interim to see partial output
6. Call claude_desktop_stop to halt generation
7. Call claude_desktop_read to capture what was generated
8. EVALUATE: Did you successfully stop mid-generation and capture partial output?
9. Print SCENARIO_PASS if you captured partial text, SCENARIO_FAIL otherwise
10. Print TURNS_USED and FINAL_QUALITY'

# ============================================================
# SCENARIO 4: Complex multi-step with judgment
# ============================================================
SCENARIO_4_PROMPT='You have claude_desktop MCP tools. Complete this complex task:

GOAL: Ask Claude Desktop to analyze the pros and cons of microservices vs monolith architecture for a 5-person startup, then ask it to make a concrete recommendation with justification.

PROTOCOL:
1. claude_desktop_new
2. Send analysis request, wait for response
3. Read and evaluate: Is the analysis balanced? Does it cover cost, complexity, team size, deployment?
4. If analysis is shallow, ask for specific depth on weak areas
5. Send follow-up asking for a concrete recommendation with justification
6. Read and evaluate: Is the recommendation clear and well-justified?
7. Print TURNS_USED, FINAL_QUALITY (1-5), SCENARIO_PASS/FAIL (pass if quality >= 3)
8. Print REASONING: <why you gave that quality score>'

echo "=== Orchestration Evaluation ===" | tee "$LOG_DIR/summary.log"
echo "Started: $(date)" | tee -a "$LOG_DIR/summary.log"
echo "Models to test: $@" | tee -a "$LOG_DIR/summary.log"
echo "" | tee -a "$LOG_DIR/summary.log"

# Run each model through all scenarios
for model in "$@"; do
    echo ">>> Testing model: $model" | tee -a "$LOG_DIR/summary.log"
    run_scenario "s1-simple" "$model" "$SCENARIO_1_PROMPT" 120
    run_scenario "s2-multiturn" "$model" "$SCENARIO_2_PROMPT" 300
    run_scenario "s3-recovery" "$model" "$SCENARIO_3_PROMPT" 180
    run_scenario "s4-complex" "$model" "$SCENARIO_4_PROMPT" 300
done

echo "" | tee -a "$LOG_DIR/summary.log"
echo "=== RESULTS ===" | tee -a "$LOG_DIR/summary.log"
cat "$RESULTS_FILE" | tee -a "$LOG_DIR/summary.log"
echo "" | tee -a "$LOG_DIR/summary.log"
echo "Finished: $(date)" | tee -a "$LOG_DIR/summary.log"
echo "Logs at: $LOG_DIR"
