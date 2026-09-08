# Prerequisites

What you need to know, and what you need installed, before working through
this Bridge pattern demo.

## Knowledge Prerequisites

You do **not** need prior design-pattern experience. You do need comfortable
familiarity with core Java.

### Required

| Topic | Why it matters here | Quick self-check |
| --- | --- | --- |
| **Interfaces** | `MessageChannel` is the shared type `EmailChannel`, `SmsChannel`, and `PushChannel` implement | Can you write an interface and three classes implementing it? |
| **Abstract classes** | `Notification` is abstract; it implements `send()` once and leaves `subject()`/`body()` for subclasses | Do you know the difference between an interface and an abstract class in Java? |
| **Composition over inheritance** | `Notification` *holds* a `MessageChannel` field rather than subclassing per channel | Can you explain why `Notification` is not `abstract class Notification implements MessageChannel`? |
| **`final` fields set in a constructor** | `Notification.channel` is `private final`, assigned once | Do you know why a `final` field must be assigned in every constructor path? |
| **`BigDecimal`** | `OrderConfirmationNotification.total` is `BigDecimal`, not `double` | Do you know why money is usually not stored as `double`? |

### Helpful, but explained as we go

| Topic | Where it appears |
| --- | --- |
| **String truncation (`substring`)** | `SmsChannel`'s 140-character limit |
| **JUnit 5 basics** | Every `*Test.java` file |
| **`System.setOut` / stdout capturing** | Tests that assert on printed output |
| **Gradle basics** | `build.gradle`, `./gradlew run` |
| **UML class & sequence diagrams** | The diagram docs |

### Explicitly NOT required

- Spring, Spring Boot, or any framework
- A real email/SMS/push provider — every channel in this project just
  prints to the console
- Any UI toolkit
- Any other design pattern

## A 60-Second "Two Hierarchies" Primer

If "two independent hierarchies connected by composition" feels abstract,
this is all you need:

```java
public abstract class Notification {
    private final MessageChannel channel;   // <-- the bridge: a field, not a superclass

    protected Notification(MessageChannel channel) {
        this.channel = channel;
    }

    public final void send(String recipient) {
        channel.deliver(recipient, subject(), body());   // delegate; never inspect the channel
    }
}
```

`Notification` never has a subclass called `EmailNotification` or
`SmsNotification`. It has a *field* that happens to be an email channel or
an SMS channel. That field is the entire bridge — one line, no inheritance
across the two hierarchies.

## A 60-Second Abstraction vs. Implementor Primer

- **Abstraction** = "what to say" = `Notification` and its subclasses. They
  compose a subject and a body and know nothing about delivery mechanics.
- **Implementor** = "how to deliver it" = `MessageChannel` and its
  implementations. They know delivery mechanics (truncate at 140 chars,
  drop the body) and know nothing about what a specific notification says.

Neither hierarchy ever imports or extends the other. The only place they
meet is the `channel` field inside `Notification`.

## Software Prerequisites

| Tool | Minimum version | Check with |
| --- | --- | --- |
| **JDK** | 21 | `java -version` |
| **Gradle** | 8.x+ (or use the bundled wrapper) | `gradle -v` |
| **Git** | any recent | `git --version` |
| **IDE** | IntelliJ IDEA / VS Code / Eclipse | — |

### Installing JDK 21

**macOS (Homebrew)**
```bash
brew install --cask temurin@21
java -version
```

**Linux (SDKMAN)**
```bash
curl -s "https://get.sdkman.io" | bash
sdk install java 21-tem
```

**Windows** — download the Temurin 21 MSI from
[adoptium.net](https://adoptium.net) and run the installer.

Expected output:
```
openjdk version "21.0.1" 2023-10-17 LTS
```

### Gradle

You do not need to install Gradle — the project ships a wrapper:

```bash
./gradlew build     # macOS / Linux
gradlew.bat build   # Windows
```

The first run downloads the correct Gradle version automatically, so an
internet connection is needed once. If you already have Gradle installed,
plain `gradle build` works too.

## Verify Your Setup

Run these three commands from the project directory. All three must succeed
before the session.

```bash
java -version      # must report 21
./gradlew build    # must end with BUILD SUCCESSFUL
./gradlew run      # must print notifications going out over three channels
```

Expected output from `./gradlew run` (abridged — see
[`../README.md`](../README.md) for the full transcript):

```
== Same notification, delivered through three different channels ==
[EMAIL to alex@example.com] Order ORD-1042 confirmed -- Your order ORD-1042 totalling $129.99 has been confirmed.
[SMS to +1-555-0142] Order ORD-1042 confirmed: Your order ORD-1042 totalling $129.99 has been confirmed.
[PUSH to device-9f31] Order ORD-1042 confirmed
...
```

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Unsupported class file major version` | Wrong JDK on `PATH` | Point `JAVA_HOME` at JDK 21 |
| `permission denied: ./gradlew` | Wrapper not executable | `chmod +x gradlew` |
| Wrapper download times out | Offline / proxy | Install Gradle and run `gradle build` |
| SMS output has no `…` when you expected truncation | Combined subject+body is under 140 characters | That is correct behavior — only messages over the limit truncate |
| Diagrams show as raw text | Viewer lacks Mermaid support | Open the PNGs in `docs/images/` |

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — why we need this
2. [`bridge-pattern-explained.md`](bridge-pattern-explained.md) — the pattern
3. [`class-diagram.md`](class-diagram.md) — static structure
4. [`uml-diagram.md`](uml-diagram.md) — runtime flow
5. [`animation.html`](animation.html) — watch it happen
6. The source code in `src/main/java/com/jk/explore/bridge/`
7. [`session.md`](session.md) — the guided walkthrough
