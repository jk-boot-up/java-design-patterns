# Problem Statement

## The scenario

The shop is being rebuilt. The old shop is one program that does everything: it shows prices and stock, keeps each customer's basket, takes the checkout and lists past orders. A team is writing its replacement, the new service, and so far it has built prices and checkout. The shop cannot stop trading while the rewrite happens, and nobody wants a weekend where everything changes at once.

## The naive version

The big bang: when the new service is "ready", send every request to it at once. On the Monday, only what the new service has already built works.

```
  the four pages: prices 200, stock 404, basket 404, orders 404. pages that work: 1 of 4 (0 from the old shop, 1 from the new service).
```

## What the twin project already did

The plain-Java Strangler Fig project in this course put a router in front of both systems, with one switch per capability: pricing, stock, payment and email. Every switch started on the old system. Moving one capability was one switch; moving it back was the same switch. It compared the two sides' answers before moving anything, rolled one capability back without touching the others, and counted the cost of a migration that stalls half-finished. It is a complete teaching of the idea and nothing here replaces it.

It had one comfort, though. The router was a Java object, and a switch was a field. There were no rules about which switch won, no path to rewrite, no moment of changing over, and the two sides could not be down separately, because they lived in one program.

## What this project must deliver

The same shop, the same prices in pence, with the router replaced by a real NGINX that the demo starts in a container and stops at the end, in front of two real HTTP services. The big bang failing on the pages the new service has not built. One route moved by a configuration change and a reload, with the old shop still serving the rest, and a request already in progress finishing on the old configuration. An old rule in the configuration quietly cancelling a move, and one character fixing it. One slash changing the path the new service receives. The new service down, giving 502 on its route alone, and a rollback that is one reload. And an honest bill: a cookie the old shop set that the new service cannot use, and three things to run instead of one.

Every figure printed is the program's own, and two runs back to back print the same thing.
