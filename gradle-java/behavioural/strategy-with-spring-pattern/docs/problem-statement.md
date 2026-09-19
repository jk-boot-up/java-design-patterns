# Problem Statement

## Read the partner first

This project assumes [Strategy](../strategy-pattern), which priced the same delivery under four interchangeable rules, chose one by configuration name, and refused an unknown name. Nothing here is lost by skipping Spring Boot, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: four delivery pricing rules, flat, weight banded, distance based and free over a threshold.

## What is new

Spring **collects the strategies for you**. Ask for a `Map<String, Rule>` and it hands over every bean of that type, keyed by its bean name.

```
  rules found: [distance, flat, freeOverThreshold, weightBanded].
  the keys are bean names, chosen in the @Component annotations.
```

## The failure this project exists to show

The keys are bean names, so a rename changes them. Asking for the interface alone fails when there are several beans. And a wrong name in configuration is only caught if you check it at startup.
