# Problem Statement

## Read the partner first

This project assumes [Interpreter](../interpreter-pattern), which turned promotion rules written as text into a tree of small rule objects, and applied them to orders, with a parser written by hand. Nothing here is lost by skipping Spring Expression Language, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: marketing writes a promotion as a line of text, and the shop applies it to orders.

## What is new

The **Spring Expression Language**, SpEL, is an interpreter that already exists. It parses a rule into a tree once, and evaluates the tree against any object.

```
  WELCOME10 | 10 | firstOrder
  UKBIG | 15 | country == 'UK' and basketPence > 5000
  BULK | 20 | items >= 5 or basketPence > 20000
  NOTUK | 5 | !(country == 'UK')
  asha  (UK, 60.00, 2 items):            [UKBIG (15% off)]
  ben   (DE, 30.00, 1 item, first):      [WELCOME10 (10% off), NOTUK (5% off)]
  carol (UK, 250.00, 6 items):           [UKBIG (15% off), BULK (20% off)]
```

## The failure this project exists to show

The language is far bigger than the four words we needed. A typo in a name is found only when an order arrives. And in the full context, a rule can call any static method in the program.
