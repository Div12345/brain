---
task: review-scheduler-code-quality
run_id: run-2026-02-05-145432
started: 2026-02-05T14:54:32.036950
ended: 2026-02-05T15:00:02.383820
duration_seconds: 330.35
status: completed
exit_code: 0
capacity_before_5h: 13.0
capacity_before_7d: 74.0
capacity_after_5h: 0.0
capacity_after_7d: 74.0
---

# Execution Log: review-scheduler-code-quality

**Run ID:** run-2026-02-05-145432
**Status:** ✓ Completed
**Duration:** 330.3s

## Output

```
YOLO mode is enabled. All tool calls will be automatically approved.
Loaded cached credentials.
YOLO mode is enabled. All tool calls will be automatically approved.
Hook registry initialized with 0 hook entries
Okay, I will initiate a code review of the `cc-scheduler` codebase using Claude Desktop.
Error executing tool claude_desktop_new: Tool "claude_desktop_new" not found in registry. Tools must use the exact names that are registered. Did you mean one of: "save_memory", "list_directory", "read_file"?
It appears the `claude_desktop_*` tools are not available in my current environment, despite the instructions in `GEMINI.md`. I am unable to initiate a conversation with Claude Desktop.

As I cannot use the specified tools, and I'm instructed not to return an empty response or interact with the user to clarify, I will proceed by directly examining the `cc-scheduler` codebase myself using the available `list_directory` tool. This will allow me to begin gathering information relevant to the code review.
Error executing tool list_directory: Error listing directory: ENOENT: no such file or directory, stat '/home/div/brain/~/brain/tools/cc-scheduler'
My apologies, I used an incorrect path. The `~` character is not being resolved as expected within the tool call. I will use the absolute path `/home/div/brain/tools/cc-scheduler/` to list the directory contents.
I have the `cc-scheduler` directory listing. As I cannot use Claude Desktop, I will manually review `lib/tasks.py`, `lib/executor.py`, `ccq`, `config.yaml`, `tests/test_tasks.py`, and `tests/test_executor.py` for error handling, edge cases, test coverage, configuration, and security. I'll start by reading `lib/tasks.py`.
Okay, I've analyzed `lib/tasks.py` and rated its quality at 3/5 due to several issues. Critical fixes include replacing the fragile custom YAML parser with a robust library (like PyYAML), improving error handling in `parse_task_file` for better debugging, and clarifying validation for `mcps_required` to avoid silent data type conversions.

Suggested improvements involve making `Task.is_runnable` functional or removing it, parsing `timeout` into a structured type, making path constants configurable, using Python's `logging` module, and potentially encapsulating `PRIORITY_MAP`.

Regarding test gaps, I anticipate needing tests for malformed YAML, `parse_frontmatter` edge cases, `mcps_required` type handling, invalid `skill`, `model_hint`, `backend` values, and `deadline` parsing errors.

Now, I'll review `tests/test_tasks.py` to assess current test coverage.
I've reviewed `tests/test_tasks.py`, finding its quality to be 2/5 due to a lack of robust testing. Critical gaps include: tests for malformed or complex YAML, thorough error handling in `parse_task_file` (especially for `mcps_required` type issues), `deadline` parsing (both valid and invalid formats), comprehensive `Task` class default value checks, and string-to-integer `PRIORITY_MAP` functionality. Current tests only cover basic valid field parsing and some defaults. Next, I will examine `lib/executor.py`.
`lib/executor.py`, which manages task execution, reveals critical security and robustness flaws. The most pressing is a potential command injection vulnerability in `subprocess.Popen` where user-controlled `prompt` data is used. This requires immediate investigation into how `gemini` and `claude` CLIs interpret their `-p` argument, and potentially sanitization. Broader `try-except` blocks obscure specific errors, particularly around `subprocess.Popen` and `move_task` failures. Configuration loading of `config.yaml` is decentralized and lacks robust error handling. `TASKS_DIR` relies on a hardcoded path.

Suggested improvements include optimizing timeout handling, externalizing the verbose `desktop_wrapper` string, creating a centralized `subprocess` utility, adopting Python's `logging` module, making Gemini quota detection more robust than string matching, and improving `parse_timeout` validation.

Anticipated test gaps (to be confirmed by `tests/test_executor.py` review) include: security tests for command injection, timeout scenarios, `backend: auto` switching, invalid configuration loading, executable not found errors, task movement failures, Gemini quota handling, and `parse_timeout` edge cases.

I will now proceed to review `tests/test_executor.py`.
`tests/test_executor.py` is critically deficient, achieving a 1/5 quality score, as it exclusively provides basic coverage for `move_task` and fails to address the majority of `lib/executor.py`'s functionality and vulnerabilities. Key omissions include tests for command injection, `execute_task`'s success/failure modes (including timeouts, backend switching, error handling for `subprocess.Popen`), `build_prompt` and `build_command`'s various logic branches, `parse_timeout` edge cases, `check_desktop_availability`, `config.yaml` loading, and Gemini quota detection. This test suite requires a comprehensive rewrite. I will now examine `ccq`.
`ccq` is a well-structured CLI, but its quality is limited by inherited issues from `lib/tasks.py` and `lib/executor.py`, making it prone to errors from malformed YAML and command injection vulnerabilities. `load_config` needs better error handling for `config.yaml`. The `os.chdir()` call should be replaced with explicit path handling, and the desktop backend's mocked capacity should be re-evaluated. The hardcoded `TOKENS_PER_PERCENT` should be configurable. Test gaps are significant, especially concerning integration tests for `ccq run`'s various execution and failure modes, budget/schedule adherence, and `ccq add`, as well as error handling for `config.yaml` loading. I will now examine `config.yaml`.
I've reviewed `config.yaml`, rating it a 4/5. It effectively centralizes most scheduler configurations, including flexible path definitions and backend flags. Key issues include the `TOKENS_PER_PERCENT` being hardcoded elsewhere, and the lack of a formal schema. Code integration seems good, but `ccq`'s YAML loading needs more robust error handling. Security-wise, command flags are correctly structured; the primary risk remains with `prompt` content in `lib/executor.py`. Test gaps exist for verifying all configuration values are correctly loaded and used, and for handling edge cases like missing or invalid sections. Next, I will review `lib/capacity`, `lib/log_utils`, `lib/budget`, `lib/scheduler`, `lib/task_queue` by first listing the contents of the `lib` directory.
Alright, `lib` files reviewed are `tasks.py` and `executor.py`. I'll now examine `budget.py`, `capacity.py`, `log_utils.py`, `scheduler.py`, and `task_queue.py`, along with their respective tests. Starting with `capacity.py`.
I've reviewed `lib/capacity.py` (4/5 quality), noting its reliance on external API and credentials, and robust error handling for `get_access_token` and `parse_date`. `check_capacity` returns `None` on errors but lacks detailed logging, a potential debug hinderance. I've noted a security consideration regarding credential file permissions.

Anticipated test gaps (due to missing test file) include `get_access_token` scenarios (valid/invalid JSON, missing token), `check_capacity` with mocked successful and failing API calls, `Capacity` property validation, and `format_capacity` output. I will now read `budget.py`.
Attempt 1 failed: You have exhausted your capacity on this model. Your quota will reset after 0s.. Retrying after 322.689542ms...
Attempt 1 failed: You have exhausted your capacity on this model. Your quota will reset after 1s.. Retrying after 1816.693137ms...
`lib/budget.py` (4/5 quality) provides robust budget tracking with data persistence and proper date handling using dataclasses for clear structures. Error handling for file operations is good, but `KeyError` could be more explicitly caught in `from_dict` methods. I've noted an apparent inconsistency in `DailyAllocation` handling, which needs ensuring that all dictionary entries in `daily_allocations` are reliably converted into `DailyAllocation` objects. The `rebalance_week` logic is basic but functional, while `_update_cost_model` uses effective EMA. Path configurability remains an ongoing consideration.

Significant test gaps exist, as `tests/test_budget.py` is absent. Key test areas include `BudgetTracker` initialization; `WeeklyBudget` loading, saving, and rollover; various daily/weekly allocation calculations; accurate usage recording (autonomous and user-directed); cost model updates and estimations; session budget functionality (start, load, update, check); and `format_budget_status` accuracy.

I will now read `lib/scheduler.py`.
Attempt 1 failed: You have exhausted your capacity on this model. Your quota will reset after 0s.. Retrying after 236.471344ms...
I've reviewed `lib/scheduler.py` (4/5 quality), finding it well-designed but with some robustness concerns. `ScheduleConfig.from_dict` needs more consistent use of `dict.get()` and `try-except` blocks for time parsing to prevent `KeyError` or `ValueError` with incomplete `config.yaml` data. Time window logic needs explicit handling for phases spanning midnight. Priority scoring's project boost needs robustness for `task.tags` usage. Both `plan_session` and `check_budget` use a hardcoded 5000 tokens-per-percent, which should be configurable.

Significant test gaps exist, as there's no `tests/test_scheduler.py`. Critical tests needed include: `ScheduleConfig.from_dict` with various configurations, comprehensive time window logic tests (including midnight crossing), priority scoring across diverse task attributes, task ranking and selection, session and weekly planning within constraints, budget checks, and confidence-based routing at all thresholds.

I will now read `lib/task_queue.py`.
Attempt 1 failed: You have exhausted your capacity on this model. Your quota will reset after 0s.. Retrying after 432.560772ms...
`lib/task_queue.py` (4/5 quality) effectively manages tasks across projects with good dependency handling. I've noted a convoluted path resolution in `TaskQueue.load_all` that could be simplified and a dependency on `lib/tasks.py`'s parsing. `check_dependencies` could optimize `pending_names` creation for performance. `load_projects_from_config` needs better error handling for missing project paths in `config.yaml`.

Significant test gaps exist without `tests/test_task_queue.py`. Key tests should cover: `ProjectConfig` name generation; `TaskQueue` initialization with and without projects; comprehensive `load_all` scenarios including multiple projects, completed tasks, and invalid files; all `check_dependencies` cases; `get_blocked_tasks`, `get_runnable_tasks`, and specific task retrieval methods; accurate `summary` calculations; `load_projects_from_config` with various configurations and error conditions; and `format_queue_status` output.

Now, I will proceed to read `lib/log_utils.py`.
Attempt 1 failed: You have exhausted your capacity on this model. Your quota will reset after 1s.. Retrying after 1180.646176ms...
`lib/log_utils.py` (4.5/5 quality) is well-designed, using YAML frontmatter for human readability, and `index.jsonl` and `history.jsonl` for machine parsing, enhancing structured logging and feedback loop analysis. It robustly captures execution details, truncates long outputs, and categorizes errors effectively, though `classify_error` could be expanded. A rough token estimation is included.

However, `json.loads` calls in `get_history_stats` and `get_recent_logs` lack `try-except json.JSONDecodeError` blocks, making them vulnerable to malformed JSON.

Test gaps (assuming no `tests/test_log_utils.py`) require tests for directory creation, `run_id` generation, `log_execution` with various inputs (success/failure, capacity info, long/edge-case outputs), `append_to_index`, comprehensive `classify_error` scenarios, `estimate_tokens`, `append_to_history`, robust stats generation (including malformed JSON handling), and `format_recent_logs`.

Having reviewed all core Python files and `config.yaml`, and identified pervasive test gaps, I will now compile a comprehensive final summary adhering to the specified structure.

```
