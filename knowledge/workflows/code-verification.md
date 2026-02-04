# Code Verification Workflow

Systematic approach to verify Claude-generated code while learning.

## Philosophy

Verification isn't just about catching bugs - it's about understanding. Each verification step is a learning opportunity. Match effort to risk.

## Verification Levels

### Quick (1-2 min)
**When:** Simple utilities, config changes, documentation updates

| Check | How | Learn |
|-------|-----|-------|
| Syntax | Save file, watch for red squiggles | IDE knows the language rules |
| Types | `tsc --noEmit` or equivalent | Type system catches mismatches |
| Lint | `eslint .` / `ruff check` | Style and common gotchas |

**Learning hook:** Ask Claude "What pattern is this code using?" after it works.

### Standard (5-10 min)
**When:** New features, bug fixes, anything that changes behavior

| Check | How | Learn |
|-------|-----|-------|
| Unit test | Run existing tests + add new one | Tests document expected behavior |
| Edge cases | "What if input is null/empty/huge?" | Boundary conditions reveal assumptions |
| Manual run | Actually execute the code path | Nothing beats seeing it work |
| Read diff | `git diff` line by line | Understand every change |

**Learning hook:** Before running, predict what each function will do. Check predictions.

### Deep (15-30 min)
**When:** Security-sensitive, data-handling, production deployments, unfamiliar domains

| Check | How | Learn |
|-------|-----|-------|
| Integration test | End-to-end scenarios | Components must work together |
| Security scan | `npm audit` / `bandit` / OWASP checks | Know the vulnerability patterns |
| Code review | Line-by-line with questions | Challenge every assumption |
| Documentation | Does README match behavior? | Docs are part of the code |

**Learning hook:** Ask Claude to explain the hardest part. Then explain it back.

## Decision Matrix

| Code Type | Default Level | Upgrade If... |
|-----------|---------------|---------------|
| Config/docs | Quick | Changes deployment behavior |
| Utils/helpers | Quick | Used in critical paths |
| Features | Standard | Handles user data |
| Auth/security | Deep | Always |
| Data pipelines | Deep | Always |
| New patterns | Standard+ | Unfamiliar territory |

## Proportional Effort

```
Risk × Complexity = Verification Level

Low risk + Simple → Quick
Any risk + Complex → Standard minimum
High risk + Any → Deep
```

## Verification Capture

After verifying, record:

```markdown
## Verification: [feature-name]
- **Level:** Quick/Standard/Deep
- **Checks passed:** [list]
- **Issues found:** [none or list]
- **Learning:** [one thing you understood better]
```

## Incremental Adoption

Start here:
1. **Week 1:** Always run Quick level
2. **Week 2:** Add Standard for new features
3. **Week 3:** Add Deep for security-related
4. **Week 4:** Develop intuition for which level

## Red Flags Requiring Deep Verification

- Modifies authentication/authorization
- Handles PII or sensitive data
- Writes to production systems
- Uses `eval`, `exec`, or dynamic code
- Disables security features
- Has complex conditional logic
- Unfamiliar library/pattern

## See Also

- [verification-checklist.md](../patterns/verification-checklist.md) - Quick reference checklist
