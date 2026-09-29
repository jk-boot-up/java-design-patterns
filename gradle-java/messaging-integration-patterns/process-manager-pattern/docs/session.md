# Session Guide — Process Manager Pattern

## Learning Objectives

By the end of the session you can:

- Explain why a chain of services loses track of failures.
- Keep per-instance state and decide the next step from replies.
- Put unhappy paths inside the process.
- Weigh a central process manager against choreography.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Steps chained together | 7 min |
| 0:17 | Act 2: A process manager | 7 min |
| 0:24 | Act 3: A branch | 7 min |
| 0:31 | Act 4: The unhappy path | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act one's stock count. Open
`ProcessManager.step`: every reply comes back here, and a `switch` decides
what happens next. End on act five and ask what must be stored so a restart
does not lose orders.

## Exercises

1. Store the manager's state in a map that is saved to a file, and restart it mid-order.
2. Add a step: send a delivery-slot email after shipping.
3. If the partner warehouse is used, charge an extra £5 delivery. Where does that rule go?
