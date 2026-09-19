# Problem Statement

## The scenario

A checkout request goes through checkout, pricing and stock, and the audit log at the bottom must say which customer did it.

## The naive version

Pass the customer down as a parameter through every method, so the last one can log it.

```
  three methods each take a customer parameter that they never use, so that the last can log it: [ada: reserved stock].
  every new layer, and every new caller, has to pass it on.
```

## What this project must deliver

A request context in a thread-local field with a set, a read, a clear, and a helper that always clears; an audit log that reads it; the parameter-passing version; two simultaneous threads that do not see each other; a single-thread pool that leaks one request's customer into the next unless cleared; a pool thread that does not see the submitter's context; an inheritable variant; and a plain verdict.
