# Micro-Frontends Pattern — Video Narration Script

## 1. Micro-Frontends

Hello, and welcome. This video explains the Micro-Frontends pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. With micro-frontends, a web page is split into parts, and each part belongs to one team. Each team builds and releases its part on its own. The page is assembled from those parts, with a fallback when one fails. Think of a newspaper. The sport, business, and weather desks each write their own pages. The printers put the paper together from whatever arrives. If the weather desk is late, the paper still goes out, with a note in the weather box. In this video, the domain is an online shop. Its product page shows the product, a small basket summary, and recommendations, built by three teams. By the end, you will hear why one front-end for many teams fails as a whole. How a page is assembled from team parts. How failures stay in their slot. And what it costs.

## 2. The Scenario

Here is the scenario. The product page shows the product details, a small basket summary, and recommendations. Three teams work on it. But it was one front-end application. Built together, released together, and failing together.

## 3. Act One — One front-end for everything

First demo: one front-end renders the whole product page. The product details, the basket summary, and the recommendations. Three teams, one application. The recommendations team ships a bug. The whole page fails. Including the parts that had nothing wrong with them. And to fix it, everyone's code must be released together.

## 4. Act Two — Each team serves its part

Second demo: micro-frontends. Each team now runs its own small web application. It serves only that team's part of the page. The page itself is a layout with three slots. Product, basket, and recommendations. Each slot is filled by asking the team that owns it. The page looks exactly as before.

## 5. Act Three — Failure stays in its slot

Third demo: one team's failure stays in its slot. The recommendations app fails. The page still shows the product and the basket. The recommendations slot says: unavailable. Then the recommendations app is slow. After three hundred milliseconds, the page stops waiting for it. Same result: the rest of the page is served.

## 6. Act Four — Independent releases

Fourth demo: each team releases on its own. The basket team releases version two. It now says: free delivery over forty pounds. The very next page view shows it. The product and recommendations apps were not touched.

## 7. Act Five — The bill

Fifth demo: the bill. One page view is now one page, and three fragment requests. The slowest fragment sets the pace. And teams drift apart. The product team starts writing thirty point zero zero G B P. The basket team writes pounds and pence. The page looks like two different shops.

## 8. The Pattern

Let's name the pattern. The page becomes a layout with slots. Each slot belongs to one team. It is filled by that team's own small application. And each slot has a time limit and a fallback, so one team's problem never takes down the page.

## 9. Who Does What

Here is who does what. The page assembler holds the layout, fetches every slot at once, and fills in fallbacks. A team app is one team's small server. It serves only that team's fragment, and is released by that team. And one front-end is the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern already. Server-side includes, and edge-side includes on content delivery networks, assemble pages from parts. In the browser, tools such as Module Federation and single-spa do it. And many large shops and news sites give each team its own part of the page.

## 11. When To Use It

So, when should you use it? When several independent teams keep blocking each other's front-end releases. Give every fragment a time limit and a fallback. Share a design system, so the page still looks like one shop. And when one team owns the page, keep one front-end.

## 12. Thanks for Watching

That's the Micro-Frontends pattern. If you remember one sentence, make it this one. Each team owns its part of the page, and one part failing never takes down the rest. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a reviews slot, owned by a new team. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
