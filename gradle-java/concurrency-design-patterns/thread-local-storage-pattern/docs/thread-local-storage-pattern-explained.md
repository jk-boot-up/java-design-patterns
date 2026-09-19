# Thread-Local Storage, Explained

## The pattern in one sentence

Thread-local storage gives each thread its own private copy of a variable, so code anywhere on that thread can read it without it being passed down, and other threads never see it.

## The six acts

### Hand It Down

Three methods each take a customer they never use, so that the last can log it. Every new layer and every new caller has to pass it on.

```
  three methods each take a customer parameter that they never use, so that the last can log it: [ada: reserved stock].
  every new layer, and every new caller, has to pass it on.
```

### A Value That Belongs To The Thread

The customer is set once at the door, and checkout, price and stock take no customer, yet the log says ada. After the request the context is cleared.

```
  the customer is set once, at the door. checkout, price and stock take no customer: [ada: reserved stock].
  after the request the context is cleared: null.
```

### Each Thread Has Its Own

Two customers are handled at the same moment, both contexts set before either is read. Each log line names its own customer. They share the code and the static field, and not the value.

```
  two customers at the same moment, both contexts set before either reads: [ada: reserved stock, ben: reserved stock].
  neither saw the other's, though both used the same code and the same static field.
```

### A Thread That Is Reused

Request A sets ada and forgets to clear it. Request B, an anonymous visitor, runs next on the same pool thread, and is logged as ada. With the clear in a finally block, B is logged as nobody.

```
  request A sets its customer and forgets to clear it. request B, an anonymous visitor, runs next on the same pool thread: [ada: reserved stock, ada: reserved stock].
  request B was logged as ada. a pool reuses its threads, so what a request leaves behind, the next one finds.
  with the clear in a finally block: [ada: reserved stock, null: reserved stock].
```

### A New Thread Starts Empty

Ada's request hands the work to another thread, and the log says null. A thread created by ada's thread can inherit a copy, but a pool thread is created once and reused, so it does not have the current request's. Handing work on means handing the context on.

```
  ada's request hands the work to another thread: [null: reserved stock].
  a thread created by ada's thread inherits a copy: ada. but a pool thread is created once and reused, so it holds whatever was there when it was created, not the current request's.
  handing work on means handing the context on, on purpose.
```

### The Bill

A method that reads the context has a dependency its signature does not show, and with none set it logs null. Every test has to set and clear the context. And a pool thread keeps what is left in it for as long as it lives.

```
  a method that reads the context has a dependency its signature does not show. called with none set: [null: reserved stock].
  every test of the code below the door has to remember to set the context first, and to clear it after.
  and a long-lived pool thread keeps whatever is left in it for as long as the thread lives.
```

## The verdict

Use thread-local storage for context that is truly per-request and crosses many layers, such as a trace id, a security principal or a transaction. Set it in one place, clear it in a finally block in the same place, pass it on by hand when you hand work to another thread, and keep the values small. If a parameter is easy, pass the parameter.

## How to recognise this in code you did not write

- A `private static final ThreadLocal<...>` field.
- `SecurityContextHolder`, `TransactionSynchronizationManager`, `MDC` from logging.
- `try { set(...); ... } finally { remove(); }`.
- A `TaskDecorator` or `ContextSnapshot` that copies context to another thread.

## Where you have already met this

Spring's security and transaction context, logging MDC, and every framework that seems to know who you are without being told.

## When this is too much

If a value is used in one or two places, pass it as a parameter, where it can be seen and tested. Thread-local state is global state with a thread's name on it.
