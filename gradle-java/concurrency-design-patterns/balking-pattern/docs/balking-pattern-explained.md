# Balking, Explained

## The pattern in one sentence

Balking means an action is only carried out if the object is in the right state, and if it is not, the call returns at once instead of waiting or failing.

## The six acts

### Save Every Time

One edit, and the autosave timer fires five times: five writes. Four of them wrote exactly what was already there.

```
  one edit, and the autosave timer fires 5 times: 5 writes.
  four of them wrote exactly what was already there.
```

### Balk When There Is Nothing To Save

The same five calls give saved once and nothing to save four times. One write.

```
  the same five calls: SAVED, NOTHING_TO_SAVE, NOTHING_TO_SAVE, NOTHING_TO_SAVE, NOTHING_TO_SAVE.
  writes: 1.
```

### Balk When A Save Is Already Running

A save is in progress, held in the write. A second call arrives and is told already saving, at once, without waiting. Only one write happens.

```
  a save is in progress. a second call arrives: ALREADY_SAVING, straight away, without waiting.
  the first save finishes. writes: 1. the second caller did not queue behind it.
```

### An Edit During A Save

The customer changes two to three while a save runs. A draft that marks itself clean when the save ends loses the change. One with a version counter stays dirty, and the next save writes three.

```
  the customer changes 2 to 3 while the save runs. a draft that marks itself clean when the save ends: dirty false, next save says NOTHING_TO_SAVE. saved: [2 x MUG-BLUE].
  with a version counter: dirty true, next save says SAVED. saved: [2 x MUG-BLUE, 3 x MUG-BLUE].
```

### The Caller Is Told

Nothing edited gives nothing to save. Edited gives saved. A balk is an answer, not an error, so the caller can retry, ignore it, or tell the user.

```
  nothing edited: NOTHING_TO_SAVE.
  edited: SAVED.
  a balk is an answer, not an error. the caller can retry, ignore it, or tell the user, and the enum says which happened.
```

### The Bill

The customer clicks Save while the autosave runs, and is told already saving. Their click did nothing, and their change waits for the next save. Balking is wrong where every request must be honoured.

```
  the customer clicks Save while the autosave is running: ALREADY_SAVING. their click did nothing.
  the draft is still dirty: true. saved so far: [2 x MUG-BLUE]. the change waits for the next save.
  balking suits work that can be skipped and done later. it is wrong where every request must be honoured, because a balked request is simply not done.
```

## The verdict

Use balking for work that is idempotent or repeatable, where skipping a call is harmless because a later call will catch up: autosave, refresh, a periodic sync. Return a result that says what happened. Track what was saved with a version, not a flag. Do not use it where every request must be carried out: wait instead, or queue.

## How to recognise this in code you did not write

- An early `return` at the top of a method that checks a state flag.
- `isSaving`, `isRunning` or `alreadyStarted` fields.
- `AtomicBoolean.compareAndSet(false, true)` guarding a task.
- `ScheduledExecutorService` tasks that skip a run if the last is still going.

## Where you have already met this

Autosave in every editor, refresh buttons that ignore a second click, and `Lock.tryLock()` with no waiting.

## When this is too much

Where the caller needs the action done, balking silently drops it. Where the state is checked and changed in separate steps without a lock, balking is a race in disguise.
