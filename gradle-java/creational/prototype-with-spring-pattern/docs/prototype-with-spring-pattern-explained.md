# Prototype with Spring, Explained

## The pattern in one sentence

In Spring, a prototype is a scope: every request builds a new bean from its definition.

## What is new here

The pattern is [Prototype](../prototype-pattern). This page is only what Spring Boot adds.

### A New One Each Time

Two requests to the container give two different listings, both built from the definition.

```
  same object: false. both are titled 'Untitled'.
```

### Independent

Edit one listing and the other is untouched.

```
  a: 'Blue Mug' with 2 images.
  b: 'Untitled' with 1 image.
```

### A Definition, Not A Draft

Ask the container for another listing and you get a fresh one, not your edited draft. Only the class's own `copy()` carries the edits.

```
  asked the container again: 'Untitled' with 1 image.
  asked the draft to copy(): 'Blue Mug' with 2 images.
```

### A Prototype Inside A Singleton

Injected into a singleton's constructor, the prototype is built once, so every call gets the same listing.

```
  two calls, same object: true.
  the second caller sees the first caller's title: 'Blue Mug'.
```

### Ask Each Time

Inject an `ObjectProvider` instead, and ask it each time. Each call builds a new listing.

```
  two calls, same object: false.
  the second caller sees: 'Untitled'.
```

### Nobody Cleans Up

Spring calls destroy methods on singletons when the container closes, and never on prototypes.

```
  listings built: 3. listings destroyed on close: 0.
  the singleton's destroy method ran 1 time on close.
  Spring builds a prototype and lets go of it. Cleaning up is the caller's job.
```

## The verdict

Use the prototype scope for a fresh, identical object. Ask for it through an ObjectProvider inside a singleton. Copy an edited draft with a copy method of your own. Clean up after it yourself.

## How to recognise this in code you did not write

- `@Scope("prototype")` on a class.
- An `ObjectProvider<T>` or `Provider<T>` in a constructor.
- `getBean` called in a loop or per request.

## Where you have already met this

Per-request helpers, builders with state, and command objects. Any bean marked prototype.

## When this is too much

If the object is cheap and has no state to configure, `new` is simpler than a scope.
