# Strangler Fig with NGINX Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. A customer asks the shop for the price of product SKU-1. The request goes to NGINX, the shop's only public address. NGINX's configuration has one rule, everything to the old shop, so its worker passes the request to the old shop, and the old shop is slow to answer. While that request is still open, the demo adds one rule to the configuration, prices to the new service, and tells NGINX to reload. NGINX's main process starts a new worker with the new rule, and tells the old worker to take nothing new and finish what it has. A second customer asks for the same price. The new worker takes it and passes it to the new service, which answers 1299 pence. Then the old shop answers the first request, 1299 pence as well, and the old worker hands it back and exits. Both customers got their price. Nobody saw a restart. From now on, prices come from the new service and everything else still comes from the old shop.

![Strangler Fig with NGINX sequence diagram](images/sequence-diagram.png)

The load-bearing sentence: **a reload changes which service answers the next request, never the request already in progress.**

For the regular expression that wins, the slash, the service that goes down and the cookie, see [`uml-diagram.md`](uml-diagram.md).
