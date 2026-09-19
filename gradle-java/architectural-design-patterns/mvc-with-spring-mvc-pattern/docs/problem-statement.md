# Problem Statement

## Read the partner first

This project assumes [MVC](../mvc-pattern), which split an order summary into a model that works out the total, views that only show it, and a controller that connects them, and showed a second view added without touching the model. Nothing here is lost by skipping Spring MVC, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: an order summary, with one place that works out the total.

## What is new

**Spring MVC** is the framework's own controller layer. A method returns a view name and a model, and the framework finds a template, or turns the model into JSON, over real HTTP.

```
  GET /orders/ORD-000001, as a browser -> 200, text/html.
  the page says: Total: £292.50, Discount: £32.50.
```

## The failure this project exists to show

A template can do arithmetic, and then the view and the model disagree. A template written for one shape of order breaks on another. And the controller can quietly grow logic.
