# Session Guide — Message Translator / Normalizer Pattern

## Learning Objectives

By the end of the session you can:

- Explain a canonical data model.
- Write a translator for one format.
- Build a normalizer that picks translators.
- Name what translation can lose.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: The warehouse reads every format | 7 min |
| 0:17 | Act 2: Translators | 7 min |
| 0:24 | Act 3: The normalizer | 7 min |
| 0:31 | Act 4: A new marketplace | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act one. Open `Translators`: four small
functions. Then `Normalizer.standard`: three rules. End on act five and ask
what should happen to the gift note.

## Exercises

1. Add a `note` field to OrderMessage and carry the gift note through.
2. Make the normalizer send unrecognised messages to a dead-letter list instead of throwing.
3. Replace the JSON regex with a real JSON library. What breaks less?
