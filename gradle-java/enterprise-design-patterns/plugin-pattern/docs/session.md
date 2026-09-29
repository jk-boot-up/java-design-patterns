# Session Guide — Plugin Pattern

## Learning Objectives

By the end of the session you can:

- Explain the risk of choosing implementations with scattered ifs.
- Wire implementations from a configuration file.
- Add an environment without changing code.
- Check plugins at startup, and name what is lost.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Choices scattered in code | 7 min |
| 0:17 | Act 2: Plugins from configuration | 7 min |
| 0:24 | Act 3: A new environment | 7 min |
| 0:31 | Act 4: Caught at startup | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act one: a real email from staging. Open the three
`plugins-*.properties` files side by side. Then open `PluginFactory.get`: read
a line, create a class. End with `check`, and ask why it matters that it runs
at startup.

## Exercises

1. Add a `TaxService` interface with a flat-rate and a real implementation, and configure both.
2. Replace `PluginFactory` with Java's `ServiceLoader`. What changes in the files?
3. Make the factory refuse to start production if any plugin name contains "Fake" or "Sandbox".
