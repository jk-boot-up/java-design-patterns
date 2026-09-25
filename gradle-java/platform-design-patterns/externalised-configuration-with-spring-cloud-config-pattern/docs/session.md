# Session Guide — Externalised Configuration with Spring Cloud Config Pattern

A 60-minute session built around one question: once the setting lives in git behind a config server, when does a running shop actually use a new value, and which parts of it never do?

## Learning Objectives

1. Say, in plain words, what a config server, a commit and its version, fetching at startup, a refresh and `@RefreshScope` are.
2. Show a commit the server serves at once and the running shop does not use, and a refresh that puts it in force with no restart.
3. Explain why the banner kept £50.00 after the refresh, and name two ways to fix it.
4. Explain why a range check with nothing behind it made every quote fail.
5. Compare fail fast and optional when the server is down, and say which you would choose for a checkout.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:08 | The bakery head-office analogy, and the twin project recapped in two minutes |
| 0:08–0:18 | Acts one and two: served over HTTP, then committed but not in force |
| 0:18–0:26 | Act three: the refresh |
| 0:26–0:38 | Act four: two thresholds in one shop |
| 0:38–0:46 | Act five: the value nobody checked, and git's log |
| 0:46–0:54 | Act six: the server stops |
| 0:54–1:00 | Exercises |

## Walkthrough

No container runtime is needed.

```bash
cd platform-design-patterns/externalised-configuration-with-spring-cloud-config-pattern
./gradlew -q run
```

Act one: which process holds the threshold, and how did the shop get it? Act two: why does the server say 35.0 while the shop quotes on £50.00? Act three: what does `config.client.version` mean, and how do we know the shop did not restart? Act four: why did the banner not move? Act five: why did the refresh answer 200 when the value was going to be refused? Act six: which of the two new copies would you rather have on a Saturday morning?

Then open `src/main/java/com/jk/explore/springcloudconfig/shop/DeliverySettings.java` and `PromotionBanner.java` side by side. Read the annotations aloud. The only difference that matters is `@RefreshScope` on one and a constructor `@Value` on the other.

## Discussion

Ask the room who sends the refresh in a real estate with twenty copies of the shop. By hand, after every commit? A pipeline step after the merge? Spring Cloud Bus, which broadcasts one refresh to every copy through a message broker? Each answer has a failure: the copy that was down when the refresh went out, and comes back on old values.

Then ask whether the shop should fall back to the last good value when a refresh brings in a bad one. The twin did. What would it take here? Where would the last good value live, so that it survives the refresh that throws the settings object away?

## Exercises

1. Mark `PromotionBanner` with `@RefreshScope`, run act four, and predict what the banner says after the refresh.
2. Instead, change `PromotionBanner` to read `DeliverySettings` on every call rather than copying the value. Which fix would you rather defend in a code review?
3. Commit `free-over: fifty` instead of `-1` and predict the status of the refresh and of the next quote before you run it.
4. Add a `checkout-service-weekend.yml` to the repository with a different threshold, start the shop with the profile `weekend`, and see which value wins.
5. Write a small class that keeps the last value that passed the range check and hands it out when the rebuild fails. Where must it live so that the refresh does not throw it away?

Close with the verdict: a commit is not in force until a refresh, a refresh reaches only what is refresh-scoped, a range check needs a fallback, and every service must choose between fail fast and optional.
