# Day 15 PM Part B — BCNF (Boyce-Codd Normal Form)

## Schema in 3NF but not BCNF

**Example:** Suppose we have **R(Student, Course, Instructor)** with FDs:
- Student, Course → Instructor
- Instructor → Course

So each instructor teaches exactly one course; a student can take a course from one instructor. Candidate key: (Student, Course). R is in 3NF (every non-prime attribute depends on a key). But **Instructor → Course** is a non-trivial FD whose left side (Instructor) is not a superkey** → BCNF violation.

**Decomposition to BCNF:** Resolve the FD Instructor → Course by splitting:
- **R1(Instructor, Course)** — key Instructor.
- **R2(Student, Instructor)** — key (Student, Instructor); we can recover (Student, Course) by joining R2 with R1.

So the schema becomes R1 and R2; both are in BCNF. The original relation is recoverable by R2 ⋈ R1.

## When to leave in 3NF instead of BCNF

- **When decomposition loses FDs:** Decomposing to BCNF can make it impossible to enforce some functional dependencies without joins. If the lost FD is important for integrity, we may keep 3NF and enforce the FD in application or triggers.
- **When join cost dominates:** Extra tables mean more joins for common queries; if performance is critical and updates are rare, 3NF might be preferred.
- **When the BCNF violation is “benign”:** If the non-key FD (e.g. Instructor → Course) is rarely updated and consistency can be checked periodically, staying in 3NF is sometimes acceptable.
