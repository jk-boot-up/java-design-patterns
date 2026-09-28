# Circuit Breaker with Resilience4j Pattern — Video Narration Script

## 1. Circuit Breaker with Resilience4j

Hello, and welcome. This video explains the Circuit Breaker pattern in Java, using a library called Resilience four J. This video is presented by Jayasekhar Konduru. First, a simple definition. A circuit breaker stops calling a service that keeps failing. It fails instantly for a while. Then it lets one test call through, to see whether the service has recovered. Think of the fuse box in a house. It trips when there is a fault, stays off, and is switched back on once, to check. In Resilience four J, the breaker is an annotation on a method, and its limits are settings. In our online store, a product page shows recommendations from a separate service. By the end, you will hear the same breaker built from one annotation and a few settings. Then how it can be skipped by accident. How it hides failures. And how a wrong setting trips it for the wrong reason.

## 2. The Partner Project

This video builds on the plain Java Circuit Breaker video. If you have not seen it, start there. That video counts failures, and opens the breaker when there are too many. While open, it fails instantly. Later, it lets one test call through, to see whether the service has recovered. This video uses the same example. It does not teach the pattern again. It shows what Resilience four J does with it.

## 3. Before The First Line

Before any code, what is Resilience four J? It is a library of resilience patterns for Java. It includes a circuit breaker with three states. Closed, which means calls go through. Open, which means calls are refused. And half-open, which lets one test call through. It also has a Spring Boot module that turns the breaker into an annotation. And a promise. Skipping this video loses none of the pattern. The plain Java video teaches all of it.

## 4. Healthy

First demo: a good day. The product page asks for recommendations, and gets two products. The breaker is closed, which means calls go through. One call reached the service.

## 5. The Service Goes Down

Second demo: the service goes down. The breaker looks at the last four calls. And the healthy call from the first demo is still one of them. Each failure shows an empty list on the page, not an error. At the third failure, three of the last four calls have failed. So the breaker opens. The fourth call never reaches the service.

## 6. Open: Fail Fast

Third demo: the payoff. A hundred more page views. And not one of them reaches the service. The breaker refuses every call, instantly. A fallback method, which is a backup answer, returns an empty list. And the struggling service gets a rest. But notice this. The page never saw an error. So the only warning sign is the breaker's state.

## 7. Half-Open: One Probe

Fourth demo: the test call. The demo moves the breaker to half-open. In a real system, a waiting time does that by itself. One call is let through. The service is still down, so it fails. And the breaker opens again. Then the service comes back. The next test call works. And the breaker closes.

## 8. What Counts As A Failure

Fifth demo: what counts as a failure? Eight requests arrive, for a product that does not exist. That is the caller's mistake, not the service's. One breaker has a list of errors to ignore, and it stays closed. Another breaker counts every error. It opens, and starts blocking good requests too. That ignore list is one line in the settings. And it is easy to forget.

## 9. The Annotation Is A Proxy

Last demo: a trap. Spring adds the breaker by wrapping the object in a proxy. A proxy is a stand-in that sits in front of the real object, and checks each call on the way in. Here, a method inside the client calls its own protected method directly. That call never goes through the proxy. So it skips both the breaker and the fallback. All ten errors reach the caller. All ten calls hit the struggling service. And the breaker stays closed, because it saw nothing. The rule is the same for every Spring proxy. Call the protected method from outside the object.

## 10. The Verdict

So, here is the verdict. Choose how many calls the breaker looks at, and its failure limit, on purpose. List the errors that are not real failures. Alert on the breaker's state, because the fallback hides the errors. And call protected methods from outside the object.

## 11. How To Recognise It

How can you spot this in code someone else wrote? Look for a circuit breaker annotation, with a name and a fallback method. And look for circuit breaker settings in the configuration file.

## 12. Where You Have Met This

Where have you met this before? In any Spring service that calls another service over the network. And must keep serving when that service fails.

## 13. What Was Used

For the record, here is what was used. Spring Boot, version four point one point one. Resilience four J, version two point four point zero. There is no web server, and no web starter.

## 14. What Is Real Here

A quick, honest note about this demo. Everything is real: the real breaker, and the real annotation. The clock is not used. The demo starts the test call itself, so the numbers are the same on every run.

## 15. When This Is Too Much

So, when is this too much? For a call that is local, fast, and reliable, a breaker is only more code.

## 16. Thanks for Watching

That's Circuit Breaker, with Resilience four J. If you remember one sentence, make it this one. Resilience four J gives you the breaker as settings, and its state is your only warning sign. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Remove the ignore list, and run the fifth demo again. Guess first whether the breaker will open. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
