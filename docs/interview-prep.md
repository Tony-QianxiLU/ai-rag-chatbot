# Interview Preparation

## Recruiter-Friendly Explanation

AI RAG Chatbot is a deployed GenAI application that answers questions from uploaded documents and shows citations. It demonstrates the full applied AI loop: document ingestion, chunking, retrieval, answer generation, evaluation, testing, CI, deployment, and documentation.

In simple terms: instead of asking an LLM to answer from memory, the app first retrieves relevant document chunks and then answers using that context. This makes the answer more inspectable and reduces hallucination risk.

## Technical Questions

| Question | Strong answer points |
| --- | --- |
| What is RAG? | Retrieval-augmented generation combines search over external knowledge with language generation. The retriever finds relevant context, and the generator uses that context to answer. |
| Why chunk documents? | LLMs and retrievers work better on focused passages. Chunking balances context size, retrieval precision, and citation quality. |
| Why include citations? | Citations let users inspect sources, debug retrieval, and build trust in generated answers. |
| Why support local deterministic fallbacks? | They make demos, tests, and CI reliable without depending on paid API calls or external model availability. |
| What does the evaluation suite measure? | Retrieval accuracy, citation coverage, grounded answer terms, overall pass rate, and latency. |
| How would you improve retrieval quality? | Add harder eval cases, precision/recall@k, hybrid retrieval, reranking, metadata filters, and query rewriting. |

## Architecture Questions

| Question | Strong answer points |
| --- | --- |
| Why separate loader, chunker, retriever, generator, and evaluator? | Separation makes each component testable, replaceable, and easier to explain. |
| What happens when an API key is missing? | The app still runs with local deterministic behavior and template generation. |
| What is the tradeoff between keyword and vector retrieval? | Keyword retrieval is simple and deterministic; vector retrieval can capture semantic similarity but requires embedding quality and evaluation. |
| Where would you add observability? | Track query, retrieved chunks, scores, latency, answer metadata, user feedback, and evaluation results over time. |

## System Design Questions

| Question | Strong answer points |
| --- | --- |
| How would you make this enterprise-ready? | Add auth, tenant-aware document storage, access control, hybrid retrieval, reranking, eval dashboards, logging, monitoring, and deployment automation. |
| How would you handle private documents? | Store documents securely, enforce per-user permissions, avoid logging sensitive content, and isolate vector indexes by tenant or access policy. |
| How would you detect regressions? | Run the offline evaluation suite on every PR and track metrics such as retrieval accuracy, citation coverage, groundedness, and latency. |
| How would you scale ingestion? | Use background jobs, durable storage, batch embedding, retry handling, and incremental indexing. |

## STAR Stories

### Building a Working RAG System

- Situation: I needed a portfolio project that proved I could build more than a chatbot UI.
- Task: Build a document QA app with retrieval, citations, tests, deployment, and documentation.
- Action: I separated ingestion, chunking, retrieval, generation, and evaluation into modules, added deterministic fallbacks, and deployed it on Streamlit.
- Result: The project now has a live demo, 27 passing tests, CI, v0.3.0 evaluation reports, screenshots, GIF, and walkthrough video.

### Adding Evaluation

- Situation: A demo alone does not prove an AI system is reliable.
- Task: Add an offline evaluation suite that can run without API keys.
- Action: I created a curated JSONL benchmark and measured retrieval accuracy, citation coverage, groundedness, and latency.
- Result: The benchmark passes 4/4 cases and runs in CI, making regressions visible after code or prompt changes.

## Common Follow-Up Questions

- What would happen if the document is irrelevant to the question?
- How would you prevent hallucinated citations?
- How would you evaluate top-k retrieval quality?
- How would you choose chunk size and overlap?
- How would you handle multi-document conflicts?
- What changes would you make for production deployment?
