# Circuit Breaker with Resilience4j Pattern — Video Narration Script

## 1. Circuit Breaker with Resilience4j

Hello, and welcome. This video explains the Circuit Breaker pattern with Resilience4j, in Java, and it is written and presented by Jayasekhar Konduru. It is the framework version of the Circuit Breaker video. That one built a breaker with three states by hand, so a product page stopped waiting on a recommendations service that had gone quiet, and failed instantly instead. This one shows the same idea inside Resilience4j. The plain definition, in short: in Resilience4j, a circuit breaker is an annotation on a method, and its thresholds are configuration. By the end you will see the same breaker as an annotation and a few settings, then see how it can be bypassed, how it hides failures, and how a wrong setting trips it for the wrong reason.

## 2. The Partner Project

This video assumes the Circuit Breaker video. If you have not seen it, start there. It counts failures, opens the breaker when there are too many, fails instantly while open, and lets one probe through later to see whether the service has recovered. This one uses the same example. It does not teach the pattern again. It shows what Resilience4j does with it.

## 3. Before The First Line

Before the first line of code, what Resilience4j is. Resilience4j is a library of resilience patterns for Java. It contains a circuit breaker with three states, and a Spring Boot module that turns it into an annotation. And a promise: skipping this video loses none of the pattern. The hand-built one teaches all of it.

## 4. Healthy

First, the good day. The product page asks for recommendations, and gets two products. The breaker is closed, which means calls flow. One call reached the service.

## 5. The Service Goes Down

Second, the service goes down. The window holds the last four calls, and the healthy one from act one is still in it. Each failure shows an empty list on the page, not an error. At the third failure, three of the last four have failed, and the breaker opens. The fourth call never reaches the service.

## 6. Open: Fail Fast

Third, the payoff. A hundred more page views, and not one reaches the service. The breaker refuses every one, instantly, and the fallback answers with an empty list. The struggling service gets a rest. But notice: the page never saw an error. The only alarm is the breaker's state.

## 7. Half-Open: One Probe

Fourth, the probe. The demo moves the breaker to half-open, which in production a wait duration does by itself. One call is let through. The service is still down, so it fails, and the breaker opens again. Then the service comes back. The next probe works, and the breaker closes.

## 8. What Counts As A Failure

Fifth, what counts as a failure. Eight requests for a product that does not exist. That is the caller's mistake, not the service's. The breaker with an ignore list stays closed. The breaker that counts everything opens, and blocks good requests. The ignore list is one line in the settings, and easy to forget.

## 9. The Annotation Is A Proxy

Last, the annotation is a proxy. A method inside the client calls its own protected method, on this. That call skips the proxy, and so the breaker and the fallback. All ten errors reach the caller. All ten calls hit the struggling service. The breaker stays closed. The same rule as every Spring proxy: call it from outside.

## 10. The Verdict

My verdict, plainly. Configure the window and the threshold on purpose. List the exceptions that are not failures. Alert on the breaker's state, because the fallback hides the errors. And call protected methods from outside the bean.

## 11. How To Recognise It

How do you recognise this in code you did not write? A circuit breaker annotation with a name and a fallback method. And settings under resilience four j circuit breaker in the configuration.

## 12. Where You Have Met This

You have met this in any Spring service that calls another service over the network, and must keep serving when it fails.

## 13. What Was Used

For the record. Spring Boot four point one point one. Resilience four j two point four point zero. No web server, and no web starter.

## 14. What Is Real Here

The same honest admission as everywhere in this course. Everything is real: the real breaker and the real annotation. The clock is not used. The demo starts the probe itself, so the numbers are the same every run.

## 15. When This Is Too Much

So when is it too much? For a call that is local, fast and reliable, a breaker is only more code.

## 16. Thanks for Watching

That's Circuit Breaker with Resilience4j. If you take one sentence away, take this one: Resilience4j gives you the breaker as configuration, and the state is your only alarm. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, remove the ignore list, and rerun act five. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
