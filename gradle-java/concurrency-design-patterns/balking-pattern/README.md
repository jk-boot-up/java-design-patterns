# Balking Pattern

```
src/main/java/com/jk/explore/balkingpattern/
├── BalkingDemo.java                 the six acts
├── BalkingDraft.java                balks when clean or busy; a version counter makes it correct
├── CarelessBalkingDraft.java        balks, and loses an edit made during a save
├── AlwaysSavingDraft.java           writes every time
├── Storage.java  Gate.java  SaveResult.java
```

**Balking: if the object is not in the right state, return at once instead of waiting.**

This project is in [concurrency-design-patterns](..). It is the impatient partner of [Guarded Suspension](../guarded-suspension-pattern), which waits until the state is right, and a cousin of [Thread Pool](../thread-pool-pattern)'s refusal of work it cannot take.

## Run

```bash
./gradlew run
```

Six acts. Every number quoted below comes from this program's own output.

```
ONE. Save every time it is asked.
  one edit, and the autosave timer fires 5 times: 5 writes.
  four of them wrote exactly what was already there.
TWO. Balk when there is nothing to save.
  the same five calls: SAVED, NOTHING_TO_SAVE, NOTHING_TO_SAVE, NOTHING_TO_SAVE, NOTHING_TO_SAVE.
  writes: 1.
THREE. Balk when a save is already running.
  a save is in progress. a second call arrives: ALREADY_SAVING, straight away, without waiting.
  the first save finishes. writes: 1. the second caller did not queue behind it.
FOUR. An edit during a save.
  the customer changes 2 to 3 while the save runs. a draft that marks itself clean when the save ends: dirty false, next save says NOTHING_TO_SAVE. saved: [2 x MUG-BLUE].
  with a version counter: dirty true, next save says SAVED. saved: [2 x MUG-BLUE, 3 x MUG-BLUE].
FIVE. The caller is told.
  nothing edited: NOTHING_TO_SAVE.
  edited: SAVED.
  a balk is an answer, not an error. the caller can retry, ignore it, or tell the user, and the enum says which happened.
SIX. The bill.
  the customer clicks Save while the autosave is running: ALREADY_SAVING. their click did nothing.
  the draft is still dirty: true. saved so far: [2 x MUG-BLUE]. the change waits for the next save.
  balking suits work that can be skipped and done later. it is wrong where every request must be honoured, because a balked request is simply not done.
```

## Test

```bash
./gradlew test
```

2 test classes, 8 test methods, offline, with nothing installed and no framework.

## Technologies and versions

| What | Version | Why it is here |
| --- | --- | --- |
| Java | 21 | The repository standard, via the Gradle toolchain block |
| Gradle | 9.2.1 | The wrapper in this directory; no separate install needed |
| JUnit 5 | 5.10.2 | Test runner |

No framework. A hand-built project stays plain Java so the mechanism is the whole lesson.

## Learning Material

| Document | What it covers |
| --- | --- |
| [`docs/problem-statement.md`](docs/problem-statement.md) | The scenario, and the problem |
| [`docs/balking-pattern-explained.md`](docs/balking-pattern-explained.md) | The pattern, and six acts |
| [`docs/class-diagram.md`](docs/class-diagram.md) | The types |
| [`docs/architecture-diagram.md`](docs/architecture-diagram.md) | The parts and how they connect |
| [`docs/data-flow-diagram.md`](docs/data-flow-diagram.md) | What happens to one request |
| [`docs/sequence-diagram.md`](docs/sequence-diagram.md) | Written for a listener with the screen off |
| [`docs/uml-diagram.md`](docs/uml-diagram.md) | Four sequences |
| [`docs/animation.html`](docs/animation.html) | The six acts in a browser |
| [`docs/prerequisites.md`](docs/prerequisites.md) | What you need to know |
| [`docs/session.md`](docs/session.md) | A one-hour taught session |
| [`docs/spec.md`](docs/spec.md) | The generated specification |
| [`docs/youtube.md`](docs/youtube.md) | Title, description and chapters |

### The pattern in one picture

![Class diagram](docs/images/class-diagram.png)

### Where each piece sits

![Architecture diagram](docs/images/architecture-diagram.png)

### How one request moves

![Data flow diagram](docs/images/data-flow-diagram.png)

### Who calls whom, in order

![Sequence diagram](docs/images/sequence-diagram.png)

### All four sequences

![Sequence one](docs/images/uml-diagram.png)

![Sequence two](docs/images/uml-diagram-2.png)

![Sequence three](docs/images/uml-diagram-3.png)

![Sequence four](docs/images/uml-diagram-4.png)

### Video

Built from [`video/scenes.py`](video/scenes.py) by
[`video/build_video.sh`](video/build_video.sh). The rendered file is not
committed; see the repository README for why.

## Where you have already met this

Autosave in every editor, refresh buttons that ignore a second click, and `Lock.tryLock()` with no waiting.

## When this is too much

Where the caller needs the action done, balking silently drops it. Where the state is checked and changed in separate steps without a lock, balking is a race in disguise.

## Where this sits

This project is in [`concurrency-design-patterns`](..), and is meant to be read with its neighbours there.
