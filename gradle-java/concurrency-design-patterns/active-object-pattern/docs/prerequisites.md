# Prerequisites

## Required

This is the capstone. It assumes, and does not re-teach:

- **Producer–Consumer (§46):** the queue, and the harness.
- **Thread Pool (§47):** a worker thread that takes tasks.
- **Future/Promise (§48):** `CompletableFuture` and a result that arrives later.
- **Monitor Object (§50):** state owned by one party, and a lock that is private.

## Explicitly not required

No actor framework, and no knowledge of event loops. Both are named at the
end and neither is taught.

## What you will need

Java 21. `./gradlew run` works offline.
