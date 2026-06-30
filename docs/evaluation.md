# Evaluation

This project includes a small retrieval evaluation layer.

## Purpose

RAG systems should not only generate answers. They should be checked for whether they retrieve the right supporting context.

The first evaluation version checks:

- User question
- Expected source document
- Sources retrieved by the pipeline
- Pass/fail result
- Overall pass rate

## Next Improvements

- Add a small benchmark dataset.
- Track retrieval precision and recall.
- Add answer quality evaluation.
- Add regression tests for known documents.
- Store evaluation results as CI artifacts.

