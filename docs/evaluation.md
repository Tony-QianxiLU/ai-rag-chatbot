# Evaluation

This project includes an offline RAG evaluation suite that runs without paid API calls.

The goal is to make the project interview-ready by showing not only that the app works, but also that retrieval and answer behavior can be measured after code, prompt, or model changes.

## What It Measures

| Metric | Meaning |
| --- | --- |
| Retrieval accuracy | Whether the expected source document appears in retrieved citations. |
| Citation coverage | Whether the answer includes at least the expected number of citations. |
| Groundedness rate | Whether the generated answer includes expected terms from the retrieved context. |
| Overall pass rate | Whether a case passes retrieval, citation, and groundedness checks together. |
| Average latency | How long each benchmark question takes to run locally. |

## Benchmark Dataset

The benchmark lives in:

```text
data/evaluation_cases.jsonl
```

Each JSONL row includes:

- `id`
- `question`
- `expected_source`
- `expected_answer_terms`
- `expected_citation_count`

The current dataset covers:

- RAG architecture
- AI agent transparency
- Deployment readiness
- RAG evaluation metrics

## Run Evaluation

```bash
PYTHONPATH=src uv run rag-evaluate
```

Generated reports:

```text
reports/evaluation-report.md
reports/evaluation-report.json
```

## Current Result

| Metric | Result |
| --- | ---: |
| Retrieval accuracy | 100% |
| Citation coverage | 100% |
| Groundedness rate | 100% |
| Overall pass rate | 100% |

See [reports/evaluation-report.md](../reports/evaluation-report.md) for case-level details.

## CI Integration

GitHub Actions runs the evaluation suite after linting and tests:

```bash
PYTHONPATH=src uv run rag-evaluate
```

This means changes to chunking, retrieval, generation, or evaluation logic are checked automatically on push and pull request.

## Future Improvements

- Add harder negative cases where the correct answer should say context is insufficient.
- Add retrieval precision and recall at top-k.
- Track latency trends over time.
- Add optional LLM-as-judge evaluation for answer helpfulness.
- Store generated reports as CI artifacts.
