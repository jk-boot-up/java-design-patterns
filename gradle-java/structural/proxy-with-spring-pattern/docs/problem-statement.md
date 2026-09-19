# Problem Statement

## Read the partner first

This project assumes [Proxy](../proxy-pattern), which stood a lazy proxy and a protection proxy in front of a product image, each written by hand, and composed the two. Nothing here is lost by skipping Spring Boot, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: a product image that is costly to load and that only a catalogue admin may view.

## What is new

Spring **writes the proxy for you**. It wraps a bean in a generated subclass and runs your advice, an aspect, before and after each call.

```
  is a generated proxy: true
  its class is a subclass of ImageCatalogue: true
  the class Spring wrapped: ImageCatalogue
```

## The failure this project exists to show

The generated proxy only sees calls that come through it. A call on `this` skips it, and a `final` method cannot be overridden, so both run unprotected.
