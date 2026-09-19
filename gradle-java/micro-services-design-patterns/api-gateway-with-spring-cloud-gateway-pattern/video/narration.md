# API Gateway with Spring Cloud Gateway Pattern — Video Narration Script

## 1. API Gateway with Spring Cloud Gateway

Hello, and welcome. This video explains the API Gateway pattern with Spring Cloud Gateway, in Java, and it is written and presented by Jayasekhar Konduru. It is the framework version of the API Gateway video. That one put one gateway in front of catalogue, pricing, inventory and recommendations, so the mobile app made one call to one address and lost nothing when a feature service went down. This one shows the same idea inside Spring Cloud Gateway. The plain definition, in short: in Spring Cloud Gateway, a gateway is a routing table of paths and services, with filters applied to each request on the way through. By the end you will see a real gateway route real HTTP to four services, strip a prefix, check a token once, and time out a slow service, then see what it does not do: merge responses, and report a dead service as a 503.

## 2. The Partner Project

This video assumes the API Gateway video. If you have not seen it, start there. It puts one service in front of catalogue, pricing, inventory and recommendations, so the app makes one call, and it merges the four answers into one product page. This one uses the same example. It does not teach the pattern again. It shows what Spring Cloud Gateway does with it.

## 3. Before The First Line

Before the first line of code, what Spring Cloud Gateway is. Spring Cloud Gateway is a gateway built on Spring. You describe routes, a path and a destination, and filters, and it forwards real HTTP requests on a reactive server. And a promise: skipping this video loses none of the pattern. The hand-built one teaches all of it.

## 4. One Address, Four Services

First, one address. The client calls the gateway with four different paths, and each goes to a different service: catalogue, pricing, inventory and recommendations. The client knows one address. The routing table knows the rest. All of it is real HTTP over real sockets.

## 5. The Prefix Is Stripped

Second, the gateway rewrites. The client asked for slash api slash pricing slash products. The pricing service was asked for only slash products. The public prefix is gone, so the services never need to know about it. A header tells them the request came through the gateway.

## 6. One Token Check, For Every Route

Third, one token check. Without a token, the gateway answers four hundred and one, on any route. Zero requests reach a service. With a token, the request goes through. The check is written once. In the hand built version, each service repeated it.

## 7. One Service Down

Fourth, a service goes down. Recommendations answers with an error, and catalogue still works. The failure stays on its own route. But look at the status. It is five hundred, not five oh three. A refused connection is reported as an internal server error. To a client, that looks like a bug in the shop. Map it if the difference matters.

## 8. A Gateway Forwards

Fifth, what a gateway does not do. A product page that needs three services still takes three calls, and three reach the services. The gateway forwards. It does not merge. The partner video's gateway merged four answers into one page. Here that is a separate job, for code you write.

## 9. A Slow Service

Last, a slow service. Pricing never answers. After the timeout in the settings, the gateway answers for it with a five oh four, gateway timeout. The client is not left hanging. Set that timeout on every route.

## 10. The Verdict

My verdict, plainly. Use it for routing, authentication, headers and limits at the edge. Set a timeout on every route. Decide what a dead service looks like to clients. And compose responses somewhere else, or in a filter you write.

## 11. How To Recognise It

How do you recognise this in code you did not write? A route locator builder with route calls. Settings under spring cloud gateway. Or a global filter bean.

## 12. Where You Have Met This

You have met this at the public edge of most Spring based platforms.

## 13. What Was Used

For the record. Spring Boot four point one point one. Spring Cloud twenty twenty five point one point three. Gateway five point zero point three, on Netty.

## 14. What Is Real Here

The same honest admission as everywhere in this course. Everything is real: real sockets, real HTTP, and the real gateway. The four services are small JDK servers on free ports, and the slow one is held at a gate.

## 15. When This Is Too Much

So when is it too much? For one service, a gateway is a hop that adds nothing.

## 16. Thanks for Watching

That's API Gateway with Spring Cloud Gateway. If you take one sentence away, take this one: Spring Cloud Gateway routes and filters real requests, and composing them is still yours to write. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, map the five hundred for a refused connection to a five oh three. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
