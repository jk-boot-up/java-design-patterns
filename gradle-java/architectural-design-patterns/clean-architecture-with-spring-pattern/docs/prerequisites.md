# Prerequisites

## Knowledge Prerequisites

### Required

- **[`../clean-architecture-pattern`](../clean-architecture-pattern) —
  built and watched first, always.** This project is only legible to
  someone who has already seen the hand-wiring; it names §66 in its own
  first paragraph for exactly that reason.
- **Java basics**, plus enough familiarity with annotations to read
  `@Configuration` and `@Bean` without being alarmed by them.

### Helpful, but explained as we go

- **Spring Boot**, in any capacity. If you have never used it,
  [`dependencies.md`](dependencies.md) explains what it is before the
  first annotation appears.

### Explicitly NOT required

- **No web application, no database, no HTTP.** This project uses only
  `spring-boot-starter` — core dependency injection — nothing else.
- **A course on Spring itself.** This project answers one question — what
  changes when a container wires the graph — and stops. It is not a
  general Spring tutorial.

## Software Prerequisites

| Need | Version | Why |
| --- | --- | --- |
| JDK | 21 or later | The repository standard |
| Gradle | none to install | The wrapper (`./gradlew`) fetches Spring Boot 4.1.1 and everything else on first run — needs a network connection once |

### Verify Your Setup

```bash
java -version
cd architectural-design-patterns/clean-architecture-with-spring-pattern
./gradlew test         # expect BUILD SUCCESSFUL, 11 tests
./gradlew run          # expect five acts, a startup failure, then ACCEPTANCE
```

## Recommended Reading Order

1. [`../clean-architecture-pattern`](../clean-architecture-pattern), completely, first
2. [`dependencies.md`](dependencies.md) — what Spring is, and what it costs
3. Run `./gradlew run` and read all five acts, especially act five
4. [`clean-architecture-with-spring-pattern-explained.md`](clean-architecture-with-spring-pattern-explained.md)
5. The source: `config/AppConfig.java` next to §66's `PlaceAnOrderDemo.shop()`
6. `WiringContrastTest`
