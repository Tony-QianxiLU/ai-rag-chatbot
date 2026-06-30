from __future__ import annotations

import argparse
from pathlib import Path

from ai_rag_chatbot.document_loader import LoadedDocument
from ai_rag_chatbot.evaluation import (
    evaluate_rag,
    load_evaluation_cases,
    write_json_report,
    write_markdown_report,
)


BENCHMARK_DOCUMENTS = [
    LoadedDocument(
        filename="rag-architecture.txt",
        text=(
            "Retrieval augmented generation combines search with language generation. "
            "The system chunks source documents, retrieves relevant context for a question, "
            "and uses that context to ground the answer with citations."
        ),
    ),
    LoadedDocument(
        filename="agent-design.txt",
        text=(
            "AI agents use planning, tools, and execution traces to complete structured tasks. "
            "A transparent agent should show its plan, tool calls, tool results, and memory."
        ),
    ),
    LoadedDocument(
        filename="deployment-ops.txt",
        text=(
            "Production AI applications need deployment documentation, environment variables, "
            "CI checks, release notes, and rollback-friendly workflows."
        ),
    ),
    LoadedDocument(
        filename="evaluation-quality.txt",
        text=(
            "RAG evaluation tracks retrieval accuracy, citation coverage, groundedness, and "
            "latency. These metrics help teams detect regressions when prompts or models change."
        ),
    ),
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the RAG evaluation benchmark.")
    parser.add_argument(
        "--cases",
        type=Path,
        default=Path("data/evaluation_cases.jsonl"),
        help="Path to JSONL evaluation cases.",
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        default=Path("reports/evaluation-report.json"),
        help="Path for the JSON evaluation report.",
    )
    parser.add_argument(
        "--markdown-output",
        type=Path,
        default=Path("reports/evaluation-report.md"),
        help="Path for the Markdown evaluation report.",
    )
    args = parser.parse_args()

    cases = load_evaluation_cases(args.cases)
    report = evaluate_rag(BENCHMARK_DOCUMENTS, cases)
    write_json_report(report, args.json_output)
    write_markdown_report(report, args.markdown_output)

    summary = report.summary
    print(
        "Evaluation complete: "
        f"{summary.passed_cases}/{summary.total_cases} cases passed, "
        f"retrieval={summary.retrieval_accuracy:.0%}, "
        f"citations={summary.citation_coverage:.0%}, "
        f"groundedness={summary.groundedness_rate:.0%}, "
        f"latency={summary.average_latency_ms:.1f}ms"
    )


if __name__ == "__main__":
    main()
