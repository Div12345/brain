# Agent Evaluation Frameworks Research

**Date:** 2026-02-03
**Bead:** brain-19s

## Key Concepts

### Transcript Analysis
A **transcript** (trace/trajectory) is the complete record of a trial:
- All outputs and tool calls
- Reasoning and intermediate results
- Full messages array from API calls and responses

Per [Anthropic's engineering blog](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), teams should invest in transcript viewing tooling and regularly read them. When tasks fail, transcripts reveal whether the agent made a genuine mistake or graders rejected a valid solution.

### Grader Types
Agent evaluations combine three grader types:
1. **Code-based** - Deterministic checks
2. **Model-based** - LLM-as-judge for breadth
3. **Human** - Essential for nuanced/high-stakes situations

Per [LangChain State of Agents](https://www.langchain.com/state-of-agent-engineering): Human review (59.8%) remains essential, while LLM-as-judge (53.3%) is increasingly used.

## Frameworks

### CLEAR Framework
[Multi-dimensional enterprise framework](https://arxiv.org/html/2511.14136v1):
- **C**ost - Token/compute efficiency
- **L**atency - Response time
- **E**fficacy - Task completion quality
- **A**ssurance - Safety and alignment
- **R**eliability - Consistency across runs

### UK AISI Frameworks
[2025 review](https://www.aisi.gov.uk/blog/our-2025-year-in-review) introduced:
- Bayesian GLMs for evaluator reliability
- Transcript-level analysis for understanding agent behavior

## Tools (2026)

| Tool | Focus |
|------|-------|
| [Maxim AI](https://www.getmaxim.ai/articles/top-5-tools-for-agent-evaluation-in-2026/) | Agent reliability, cost efficiency |
| LangSmith | Tracing, debugging, evaluation |
| Arize | Observability, drift detection |
| Langfuse | Open-source tracing |
| Galileo | Output quality measurement |

### Open-Source
- **Inspect** - UK AISI's eval framework
- **InspectSandbox** - Sandboxed execution
- **ControlArena** - Control evaluations

## Benchmarks

**AgentBench 2025** includes 100+ scenarios:
- Multi-leg travel booking
- Budget management
- Cloud infrastructure config
- Software UI navigation

Assesses: planning accuracy, tool-use fluency, multi-turn coherence

## Industry Stats (2025-2026)

From [LangChain survey](https://www.langchain.com/state-of-agent-engineering) of 1,300+ professionals:
- **57%** have agents in production
- **32%** cite quality as top barrier
- **52.4%** run offline evaluations on test sets

## Relevance for Brain System

For our overnight agent and scheduler:

1. **Transcript capture** - Already logging to logs/scheduler/
2. **Grading options**:
   - Code-based: Check success criteria, file outputs
   - Model-based: Architect verification (already doing this)
   - Human: User review at briefing time
3. **Metrics to track**:
   - Task completion rate
   - Token efficiency (cost per task)
   - Bounce-back rate (retries needed)
   - Verification pass rate

## Next Steps

- [ ] Implement structured transcript format for scheduler logs
- [ ] Add cost tracking per task
- [ ] Create eval dashboard (simple: success/fail/retry counts)
- [ ] Consider LangSmith/Langfuse integration for tracing

## Sources
- [Anthropic: Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [LangChain: State of Agent Engineering](https://www.langchain.com/state-of-agent-engineering)
- [CLEAR Framework (arxiv)](https://arxiv.org/html/2511.14136v1)
- [UK AISI 2025 Review](https://www.aisi.gov.uk/blog/our-2025-year-in-review)
- [Maxim AI: Top 5 Eval Tools 2026](https://www.getmaxim.ai/articles/top-5-tools-for-agent-evaluation-in-2026/)
