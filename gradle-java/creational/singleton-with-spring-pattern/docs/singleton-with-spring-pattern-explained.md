# Singleton with Spring, Explained

## The pattern in one sentence

In Spring, a singleton is a scope: one instance per container, which the container hands out.

## What is new here

The pattern is [Singleton](../singleton-pattern). This page is only what Spring Boot adds.

### One Bean, Shared

Three callers get the same generator, and the numbers run one, two, three across them.

```
  checkout, admin and retry hold the same generator: true
  ORD-000001
  ORD-000002
  ORD-000003  (three callers, one counter)
```

### Nothing Stops new

The constructor is public, so a plain `new` makes a second generator that starts at one again.

```
  managed says ORD-000001, a plain new says ORD-000001
  same object: false. the constructor is public, so the compiler cannot help.
```

### One Per Container

Start the application twice in one program and each container has its own bean. Both issue order one.

```
  context A issues ORD-000001, context B issues ORD-000001
  the same order number went to two customers: true
```

### A Scope Change

Change the scope of the bean definition to prototype, and every caller gets its own generator.

```
  with scope prototype: checkout issues ORD-000001, admin issues ORD-000001
  one word changed, and the two callers no longer share a counter.
```

### When Is It Built?

By default the bean is built at startup. With lazy initialization it is built on first use.

```
  eager: built 1 before any caller asked.
  lazy: built 0 after startup.
  lazy: built 1 after the first caller.
```

### Shared Means Shared By Threads

A bean is shared by every thread, and Spring does not protect its fields. A plain long held between read and write hands two customers the same number. An `AtomicLong` gives ten thousand distinct numbers.

```
  a plain long, held between read and write: ORD-000001 and ORD-000001
  duplicate order number: true
  an AtomicLong, 4 threads x 2500: 10000 distinct numbers, none repeated.
  Spring shares the bean. Keeping its state safe is still your job.
```

## The verdict

Let the container own the single instance, keep the state inside it thread-safe, and be sure only one container runs. Reach for the enum when the guarantee must hold without a container.

## How to recognise this in code you did not write

- A class with no private constructor and no `getInstance()`, injected by constructor.
- `@Component`, `@Service` or `@Bean` with no scope named, since the default is singleton.
- A class whose fields are mutated by request-handling code.

## Where you have already met this

Every `@Service` and `@Repository` you have written. The default scope is singleton, so most of them already are.

## When this is too much

For a class with no state, the singleton question hardly matters. It bites when the bean holds a counter, a cache or a connection.
