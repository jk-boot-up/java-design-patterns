# Session Guide — Micro-Frontends Pattern

## Learning Objectives

By the end of the session you can:

- Explain what problem micro-frontends solve for teams.
- Assemble a page from fragments with fallbacks.
- Show an independent release.
- Name the costs: requests, consistency, operations.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: One front-end for everything | 7 min |
| 0:17 | Act 2: Each team serves its part | 7 min |
| 0:24 | Act 3: Failure stays in its slot | 7 min |
| 0:31 | Act 4: Independent releases | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act one. Open `PageAssembler.render`: fetch every
slot at once, fall back on failure. Then `TeamApp`: a tiny server each team
owns. End on act five and ask what a shared design system would contain.

## Exercises

1. Add a fourth slot, reviews, owned by a new team.
2. Cache each fragment for 10 seconds. What happens when a team releases?
3. Give the assembler a shared `formatPrice` rule that every team must use. Where should it live?
