# RAG Evaluation Report

## Summary

- Total cases: 4
- Passed cases: 4
- Retrieval accuracy: 100%
- Citation coverage: 100%
- Groundedness rate: 100%
- Overall pass rate: 100%
- Average latency: 0.0 ms

## Case Results

| Case | Retrieval | Citations | Grounded | Latency | Expected source | Retrieved sources |
| --- | --- | --- | --- | ---: | --- | --- |
| rag-retrieval | PASS | PASS | PASS | 0.1 ms | rag-architecture.txt | rag-architecture.txt, evaluation-quality.txt |
| agent-boundary | PASS | PASS | PASS | 0.0 ms | agent-design.txt | agent-design.txt, rag-architecture.txt, deployment-ops.txt |
| deployment-readiness | PASS | PASS | PASS | 0.0 ms | deployment-ops.txt | deployment-ops.txt, agent-design.txt, rag-architecture.txt |
| evaluation-metrics | PASS | PASS | PASS | 0.0 ms | evaluation-quality.txt | evaluation-quality.txt, rag-architecture.txt, agent-design.txt |
