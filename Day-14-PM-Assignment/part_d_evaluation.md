# Day 14 PM Part D — AI-Augmented Task

## Prompt used
"Give me 3 SQL interview questions at senior data engineer level involving window functions or CTEs. Include the expected answer and a common mistake candidates make."

## Queries run on database
- All 3 questions were run against the Day 14 PM schema (SQLite). Syntax was adapted where needed (e.g. date functions).
- Each query was verified to execute and return the expected shape/result.

## Evaluation
- **Common mistakes:** The AI listed mistakes such as "using RANK instead of DENSE_RANK when you need no gaps" and "forgetting PARTITION BY in a window, so the window is over the whole table." These are accurate and useful.
- **Did I make any myself?** When implementing Part A, the 2nd-highest salary correlated subquery was initially written with `>= 2` instead of `= 2` (to get "second" as the rank). Correcting to "exactly 2 salaries >= this one" fixed it. So the "common mistake" of mixing up rank semantics applied.
- **Accuracy:** One expected answer assumed a different schema; it was adjusted to our tables and re-run. Overall the senior-level focus on window functions and CTEs was appropriate.
