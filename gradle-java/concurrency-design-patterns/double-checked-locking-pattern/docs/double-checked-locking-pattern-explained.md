# Double-Checked Locking, Explained

## The pattern in one sentence

Double-checked locking creates a shared object lazily, checking for it first without a lock, and only taking the lock, and checking again, when it looks missing.

## The six acts

### Check, Then Create

Two threads ask together, and both see that the price list does not exist, so both build one. Two are built, and each thread holds a different one.

```
  two threads ask for the shared price list at the same moment, before it exists.
  price lists built: 2. both saw that it was missing, and both built one.
  each thread now holds a different price list, and one of them is thrown away.
```

### Lock Every Time

With the lock on every call, only one is built. But a thousand calls, long after it was built, take the lock a thousand times.

```
  the same two threads, with the lock on every call: built 1.
  1000 more calls, long after it was built, took the lock 1000 times.
```

### Check, Lock, Check Again

The same race builds one. The second thread waited for the lock, looked again, and found it built. A thousand calls take the lock once.

```
  the same race: built 1. the second thread waited for the lock, looked again, and found it built.
  1000 calls: the lock was taken 1 time. after that, no call waits for anyone.
```

### Why It Must Be Volatile

The field is volatile. Without it, the memory model lets one thread see the reference before it sees the object fully built. That failure cannot be produced on demand, so a test guards the rule.

```
  the field is declared volatile: true.
  without it, the Java memory model lets one thread see the reference before it sees the object built.
  that failure cannot be produced on demand. it depends on the processor and the compiler. so the rule is guarded by a test, not by a demonstration.
```

### The Simplest Correct Way

Nothing is built before anyone asks. After two calls, one is built, and both calls get it. The JVM builds a class's static state once, when it is first used, so there is no lock and no volatile to write.

```
  price lists built before anyone asks: 0.
  after two calls: 1 built, the same one both times: true.
  the JVM builds a class's static state once, when it is first used. there is no lock and no volatile to write, or to get wrong.
```

### The Bill

The double-checked version is twenty nine lines and the holder ten. Double-checked locking is ceremony with one way to be subtly wrong. It earns its place only where the holder cannot be used, for example when creation needs an argument. An uncontended lock is cheap.

```
  lines of code in the accessor's class: double-checked 29, holder 10.
  double-checked locking is ceremony with one way to be subtly wrong. it earns its place only where the holder idiom cannot be used, for example when creation needs an argument.
  and an uncontended lock is cheap. measure before deciding the lock on every call is a problem.
```

## The verdict

Prefer the class holder idiom, or an enum, for a lazy shared object. If creation needs an argument or can fail and be retried, use double-checked locking, with a volatile field, a local variable, and a test that guards the volatile. If you have not measured the lock as a problem, take the lock on every call.

## How to recognise this in code you did not write

- A `volatile` static field, an `if (x == null)`, a `synchronized` block, and another `if (x == null)`.
- A private static nested `Holder` class with one field.
- `Lazy<T>` and `Suppliers.memoize` in libraries.
- A comment that says why the field is volatile.

## Where you have already met this

Effective Java's Item 83, and the lazy initialisation inside many JDK and framework classes.

## When this is too much

Nearly always. Most lazy initialisation can use a holder, an eager static, or a lock on every call, and the cost of a wrong double check is a bug you cannot reproduce.
