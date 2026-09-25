# Problem Statement

## The scenario

The shop gives free delivery on any basket over a threshold, and charges £4.99 below it. The threshold is £50.00. Marketing decides it, not engineering, and marketing works to its own calendar: on Friday at half past four they want £35.00 for the weekend. The shop runs as a Spring Boot program, and more than one copy of it is normal. Nobody wants a rebuild, a release and a restart to move one number.

## The naive version

The threshold is written into the shop, in its own settings file, packed inside the program. Changing it means building the shop again and restarting every copy. The sixth act shows what such a shop does when it is started with nothing else to go on: it quotes on the value packed inside it.

```
    quote:  goods £48.00 delivery £4.99 threshold £50.00
```

## What the twin project already did

The plain-Java Externalised Configuration project in this course moved the threshold out of the checkout code and into a configuration source, and had the checkout read it on every quote, so a change was in force on the very next quote. It showed what the value lost on the way out of the source file — the compiler, the reviewer, the history and the revert — and bought each one back by hand: a typed setting, a declared range with a fallback to the last good value, a change log, and a rollback. It is a complete teaching of the idea and nothing here replaces it.

It had comforts, though. The configuration source was a map in the same program, so there was no network and no fetch: the checkout simply looked every time. There was only one reader, so nothing could hold on to an old copy. And the source going away was a field set to false.

## What this project must deliver

The same shop, the same £48.00 basket and the same move from £50.00 to £35.00, with the threshold in a git repository, a real Spring Cloud Config Server in front of it as a separate process, and a real Spring Boot shop that fetches its settings over HTTP. A commit the server serves at once and the running shop does not see. A refresh that puts it in force with no restart. The banner that the refresh does not reach. A value the range check refuses, and what that costs. And the config server stopping, with a running shop, a shop that must fail fast and a shop that may start without it.

Nothing needs a container: the server is a Java process the demo starts and stops. Every figure printed is the program's own, and two runs back to back print the same thing.
