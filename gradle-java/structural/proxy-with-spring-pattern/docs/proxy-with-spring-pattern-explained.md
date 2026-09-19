# Proxy with Spring, Explained

## The pattern in one sentence

In Spring, a proxy is generated at runtime around a bean, and an aspect says what it does on each call.

## What is new here

The pattern is [Proxy](../proxy-pattern). This page is only what Spring Boot adds.

### The Bean Is Not Your Class

The bean you receive is a generated subclass of your class, wrapped around the real one.

```
  is a generated proxy: true
  its class is a subclass of ImageCatalogue: true
  the class Spring wrapped: ImageCatalogue
```

### Protection, Written Once

The aspect refuses a shopper before the real method runs. An admin passes through.

```
  admin: full-resolution pixels of MUG-BLUE
  shopper: refused: render needs CATALOG_ADMIN but the caller is SHOPPER
```

### Lazy Loading

With lazy on both the class and the injection point, the image is not built until the first render.

```
  after startup: 0 images loaded.
  a cheap question, owner(): catalogue. images loaded: 0.
  after the first render: 1 image loaded.
```

### One Aspect, Three Screens

The same aspect protects the catalogue, the order export and the refund desk. The rule exists once.

```
  catalogue: refused: render needs CATALOG_ADMIN but the caller is SHOPPER
  export: refused: exportAll needs CATALOG_ADMIN but the caller is SHOPPER
  refunds: refused: refund needs CATALOG_ADMIN but the caller is SHOPPER
  the check was written once, in RoleAspect.
```

### A Call On this

A method that calls its own protected method on this skips the proxy, and the rule.

```
  render, called from outside: refused: render needs CATALOG_ADMIN but the caller is SHOPPER
  renderThroughThis, a shopper: full-resolution pixels of MUG-BLUE
  the shopper got the image. nothing was logged.
```

### A Final Method

A final method cannot be overridden by the generated subclass, so the proxy runs it directly, on an instance whose fields were never set.

```
  renderFinal, a shopper: NullPointerException: the proxy instance has no fields of its own
```

## The verdict

Write each rule once, in an aspect. Call protected methods from outside the bean. Avoid final methods on proxied beans. Test the refusal, not just the success.

## How to recognise this in code you did not write

- `@Aspect` with `@Around`.
- `@Transactional`, `@Cacheable`, `@Async` or `@PreAuthorize` on a method.
- A bean class name that ends in `$$SpringCGLIB$$` in a stack trace.

## Where you have already met this

Every `@Transactional` method. It is a proxy that opens and closes the transaction around your call.

## When this is too much

For one class with one rule, a hand-written wrapper is easier to read than an aspect.
