# Distributed Tracing with Jaeger Pattern — Video Narration Script

## 1. Distributed Tracing with Jaeger

Hello, and welcome. This video explains the Distributed Tracing pattern in Java, using a real tracing library called OpenTelemetry, and a real trace collector called Jaeger. This video is presented by Jayasekhar Konduru. First, a simple definition. Distributed tracing gives one customer request one identifier. Every piece of work records how long it took, and which piece of work asked for it. Afterwards, those records are put back together into one story. Think of a hospital. At reception you get a wristband with a number on it. X-ray, the blood test and the consultant each write their own form, with your wristband number on it. At the end of the shift, the records office puts your afternoon back together, by that number. In our online store, one product page is built by two programs. By the end, you will hear a page split into two stories because one header was forgotten. A trace that arrives late, or not at all. A customer complaint with no trace to look at. And a clock that makes an answer arrive before its question.

## 2. The Scenario

Here is the scenario. The product page is the front door. It looks the product up in the catalog, asks pricing for a price, and checks the stock. Then it calls a second program, the recommendations service, over the network. And then it builds the page. Recommendations runs a ranking model, the slowest single piece of work on the page. Both are real web servers, in two separate Java programs. And the collector, Jaeger, runs in a container that the demo starts by itself. The plain Java version of this video kept everything inside one program. Here, nothing is shared except the network.

## 3. The Tools' Words

These tools bring a few words with them. One form, for one piece of work, is called a span. It has a name, a start time, a length, and the ID of the span that asked for it, called its parent. A span with no parent is the front door, and is called the root. The wristband number is called the trace ID. Every span of one customer request carries the same one. The wristband travels from one program to the next in a web header, called trace parent. It is fifty-five characters long. Writing it onto an outgoing request is called injecting. Reading it from an incoming one is called extracting. And Jaeger is the records office. It receives every service's spans, and joins them by trace ID.

## 4. A Hop That Forgets The Header

First demo: a hop that forgets the header. The product page calls recommendations over the network. But it leaves out the one line that writes the trace parent header. Nothing fails. Recommendations finds no header, so it starts a story of its own. Jaeger now holds two traces, for one page load. The page's trace has six spans. Its call to recommendations has nothing under it. The other trace has two spans: recommendations, and its ranking model, with no page above them. And each trace looks perfectly healthy. The two halves could only be found together by searching both services for a visit number the shop happened to record.

## 5. The Header Forwarded

Second demo: the header forwarded. One line is added. Write the current trace onto the outgoing request. The header the page sent, and the header recommendations received, are the same fifty-five characters. A version number. The trace ID. The caller's own span ID. And a flag that says: keep this one. Jaeger now holds one trace. Eight spans, from two services, with one root. Read as a family tree, the ranking model sits inside recommendations' span, which sits inside the page's call. By its own time, the slowest piece of work is the ranking model: three hundred and forty milliseconds or more. And the page's call lasted a little longer than recommendations took to answer. That difference is the network hop itself. You can only see it because both sides reported.

## 6. One Page Load, One Trace

So here is the shape of it. The product page does its own four steps, and records six spans. On its call to recommendations, it writes the trace parent header. Recommendations reads that header, joins the same trace, and records two spans of its own. Neither program ever holds the whole story. Each sends its own spans to Jaeger, separately. And Jaeger joins them by trace ID. The rule is short. Write the header on every call that leaves a program. Read it on every call that arrives.

## 7. The Collector Puts It Together, Later

Third demo: the collector puts it together, later. The customer already has the page. And at that moment, Jaeger holds none of its spans. OpenTelemetry does not send a span the moment it ends. It keeps finished spans in memory, and sends them together, in a batch, every five seconds. Sending each one as it finished would slow the shop down. So the spans arrive more than two seconds after the customer had the page. Then Jaeger holds eight: six sent by the product page, and two sent by recommendations. The customer never waits for tracing. That is the point. And nobody sees the trace straight away. That is the price.

## 8. Sampling At The Front Door

Fourth demo: sampling at the front door. Keeping every trace costs storage. So the page now keeps one trace in four. The decision is made once, at the front door. Twenty page loads. Six kept, and fourteen dropped. The decision travels in the last two characters of the header. Zero one means kept. Zero zero means dropped. Recommendations obeys the flag it is sent, and records spans for the same six. Jaeger holds six traces of the twenty. Now a customer complains about the first of those page loads. Jaeger has no trace of it, and never will. The decision was made at the only moment when nothing at all was known about that request.

## 9. A Clock That Is Off

Fifth demo: a clock that is off. Each program stamps its spans with its own machine's time. Now the recommendations machine's clock is set three seconds slow. The page's clock is right. The trace is complete. Eight spans, one root, and every parent link is correct. So the family tree is right. But in time order, the first span is recommendations' own. It starts two to three seconds before the call that caused it. An answer, before its question. Jaeger notices, and attaches a warning of its own. Clock skew adjustment is turned off. Out of the box, it stores what each service said, and corrects nothing.

## 10. The Bill

Sixth demo: the bill. Recommendations answers the customer. Then it is killed, before its next batch is sent. The page stops politely, which sends everything it holds. Jaeger holds six spans of that page load, all from the page. None from recommendations. Its spans were finished, correct, and waiting. And they never arrive. The spans a crash loses are always the last ones before it. Exactly the ones somebody will want, when they investigate the crash. And the ongoing costs. Eight spans for every page load, from two programs. A fifty-five character header on every hop. And Jaeger is one more system to run. Out of the box, it keeps everything in memory, so a restart empties it.

## 11. What The Simulation Left Out

So what did the plain Java version get right? The whole idea. Spans with parents, one trace ID, and the slowest step found by its own time. All of that holds with Jaeger. What it left out was the distance. In the plain version, the trace was an object passed along inside one program. Here, it has to become a header, cross the network, and be read by a different program. Spans are sent later, in batches. And every machine has its own clock. And the headline. In the plain version, a trace could never be lost. Here, a crash loses exactly the spans you would want to read about the crash.

## 12. The Verdict

So, here is the verdict. Put a collector behind your services, as soon as one customer request crosses more than one program. Then remember five things, because nothing will fail if you forget them. One. Write the header on every call that leaves a program, and read it on every call that arrives. Two. Sample once, at the front door, and let the decision travel. Three. Shut services down politely, so their last batch is sent. Four. Keep the machines' clocks in step. Five. Give the collector real storage, before you rely on it.

## 13. How To Recognise It

How can you spot this in code someone else wrote? Look for a call to inject, just before a web request is sent. And a call to extract, at the top of a request handler. That is the header being carried. A sampler described as parent based means: follow the decision in the header, instead of making a new one. And a batch span processor, with its delay, tells you how many seconds of spans a crash can lose. Where have you met this? Spring Boot, Quarkus and the OpenTelemetry Java agent all write and read this header for you.

## 14. What Is Real, And When Not

A quick, honest note about this demo. OpenTelemetry is version one point sixty-six. Jaeger is version two point twenty-one, in a container that the demo starts and removes by itself. The two services are separate Java programs, talking over real web requests. And everything the demo says about a trace is read back from Jaeger itself, which neither service can fake. You just need Docker switched on first. So, when is this too much? If the shop is one program, a profiler, or a request ID in the logs, answers the question without a collector to run. A collector earns its keep once one request crosses several programs, and somebody has to say which of them was slow.

## 15. Thanks for Watching

That's Distributed Tracing, with Jaeger. If you remember one sentence, make it this one. Give every request one trace ID, carry it across every hop, and remember that the trace arrives later, or not at all. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Shorten the batch delay to one second, run the crash again, and count how many spans arrive. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
