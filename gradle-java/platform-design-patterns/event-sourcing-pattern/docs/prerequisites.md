# Prerequisites

This is the first project in the platform category, and it is the most demanding
pattern in it. The code, though, is deliberately small: three records, a list, and a
loop that adds numbers up. If you can read a `for` loop you can read all of it.

## Knowledge Prerequisites

### Required

- **Java basics** — classes, interfaces, methods, `for` loops.
- **Collections** — `List` and `Map`, and what "iterate in order" means.
- **Running Gradle** — `./gradlew run` and `./gradlew test`. Nothing more.

### Helpful, but explained as we go

- **Records** (`record PointsAwarded(...)`). A record is a class whose only job is to
  hold values, written in one line. `record Point(int x, int y) {}` gives you a
  constructor, `x()`, `y()`, `equals`, `hashCode` and `toString`. That is all you
  need to know for this project.
- **Sealed interfaces** (`sealed interface LoyaltyEvent permits ...`). Sealed means
  "these are the only implementations there will ever be". The compiler enforces it,
  which is useful when you want to be told about every place that handles events the
  day you add a fourth kind.
- **Pattern matching for `instanceof`** (`if (e instanceof PointsAwarded a)`). This
  is the old `instanceof` plus a cast, written once instead of twice.
- **`LocalDate`** — a calendar date with no time and no time zone. Created with
  `LocalDate.of(2025, 3, 1)`, compared with `isAfter` and `isBefore`.

### Explicitly NOT required

- **Any database.** There is none. The event store is an `ArrayList`.
- **Kafka, or any message broker.** Event sourcing is regularly taught alongside
  Kafka and the two are not the same subject. A log here is a list.
- **CQRS.** It is in this project, but as a *contrast* — the whole of Act 9 exists to
  show that the two patterns are separate. You do not need to know it going in.
- **Docker, Spring, Kubernetes, or a network.** The project runs offline with a JDK.
- **Functional programming.** "Fold" gets used because it is the standard name for
  this, but the fold in the code is a `for` loop with a running total.

## A 60-Second "Event Sourcing" Primer

Most software stores **the current state**. A customer has 140 loyalty points, so
there is a row with `140` in it, and when they earn more you replace the number.

Event sourcing stores **what happened**, in order, and never changes it. Instead of
`140` there are four records: earned 60, spent 25, earned 120, expired 15. When
somebody asks for the balance you add them up and get 140.

The number is not stored anywhere. It is worked out every time.

That sounds like more work for the same answer, and it is, right up until somebody
asks a question the number cannot answer — *why* is it 140, what was it three weeks
ago, which of these balances did that bug touch — at which point the current-state
version has nothing to say and the log has everything.

The word **fold** means "walk a list, carrying a running total". The word
**projection** means "the thing you get at the end of a fold". The word **snapshot**
means "a saved fold result so you do not have to start from the beginning". None of
the three is harder than that.

## A 60-Second "Append-Only" Primer

The event store in this project has exactly one way to write to it:

```java
public void append(LoyaltyEvent event) {
    events.add(event);
}
```

There is no `update` and no `delete`. When you find yourself asking "but what if the
event was wrong?", the answer is always the same: you add a new event that corrects
it, and both stay in the log forever. This is how bank statements work, how
accountants have worked for five hundred years, and how `git` works — you cannot
change a commit, only add one.

That rule is what everything good about the pattern rests on, and it is also the
source of everything hard about it. Half this project is about the rule paying off,
and half is about the bill.

## Software Prerequisites

| Tool | Version | Why |
| --- | --- | --- |
| JDK | 21 or newer | Records, sealed interfaces and pattern matching |
| Gradle | none needed | The wrapper is committed; it fetches Gradle 9.2.1 itself |

### Installing JDK 21

**macOS**

```bash
brew install openjdk@21
```

**Linux**

```bash
sudo apt install openjdk-21-jdk     # Debian, Ubuntu
sudo dnf install java-21-openjdk    # Fedora
```

**Windows** — download a JDK 21 build from [Adoptium](https://adoptium.net) and run
the installer.

### Verify Your Setup

```bash
java -version      # should say 21 or higher
./gradlew test     # 31 tests, about a second
./gradlew run      # nine acts of output
```

The first `./gradlew` run downloads Gradle itself and needs the internet once.
Everything after that is offline.

## Troubleshooting

**`Unsupported class file major version`** — you are on a JDK older than 21. Check
`java -version` and `echo $JAVA_HOME`.

**`./gradlew: Permission denied`** — `chmod +x gradlew`.

**The demo prints different numbers from the documents** — it should not. Every date
in the demo is a fixed `LocalDate` constant and nothing is random, so two runs are
byte-identical. `DemoRunsTest` asserts that. If it has drifted, the code changed and
the documents did not.

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — the row that cannot answer the question
2. `./gradlew run` — nine acts, benefits first, then the bill
3. [`event-sourcing-pattern-explained.md`](event-sourcing-pattern-explained.md) — the bank statement, the code, the costs, and CQRS
4. [`class-diagram.md`](class-diagram.md) — the types, and the missing balance field
5. [`uml-diagram.md`](uml-diagram.md) — four sequences
6. [`animation.html`](animation.html) — the log filling up and the fold running
7. The tests, starting with `CurrentStateLoyaltyAccountsTest`, every one of which passes
