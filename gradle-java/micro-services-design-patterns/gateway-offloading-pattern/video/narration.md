# Gateway Offloading Pattern — Video Narration Script

## 1. Gateway Offloading

Hello, and welcome. This video explains the Gateway Offloading pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Many services need the same chores done on every request. Checking who the caller is. Stopping callers who send too much. Compressing the answer. Gateway offloading moves those chores into the gateway in front of the services. So they are done once, the same way for everyone. Think of an office building with a reception desk. Visitors sign in once, at the front door. The teams upstairs do not each check passports at their own door. In this video, the domain is an online shop, with three services. Catalog, cart, and orders. By the end, you will hear how three copies of a sign-in check drifted apart. How the gateway takes over sign-in, rate limits and compression. And why there must be no side door.

## 2. The Scenario

Here is the scenario. The shop has three services. Catalog, cart and orders. Each one checked the customer's sign-in token itself, with its own copy of the code. The orders team's copy forgot to check whether the token had expired.

## 3. Act One — Every service checks for itself

First demo: every service checks the sign-in token itself. The customer's token expired a minute ago. The catalog service refuses it. The cart service refuses it. But the orders service lets the customer in. The orders team's copy of the check forgot about expiry. Three copies of the same check, and one of them is wrong.

## 4. Act Two — One check, at the gateway

Second demo: the gateway checks the token, once. Every request passes through the gateway first. The expired token is refused for all three services. The same way, every time. A valid token gets through. The gateway tells the orders service who the customer is. The services hold no sign-in code at all.

## 5. Act Three — Rate limiting

Third demo: rate limiting. The gateway allows each customer five requests a second. A customer sends eight requests in one second. Five pass. Three are refused, with too many requests. The orders service only ever sees five. And no service had to write a rate limiter.

## 6. Act Four — Compression

Fourth demo: compression. The catalog page is about ten thousand bytes. The gateway compresses it, for every browser that accepts compression. It shrinks to under a fifth of its size. One compressor at the gateway. Not one in every service.

## 7. Act Five — The bill

Fifth demo: the bill. The services now trust whatever the gateway tells them. So a call that skips the gateway, and goes straight to the orders service claiming to be another customer, is accepted. The services must only be reachable through the gateway. And everything goes through one place. If the gateway fails, or slows down, every page does.

## 8. The Pattern

Let's name the pattern. The chores every service needs move into the gateway. Checking sign-in. Limiting how often each customer can call. Compressing responses. The services keep only their own business.

## 9. Who Does What

Here is who does what. The gateway does four steps, in order. Check sign-in. Check the rate limit. Route the request, saying who the customer is. And compress the answer. The shop services just do their own job. The self-checking service is the old way, with its own copy of the check.

## 10. Where You Have Seen It

You have probably met this pattern already. Gateways such as Kong, NGINX, and Envoy have plugins for sign-in checks and rate limits. Cloud gateways, and Spring Cloud Gateway, do the same. And a load balancer that handles encryption is offloading too.

## 11. When To Use It

So, when should you use it? When many services need exactly the same chores. Keep business rules out of the gateway. Make sure nobody can reach the services around it. And run the gateway as the critical piece it now is.

## 12. Thanks for Watching

That's the Gateway Offloading pattern. If you remember one sentence, make it this one. Do the shared chores once, at the door. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Make the services refuse any call without a secret that only the gateway adds. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
