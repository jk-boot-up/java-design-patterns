# Problem Statement

## The scenario

A customer's basket draft is saved by a timer every few seconds, and by a Save button. Sometimes nothing has changed, and sometimes a save is already running.

## The naive version

Every call to save writes, changed or not, busy or not.

```
  one edit, and the autosave timer fires 5 times: 5 writes.
  four of them wrote exactly what was already there.
```

## What this project must deliver

Three drafts: one that always writes, one that balks when clean or busy but has a bug, and one with a version counter that is correct; a storage that holds a write at a gate so a save is in progress exactly when the demo says; a save result that tells the caller what happened; an edit during a save that is lost or kept; and a plain verdict.
