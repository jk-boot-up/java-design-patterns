# Onion Architecture, Explained

## The pattern in one sentence

Onion architecture arranges code in rings, with the business rules at the centre, and lets every ring depend only on rings further in, never outward.

## The six acts

### The Core Reaches Outward

The order saved itself with a SQL statement. To change the storage, the order class, at the centre, must be edited.

```
  the order saved itself with a SQL statement. statements run: 1.
  to change the storage, the order class, at the centre, must be edited.
```

### Rings, And One Rule

Ring zero is the order, the order line, and the idea of a repository. Ring one is the pricing rules. Ring two is the use cases. Ring three is storage and screens. The rule: a class may refer to its own ring, or to a ring further in, never outward. Among the eight classes of the onion, violations: none.

```
  ring 0: order, order line, the repository idea. ring 1: pricing rules. ring 2: use cases. ring 3: storage and screens.
  the rule: a class may refer to its own ring, or to a ring further in. never outward.
  violations among the 8 classes of the onion: 0.
```

### Checking The Rule

The checker is pointed at the naive order. It reports: the naive order, in ring zero, refers to the SQL database, in ring three. The checker reads the fields, constructors and methods of each class, so the rule is tested, not just hoped for.

```
  the naive order: [NaiveOrder (ring 0) refers to SqlDatabase (ring 3)].
  the checker reads the fields, constructors and methods of each class, so the rule is tested, not just hoped for.
```

### Swap The Outside

Stored in memory, the total is ten thousand eight hundred. Stored as a text record, the same. The record is the order id, the mug, two at sixty pounds, and a discount of twelve hundred. The use case, the rules and the order were not touched.

```
  in memory: total 10800. as a text record: total 10800. the record: ORD-1|MUG:2:6000|discount:1200.
  the use case, the rules and the order were not touched.
```

### The Inside, On Its Own

A small order is nine fifty. A big order is ten thousand eight hundred, ten percent off twelve thousand. No storage, no screen and no framework was used to check the rules. Through the outside, the same order gives the same total.

```
  small order total: 950. big order total: 10800 (10% off 12000).
  no storage, no screen, no framework was used to check the rules.
  through the outside, the same order: ORD-3 total 10800.
```

### The Bill

One order saved and read back through the outer ring costs two conversions. Every trip across a ring may copy the order into another shape. To place one order there are four classes in three rings, plus the repository idea. For a small program, that is a lot of ceremony. And the repository idea lives in the centre, so the centre knows that storage exists, though not how.

```
  one order saved and read back through the outer ring: conversions 2. every trip across a ring may copy the order into another shape.
  and to place one order there are 4 classes in 3 rings, plus the repository idea. for a small program, that is a lot of ceremony.
  the repository idea lives in the centre, so the centre knows that storage exists, though not how.
```

## The verdict

Put the business rules at the centre, and let everything else depend on them. Let the centre own the ideas it needs, such as a repository, and let the outside supply them. Check the rule with a test, not a diagram. Do not use it for a program too small to have an outside worth swapping.

## How to recognise this in code you did not write

- Packages named `domain`, `application` and `infrastructure`.
- An interface in the domain package, implemented in the infrastructure package.
- Entities with no framework annotations, and a use-case class that receives its repository.
- An ArchUnit test that fails when domain code imports infrastructure.

## Where you have already met this

Domain-driven design projects, Jeffrey Palermo's original onion write-up, and most well-kept Spring codebases that keep the domain free of JPA.

## When this is too much

For a small tool with one fixed storage and few rules, rings are heavier than the problem. They pay off when rules are rich and the outside changes.
