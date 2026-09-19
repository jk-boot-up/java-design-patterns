# Problem Statement

## Read the partner first

This project assumes [Prototype](../prototype-pattern), which copied a fully assembled product listing into variants, deciding field by field what a copy means, and kept a registry of templates. Nothing here is lost by skipping Spring Boot, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: a product listing that is costly to assemble and needed in several variants.

## What is new

Spring has a **prototype scope**: ask the container for the bean and it builds a new one from the definition each time.

```
  same object: false. both are titled 'Untitled'.
```

## The failure this project exists to show

The container builds from the definition, not from a draft you have edited, so it is not a copy. Injected into a singleton, a prototype is built once and shared. And Spring never cleans it up.
