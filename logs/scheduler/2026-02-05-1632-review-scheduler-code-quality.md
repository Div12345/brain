---
task: review-scheduler-code-quality
run_id: run-2026-02-05-163205
started: 2026-02-05T16:32:05.742809
ended: 2026-02-05T16:36:19.547834
duration_seconds: 253.81
status: completed
exit_code: 0
capacity_before_5h: 32.0
capacity_before_7d: 77.0
capacity_after_5h: 35.0
capacity_after_7d: 77.0
---

# Execution Log: review-scheduler-code-quality

**Run ID:** run-2026-02-05-163205
**Status:** ✓ Completed
**Duration:** 253.8s

## Output

```
YOLO mode is enabled. All tool calls will be automatically approved.
Loaded cached credentials.
YOLO mode is enabled. All tool calls will be automatically approved.
Hook registry initialized with 0 hook entries
Attempt 1 failed: You have exhausted your capacity on this model. Your quota will reset after 0s.. Retrying after 289.10416ms...
Attempt 1 failed: You have exhausted your capacity on this model. Your quota will reset after 1s.. Retrying after 1826.312935ms...
Attempt 1 failed: You have exhausted your capacity on this model. Your quota will reset after 1s.. Retrying after 1607.8003800000001ms...
Attempt 1 failed: You have exhausted your capacity on this model. Your quota will reset after 1s.. Retrying after 1633.0189799999998ms...
Attempt 1 failed: You have exhausted your capacity on this model. Your quota will reset after 1s.. Retrying after 1396.530292ms...
Attempt 1 failed: You have exhausted your capacity on this model. Your quota will reset after 1s.. Retrying after 1579.6993420000001ms...
# Code Review Summary: cc-scheduler

## Goal
Perform a thorough code review of the cc-scheduler codebase at `~/brain/tools/cc-scheduler/`. The focus is on correctness, edge cases, and maintainability.

## Review Output

### Critical Issues (must fix)

1.  **Unix-specific `os.set_blocking` in `executor.py`**:
    *   **Details**: The line `os.set_blocking(process.stdout.fileno(), False)` is Unix-specific and will cause the scheduler to crash on Windows.
    *   **Fix**: Replace with platform-agnostic I/O multiplexing (e.g., `select.select()`) or adopt `asyncio` subprocess handling for cross-platform compatibility.
2.  **Test file leakage in `tests/test_tasks.py`**:
    *   **Details**: Tests use `tempfile.NamedTemporaryFile(delete=False)` without explicit cleanup, leading to accumulation of temporary files and potential test pollution.
    *   **Fix**: Set `delete=True` for `NamedTemporaryFile` and ensure content is flushed before reading, or use `pytest` fixtures with proper `tmp_path` handling for automatic cleanup.
3.  **Inconsistent validation behavior in `tasks.py`**:
    *   **Details**: Invalid `skill` values trigger a warning and default to `None`, but invalid `model_hint` or `backend` values raise a `ValueError`. This inconsistency can make debugging difficult, as some errors fail silently while others cause a full task failure.
    *   **Fix**: Standardize error handling: either raise `ValueError` for all invalid configurations or consistently log warnings and default to a safe value. Prefer early and clear failure for invalid inputs.

### Suggested Improvements (nice to have)

1.  **Fragile custom YAML parser in `tasks.py`**:
    *   **Details**: The `parse_frontmatter` function uses a custom regex and string manipulation for YAML parsing. This approach is prone to errors with more complex YAML structures (e.g., quoted strings with colons, nested objects, multi-line strings).
    *   **Improvement**: Leverage a robust YAML library like PyYAML (which is already imported in `executor.py`) to handle frontmatter parsing: `frontmatter = yaml.safe_load(frontmatter_str)`.
2.  **Magic constant `TOKENS_PER_PERCENT` in `ccq`**:
    *   **Details**: The `TOKENS_PER_PERCENT = 5000` constant is a "rough estimate" and not calibrated.
    *   **Improvement**: Implement a calibration mechanism using historical data from `history.jsonl` to dynamically adjust this value, improving the accuracy of token estimates.
3.  **Inconsistent import placement in `ccq`**:
    *   **Details**: Some imports are at the top-level, while others are placed inline within functions (e.g., `from lib.executor import check_desktop_availability`).
    *   **Improvement**: Consolidate all imports at the top of the file (`ccq`) for better readability and to prevent potential circular import issues.
4.  **Broad `except Exception` in `executor.py`**:
    *   **Details**: The `try-except` block around the subprocess output streaming uses a bare `except Exception`, which can swallow critical error information and make debugging difficult.
    *   **Improvement**: Catch more specific exceptions or, if a broad catch is necessary, ensure the full traceback is logged to aid in diagnosing unexpected issues.
5.  **Hardcoded Desktop Check URL in `executor.py`**:
    *   **Details**: `DESKTOP_CHECK_URL` is a hardcoded string (`"http://127.0.0.1:9229/json"`).
    *   **Improvement**: Move this URL to `config.yaml` to make it configurable and centralize configuration settings.
6.  **Complex timeout handling in `executor.py`**:
    *   **Details**: Manual polling for process completion and timeout checking can be complex and less efficient.
    *   **Improvement**: Explore alternative, more idiomatic Python patterns for subprocess management with timeouts, such as `subprocess.run(timeout=...)` (if output streaming is not critical) or event-driven I/O libraries.
7.  **Inconsistent return types for `main()` in `ccq`**:
    *   **Details**: The `main()` function implicitly returns `None` for many commands but explicitly returns `int` (0 or 1) for `cmd_run` and `cmd_add`.
    *   **Improvement**: Standardize the return type of `main()` (e.g., always return an integer exit code) for clarity and consistency with CLI best practices.
8.  **`None` as a valid skill in `tasks.py`**:
    *   **Details**: `VALID_SKILLS` includes `None`. While `None` might represent the absence of a skill, including it in a list of *valid* skills can be conceptually confusing.
    *   **Improvement**: Clarify the semantic meaning of `None` for skill. If it means "no specific skill required," that's fine, but the validation logic should treat it consistently as a default or absence rather than a "skill."
9.  **Placeholder `is_runnable` in `tasks.py`**:
    *   **Details**: The `is_runnable` property currently always returns `True`.
    *   **Improvement**: Implement the actual dependency resolution logic for tasks to accurately determine if they can be run, enhancing the scheduler's intelligence.
10. **Inconsistency in Gemini model names**:
    *   **Details**: `executor.py` defaults to `gemini-3-pro-preview` for desktop backend, while `config.yaml` specifies `gemini-2.5-pro`.
    *   **Improvement**: Align the default model in `executor.py` with the configuration, or provide a clear mechanism for the configuration to override the hardcoded default consistently.
11. **Hardcoded schedule logic in `config.yaml`**:
    *   **Details**: The `schedule` section explicitly defines `autonomous_start`, `autonomous_end`, etc., based on a specific "Night owl" pattern.
    *   **Improvement**: While well-documented, consider if a more abstract scheduling model (e.g., defining "active" and "idle" periods) could make the configuration more general-purpose and reusable for different user habits.

### Test Gap Analysis

*   **Missing test cases for `parse_frontmatter` (tasks.py)**:
    *   Malformed YAML (e.g., missing delimiters, invalid syntax).
    *   Empty frontmatter or files.
    *   Files with only body, no frontmatter.
    *   Edge cases like Unicode characters in frontmatter or body.
*   **Incomplete `lib/tasks.py` validation tests**:
    *   The `test_validates_model_hint_values` and `test_validates_backend_values` expect `parse_task_file` to return `None` on invalid input. However, the current `parse_task_file` raises `ValueError` before returning `None`, which is inconsistent and might break these tests.
*   **Missing tests for `executor.py` logic**:
    *   `check_desktop_availability` and its fallback logic.
    *   Various error conditions during `execute_task` (e.g., subprocess failures, timeout handling).
    *   The correctness of the `build_prompt` function for different modes and skill invocations.
*   **Inadequate test coverage for budget and scheduling**:
    *   `lib/budget.py` and `lib/scheduler.py` are core components but lack explicit test files or comprehensive coverage. These are crucial for the scheduler's correctness.
*   **General improvement**: Introduce `pytest` fixtures for setting up and tearing down temporary test environments to improve test maintainability and prevent side effects.

### Overall Quality Assessment

**3/5 - Good Foundation, Needs Robustification and Refinement**

The `cc-scheduler` project demonstrates a clear understanding of the problem space and a well-structured approach to solving it. The separation into `tasks`, `executor`, and `ccq` is logical. The configuration file is comprehensive and well-documented.

However, the codebase has several areas that require significant attention to improve its robustness, maintainability, and error handling. The reliance on custom parsing instead of existing libraries, platform-specific code, and inconsistent validation logic introduces fragility. Addressing the identified critical issues and implementing the suggested improvements, especially enhancing test coverage for core components, will elevate this project to a much higher quality standard.

---

I have now completed the code review based on the files provided. Do you have any further questions or would you like me to elaborate on any specific point?

```
