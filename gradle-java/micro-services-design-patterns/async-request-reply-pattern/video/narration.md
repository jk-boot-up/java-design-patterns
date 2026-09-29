# Asynchronous Request-Reply Pattern — Video Narration Script

## 1. Asynchronous Request-Reply

Hello, and welcome. This video explains the Asynchronous Request Reply pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. When a job takes longer than a caller can wait, the server accepts the request straight away. It hands back a link where the caller can check on the job. And when the job is done, that link leads to the result. Think of a dry cleaner. You do not stand at the counter while your coat is cleaned. You get a ticket, and you are told to come back on Thursday. On Thursday, you show the ticket, and collect the coat. In this video, the domain is an online shop. Sellers in the shop can ask for a monthly sales report. Building it takes about six seconds. By the end, you will hear why a slow job fails behind a normal request, even when it succeeds. What the answers two oh two and three oh three mean. How to stop a double click doing the work twice. And what the pattern costs.

## 2. The Scenario

Here is the scenario. A seller asks for this month's sales report. The shop adds up every order, which takes about six seconds. In front of the shop sits a gateway. A gateway is the front door that every request passes through. To protect the shop, it gives up on any request that takes longer than three seconds. Six seconds of work, and three seconds of patience. What happens?

## 3. Act One — Waiting for a slow report

First demo: waiting for a slow report. A seller asks for this month's sales report. Building it takes six seconds. But the gateway in front of the store gives up after three seconds. It answers five oh four, which means gateway timeout. The seller clicks again. Another five oh four. Meanwhile, the server never knew the seller had gone. It built the report both times. Built twice. Received, zero times.

## 4. Act Two — Accepted at once

Second demo: accepted at once. Now the seller's request gets an answer straight away. Two oh two, accepted. The answer means: I have your request, and I am working on it. It carries two things. A status link, like a ticket number. And a hint: check again in two seconds. The report is built in the background. Nothing is left waiting, so nothing times out.

## 5. Act Three — Check back, then fetch

Third demo: check back, then fetch. The seller's page waits two seconds, as it was told. Then it checks the status link. Running, thirty-three percent. Two seconds later: running, sixty-six percent. At six seconds, the status link answers three oh three, see other. That means: it is done, and the result is over here. The page follows the link, and gets the report. Four hundred and twelve orders, eighteen thousand, two hundred and forty pounds fifty.

## 6. Act Four — Asking twice

Fourth demo: the seller clicks twice. Each request carries a key, a short name for what is being asked. Here, seller seven, September. The server remembers which job each key started. So the second click gets the same status link, R 1. No second job is started. The report is built exactly once.

## 7. Act Five — The bill

Fifth demo: the bill. One report now takes five requests, instead of one. A submit, three status checks, and a fetch. And the client must behave. An impatient client that checks every tenth of a second sends sixty-two requests, for the same report. The server also has to remember every job, and its result, until someone collects it.

## 8. The Pattern

Let's name the pattern. The server has three addresses. One: submit. It answers two oh two, accepted, with a status link, straight away. Two: the status link. It answers running, with how far along the job is, and when to check again. When the job is done, it answers three oh three, see other, pointing at the result. Three: the result itself. And every request carries a key, so asking twice does the work only once.

## 9. Who Does What

Here is who does what. The async report API has the three methods: submit, status, and fetch. It keeps a list of jobs, and which key started each one. The polling client is the caller's side. It submits, waits as long as it was told, checks the status, and follows the link to the result. The report builder is the slow work. And the sync report API is the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern already. Any API that answers two oh two accepted, with a location header, is using it. A retry after header is the hint for when to check again. Cloud providers use it for slow jobs, such as starting a virtual machine. And whenever a website says your export is being prepared, and shows it later, that is this pattern.

## 11. When To Use It

So, when should you use it? Use it for any work behind an API that can take longer than a few seconds. Reports, exports, video processing. Give each request a key, so a repeat does not start the work again. Send a retry hint, so clients check at a sensible pace. And when the server can call the client back, for example with a webhook, do that instead of polling.

## 12. Thanks for Watching

That's the Asynchronous Request Reply pattern. If you remember one sentence, make it this one. For slow work, give the caller a ticket, and let them come back for the result. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a failed state, so the status link can say why a report could not be built. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
