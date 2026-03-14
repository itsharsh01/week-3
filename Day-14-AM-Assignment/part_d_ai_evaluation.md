# Day 14 AM Part D — AI-Augmented Task

## Prompt used
"Generate 5 medium-difficulty SQL interview questions for a data engineer role, with answers. Include one about JOINs, one about NULL handling, and one about performance."

## Queries run on database
- The 5 questions were generated (JOINs, NULL handling, performance, plus 2 other medium topics). Each was run against `day14_am.db` (SQLite) after adapting syntax where needed (e.g. COALESCE, LEFT JOIN, indexing concepts).
- All 5 were verified to execute; one was adjusted for SQLite (e.g. date function) to produce correct output.

## Evaluation
- **Difficulty:** The set was medium: JOINs and NULL handling (COALESCE/IS NULL) are standard; the performance question (indexes, EXPLAIN) is appropriate for data engineering.
- **Completeness:** Answers were complete for syntax and logic. The performance answer was generalized (index on WHERE/JOIN columns, avoid SELECT *) and fits our schema.
- **Improvement:** One question was refined to use our actual table names (employees, departments) so the query runs as-is and is easier to verify.
