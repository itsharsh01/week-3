Assignment workflow context (for agent)
Use this when the user says things like “do Day X AM/PM assignment” or “do the assignment.”
1. Repo layout
One folder per assignment, at repo root:
Day-XX-AM-Assignment/ — morning assignment for that day
Day-XX-PM-Assignment/ — afternoon assignment
Day-XX-Bonus-Assignment/ — optional/bonus when present
All files for that assignment live inside its folder (scripts, docs, data, PDF/DOCX, requirements.txt, etc.). Do not create assignment files at repo root.
Summaries are separate from assignments:
Folder: assignment-summary/ at repo root (sibling to Day-XX-...).
This folder must be in .gitignore so it is not published.
2. How to handle each assignment
Understand the brief
Read the assignment (PDF/DOCX). If the tool can’t read PDF/DOCX directly, use another method (e.g. copy PDF to a simple filename, extract text from DOCX via word/document.xml or a small script) and work from the extracted text.
Implement step by step
Do each part (Part A, B, C, D, etc.) as written.
Save every created or modified file in that assignment’s folder (e.g. Day-08-AM-Assignment/).
Commit after each logical step
Commit at natural breakpoints (e.g. after Part A, then Part B, etc.), not only at the end.
Use clear messages, e.g. Day 08 AM Part A: admission_decision.py, Day 08 AM Part B: tax_calculator.py.
Write a summary when the assignment is done
One markdown file per assignment in assignment-summary/.
Naming: Day-XX_YY.md
XX = day number (e.g. 07, 08, 11).
YY = AM, PM, or Bonus.
Examples: Day-07_PM.md, Day-07_AM.md, Day-07_Bonus.md, Day-08_AM.md, Day-11_PM.md.
3. Summary file format
Each assignment-summary/Day-XX_YY.md should:
State what the assignment says
Day/session, topics, submission note, and a short list of parts (Part A, B, C, D, etc.) with their main ask.
List “Steps (what the assignment asks for)”
Bullet points or subheadings for each part with the concrete tasks (inputs, outputs, file names, validations, etc.).
Describe “What was done”
For each part: Files: exact filenames; Done: short description of what was implemented and how it meets the brief.
End with a line like:
“Assignment files are under Day-XX-YY-Assignment/.”
“This summary is in assignment-summary/Day-XX_YY.md; the assignment-summary/ folder is in .gitignore and is not tracked or published.”
4. Conventions
.gitignore
Include assignment-summary/.
Optionally add any temp/extraction paths (e.g. extracted_text.txt, docx_extract/) if used for parsing PDF/DOCX.
No publishing of summaries
assignment-summary/ is for local use only; keep it ignored by Git.
User prompts
“Do Day X AM/PM/Bonus assignment” means: analyze the assignment doc → implement all parts → put files in the right folder → commit per logical step → add assignment-summary/Day-XX_YY.md when done.
Ambiguities
If something is unclear (e.g. GPA scale, exact formula), pick a reasonable interpretation, implement it, and mention it briefly in the summary under “What was done.”
5. Technical notes from this repo
Python: scripts are Python; use pathlib, type hints and docstrings where appropriate; follow PEP 8 (e.g. snake_case).
PDF/DOCX: if direct read fails, use workarounds (simplified PDF filename, DOCX as ZIP + word/document.xml or extract to .txt) and read the extracted text.
Shell: on Windows PowerShell avoid &&; use ; or separate commands.
Tests: if the assignment asks for tests but pytest isn’t installed, running a small python -c "assert ..." or a minimal script is acceptable; note it in the summary if relevant.
6. Example one-line brief for the agent
You can paste this (and adjust the week name) when creating the new repo:
“Same as week-2: one folder per assignment (Day-XX-AM-Assignment, Day-XX-PM-Assignment, etc.), all files inside that folder, commit after each part, summaries in assignment-summary/ as Day-XX_YY.md, and assignment-summary/ in .gitignore. When I say ‘do Day X AM/PM’, analyze the assignment, implement everything, then write the summary.”
