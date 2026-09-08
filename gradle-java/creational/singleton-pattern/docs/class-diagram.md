# Singleton Pattern — Class Diagram

## The structure

![Singleton pattern class diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    direction TB

    class OrderSequenceGenerator {
        <<enumeration>>
        INSTANCE
        -counter AtomicLong
        +nextOrderNumber() String
    }

    class LegacyOrderSequenceGenerator {
        <<the trap>>
        -instance LegacyOrderSequenceGenerator$
        -counter int
        -LegacyOrderSequenceGenerator()
        +getInstance()$ LegacyOrderSequenceGenerator
        +nextOrderNumber() String
    }

    class OrderSequenceGeneratorDemo {
        +main(String[]) void
    }

    OrderSequenceGeneratorDemo ..> OrderSequenceGenerator : INSTANCE.nextOrderNumber()
    OrderSequenceGeneratorDemo ..> LegacyOrderSequenceGenerator : getInstance(), then attacks it
    OrderSequenceGenerator ..> OrderSequenceGenerator : reflection and serialization both rejected
    LegacyOrderSequenceGenerator ..> LegacyOrderSequenceGenerator : reflection and serialization both succeed
```

</details>

The shape to notice: `OrderSequenceGenerator` has no `getInstance()` method
and no private constructor to guard, because an `enum` constant is not
constructed by ordinary code at all — `INSTANCE` is a field the compiler
generates and initializes exactly once, during class loading.
`LegacyOrderSequenceGenerator` has the shape every singleton tutorial
teaches first — a private constructor, a static field, a public accessor —
and every one of those three pieces is a place a guarantee can leak.

## What the caller can see

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TB
    subgraph outside["Calling code"]
        normal["OrderSequenceGenerator.INSTANCE.nextOrderNumber()"]
        attacker["Constructor.newInstance() / ObjectInputStream.readObject()"]
    end

    subgraph inside["com.jk.explore.singleton"]
        good["OrderSequenceGenerator<br/><b>enum, one constant</b><br/>INSTANCE"]
        legacy["LegacyOrderSequenceGenerator<br/><b>class, private constructor</b><br/>getInstance()"]
    end

    normal --> good
    attacker -.->|"IllegalArgumentException"| good
    attacker -->|"succeeds — a second instance"| legacy

    style good fill:#dcfce7,stroke:#15803d,stroke-width:2px
    style legacy fill:#fee2e2,stroke:#b91c1c
```

</details>

## Notes

- There is no interface in this project's main flow the way `Prototype<T>`
  anchors the prototype-pattern project — the pattern here is entirely
  about controlling instantiation of one concrete type, not about a shared
  contract implemented by several types.
- `LegacyOrderSequenceGenerator` implements `Serializable` specifically so
  its deserialization flaw can be demonstrated. A class that never expects
  to be serialized would not need that interface at all, but plenty of
  real singletons pick it up accidentally by extending or implementing
  something that already does.
- Compare with
  [`../../prototype-pattern/docs/class-diagram.md`](../../prototype-pattern/docs/class-diagram.md).
  There, the interesting arrow is one type sharing a reference across
  copies of itself. Here, the interesting fact is the *absence* of an arrow
  — nothing else in the program is ever allowed to hold a second
  `OrderSequenceGenerator`.
