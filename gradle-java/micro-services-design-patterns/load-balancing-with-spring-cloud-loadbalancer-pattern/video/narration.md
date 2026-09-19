# Load Balancing with Spring Cloud LoadBalancer Pattern — Video Narration Script

## 1. Load Balancing with Spring Cloud LoadBalancer

Hello, and welcome. This video explains the Client-Side Load Balancing pattern with Spring Cloud LoadBalancer, in Java, and it is written and presented by Jayasekhar Konduru. It is the framework version of the Client-Side Load Balancing video. That one chose among three copies of the catalogue service on the client side, with four hand-written strategies, and showed that a fair strategy is not always a fast one. This one shows the same idea inside Spring Cloud LoadBalancer. The plain definition, in short: in Spring Cloud LoadBalancer, the caller uses a service name, and a balancer picks one copy of the service for each request. By the end you will see twelve real requests spread by a real balancer, then see fair not being fast, a strategy of your own, a stopped copy, and the trap of real addresses.

## 2. The Partner Project

This video assumes the Client-Side Load Balancing video. If you have not seen it, start there. It chooses among three copies of the catalogue service on the client side, with four strategies written by hand, and shows that a fair strategy is not always a fast one. This one uses the same example. It does not teach the pattern again. It shows what Spring Cloud LoadBalancer does with it.

## 3. Before The First Line

Before the first line of code, what Spring Cloud LoadBalancer is. Spring Cloud LoadBalancer is a client-side balancer for Spring. The caller uses a service name, and the balancer picks a copy for every request. Round robin is the default. And a promise: skipping this video loses none of the pattern. The hand-built one teaches all of it.

## 4. Twelve Requests, One Name

First, the default. Twelve requests go to the name catalogue. The balancer spreads them four, four and four. The caller wrote only a name, and never saw an address.

## 5. Fair Is Not Fast

Second, fair is not fast. Copy c is on older hardware, six times the cost per request. Round robin gives it a third of the requests. The work comes out four, four and twenty four.

## 6. A Strategy Of Our Own

Third, a strategy of our own. It sends each request to the copy with the least work so far. The slow copy gets one request. The work comes out six, five and six. It is registered for one service name only. The name catalogue still uses round robin.

## 7. A Copy Goes Down

Fourth, a copy goes down. It is still in the list, so a third of the requests are sent to it. Four of twelve fail. The balancer, without health checks, does not know.

## 8. A Retry Lands Elsewhere

Fifth, a retry. Allow each request one more attempt, and all twelve are answered, because the second attempt goes to the next copy. The retry is the caller's job. The balancer alone only spreads the failures.

## 9. Only For Names

Last, a trap. A balanced client treats every host as a service name. A name with no instances fails. So does a real address, because it is looked up as a name. For a real address, use an ordinary client.

## 10. The Verdict

My verdict, plainly. Use the default until work is uneven. Add retries or health checks, because a balancer alone spreads failures. And use service names, never addresses, on a balanced client.

## 11. How To Recognise It

How do you recognise this in code you did not write? A load balanced annotation on a client builder. And a URL whose host is a service name, not an address.

## 12. Where You Have Met This

You have met this in any Spring service that calls another by name.

## 13. What Was Used

For the record. Spring Boot four point one point one. Spring Cloud twenty twenty five point one point three. LoadBalancer five point zero point three.

## 14. What Is Real Here

The same honest admission as everywhere in this course. Everything is real: real sockets, real HTTP and the real balancer. Work is counted in cost units, never timed.

## 15. When This Is Too Much

So when is it too much? With one copy of a service, there is nothing to balance.

## 16. Thanks for Watching

That's Load Balancing with Spring Cloud LoadBalancer. If you take one sentence away, take this one: Spring Cloud LoadBalancer picks per request, and health and speed are still yours to add. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, change the cost of the slow copy to two, and rerun act three. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
