# Distributed Tracing with Jaeger Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. A customer asks the product page for product A-2231. The customer sends no trace header, so the product page starts a new trace: it is the front door. Its sampler decides to keep this trace. The page does its own work — catalog, pricing, inventory — each a span whose parent is the page's span. Then it calls the recommendations service, a separate program, over HTTP. Before the call leaves, the page writes one header, traceparent, holding the trace id and the id of the page's calling span, and the flag 01, meaning kept. Recommendations reads that header and opens its own span with the page's call as its parent, and runs the ranking model inside it. It answers. The page renders, and the customer has the page. At that moment Jaeger holds nothing. A few seconds later, each service sends its own batch of finished spans to Jaeger: two from recommendations, six from the page. Jaeger joins the eight by their shared trace id into one trace, with one root. The demo asks Jaeger's query API for that trace, and reads back the tree.

![Distributed Tracing with Jaeger sequence diagram](images/sequence-diagram.png)

The load-bearing sentence: **the trace is never in one place until Jaeger joins it; each service only ever sends its own spans, and only the header ties them together.**

For the forgotten header, the late batch and the crash, and the slow clock, see [`uml-diagram.md`](uml-diagram.md).
