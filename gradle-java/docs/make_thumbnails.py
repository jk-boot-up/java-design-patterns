#!/usr/bin/env python3
"""Render `docs/thumbnail.png` for every pattern project.

Why this exists separately from `video/poster.png`: the poster is the
video's opening frame, so it is composed for a screen and carries the
before/after comparison, the arrow and the author credit. A thumbnail is
judged at about 360 pixels wide in a search result, and at that size the
comparison is a smudge. This renders a purpose-built 1280x720 image with
the same palette and branding but only three things on it -- the pattern
name, one line saying what it buys you, and one short piece of code -- each
set large enough to survive the shrink.

Both images stay in the repository. Upload this one as the thumbnail; the
poster remains what a viewer sees when the video starts.

Usage:
    python3 docs/make_thumbnails.py            # all projects
    python3 docs/make_thumbnails.py proxy      # one project
"""

import os
import sys

import matplotlib
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

W, H = 1280, 720  # YouTube's recommended thumbnail size, 16:9

TEXT = (226, 232, 240)
ACCENT = (167, 139, 250)
GREEN = (52, 211, 153)
GOLD = (251, 191, 36)
CYAN = (56, 189, 248)
TOP = (49, 16, 92)
BOTTOM = (10, 18, 58)
CODE_BG = (12, 18, 46)

FONT_DIR = os.path.join(os.path.dirname(matplotlib.__file__),
                        "mpl-data", "fonts", "ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
MONO_B = os.path.join(FONT_DIR, "DejaVuSansMono-Bold.ttf")

AUTHOR = "Jayasekhar Konduru"

# Per project: the name split across lines, the promise, and one short piece
# of code. The code is deliberately the *after* form only -- a thumbnail has
# no room to argue, so it shows the destination rather than the contrast.
# Everything here is kept short on purpose; anything longer stops being
# readable once YouTube scales the image down.
META = {
    "simple-factory": (["SIMPLE", "FACTORY"], "Let data choose the class",
                       "Factory.create(type)"),
    "static-factory": (["STATIC", "FACTORY"], "Give the constructor a name",
                       "Discount.percentage(10)"),
    "factory-method": (["FACTORY", "METHOD"], "One step, left to the subclass",
                       "createCourier()"),
    "abstract-factory": (["ABSTRACT", "FACTORY"],
                         "Choose the whole family at once",
                         "factory.taxRule()"),
    "builder": (["BUILDER"], "Decide it a piece at a time",
                ".addItem(x).build()"),
    "prototype": (["PROTOTYPE"], "Copy the one you already have",
                  "master.copy()"),
    "singleton": (["SINGLETON"], "Exactly one, actually enforced",
                  "enum INSTANCE"),
    "adapter": (["ADAPTER"], "One class translates, not every caller",
                "provider.quoteRate(...)"),
    "bridge": (["BRIDGE"], "Two hierarchies, varying independently",
               "new Notification(channel)"),
    "composite": (["COMPOSITE"], "One tree, one interface, zero instanceof",
                  "child.totalPrice()"),
    "decorator": (["DECORATOR"], "Wrap it, don't subclass it",
                  "new Insurance(gift)"),
    "facade": (["FACADE"], "One door in front of many",
               "facade.placeOrder(r)"),
    "flyweight": (["FLYWEIGHT"], "Stop paying for the same data twice",
                  "styleFor(SALE)"),
    "proxy": (["PROXY"], "Same interface, it controls the door",
              "new LazyProductImage(sku)"),
    "strategy": (["STRATEGY"], "Swap the rule, not the code",
                 "rule.costFor(shipment)"),
    "observer": (['OBSERVER'], "Tell everyone, know no one",
             "order.addListener(x)"),
    "command": (['COMMAND'], "Make the action an object",
            "history.undo()"),
    "template-method": (['TEMPLATE', 'METHOD'], "Fix the steps, vary the how",
                    "fulfil(order)"),
    "state": (['STATE'], "Behaviour follows the state",
          "order.cancel()"),
    "chain-of-responsibility": (['CHAIN OF', 'RESPONSIBILITY'], "Each link answers or passes it on",
                            "next.screen(request)"),
    "iterator": (['ITERATOR'], "Hide how the walk really works",
             "for (Product p : results)"),
    "mediator": (['MEDIATOR'], "Components talk through one hub",
             "hub.changed(field)"),
    "memento": (['MEMENTO'], "Snapshot it, restore it, safely",
            "cart.restore(saved)"),
    "visitor": (['VISITOR'], "New reports, untouched model",
            "node.accept(report)"),
    "interpreter": (['INTERPRETER'], "Turn a rule into a tree",
                "rule.matches(cart)"),
    "api-gateway": (['API', 'GATEWAY'], "One front door for the whole store",
                "gateway.productPage(sku)"),
    "service-discovery": (['SERVICE', 'DISCOVERY'],
                      "Ask where it is, don't hardcode it",
                      "registry.instancesOf(x)"),
    "load-balancing": (['LOAD', 'BALANCING'], "Spread the work, skip the sick one",
                   "balancer.choose(pool)"),
    "retry": (['RETRY'], "Try again, but only when it can help",
          "retrier.call(payment)"),
    "circuit-breaker": (['CIRCUIT', 'BREAKER'], "Stop calling what is already down",
                    "breaker.call(service)"),
    "bulkhead": (['BULKHEAD'], "One slow job cannot sink checkout",
             "bulkhead.submit(job)"),
    "database-per-service": (['DATABASE', 'PER SERVICE'],
                         "Your data is yours alone",
                         "orders.rowsFor(id)"),
    # Not "one join" — the whole premise is that the join is gone, which is why
    # somebody has to assemble the page by hand.
    "api-composition": (['API', 'COMPOSITION'], "One page, three services, no join",
                    "composer.pageFor(id)"),
    "cqrs": (['CQRS'], "Write one way, read another",
         "queries.historyFor(id)"),
    "saga": (['SAGA'], "No rollback, so undo it step by step",
         "saga.run(context)"),
    "transactional-outbox": (['TRANSACTIONAL', 'OUTBOX'],
                         "Save it and send it, or neither",
                         "outbox.add(message)"),
    "idempotent-consumer": (['IDEMPOTENT', 'CONSUMER'],
                        "Same message twice, one effect",
                        "seen(message.id())"),
    "externalised-configuration": (['EXTERNALISED', 'CONFIGURATION'],
                               "Change it without a deploy",
                               "settings.money(setting)"),
    "distributed-tracing": (['DISTRIBUTED', 'TRACING'],
                        "See where the time went",
                        "start(parent, \"pricing\")"),
    "backends-for-frontends": (['BACKENDS FOR', 'FRONTENDS'],
                           "One shape cannot serve two screens",
                           "phone.productScreen(sku)"),
    "sidecar": (['SIDECAR'], "Move it out, beside the service",
            "sidecar.send(payment)"),
    # The pair-mates carry the deployment in the promise line, because the
    # pattern name alone would make three thumbnails look identical.
    "sidecar-java-proxy": (['SIDECAR', 'JAVA PROXY'],
                       "Swap the proxy, not the service",
                       "forty lines of Java"),
    "sidecar-on-kubernetes": (['SIDECAR ON', 'KUBERNETES'],
                          "Two containers, one Pod",
                          "kubectl: 2/2"),
    "event-sourcing": (['EVENT', 'SOURCING'], "Store the facts, not the total",
                   "events.foldTo(balance)"),
    "strangler-fig": (['STRANGLER', 'FIG'], "One route at a time, no cutover",
                  "router.moveToNew(PRICING)"),
    # The architectural slugs lead with the rule each architecture enforces,
    # because four of the five share a domain and a feature, and only the rule
    # tells them apart at thumbnail size.
    "layered-architecture": (['LAYERED', 'ARCHITECTURE'],
                         "Folders are not a rule. A test is.",
                         "depend downward only"),
    "mvc": (['MVC'], "Two screens, one calculation",
        "model.total()"),
    "hexagonal-architecture": (['HEXAGONAL', 'ARCHITECTURE'],
                           "The core never learns it has a database",
                           "core names the port"),
    "clean-architecture": (['CLEAN', 'ARCHITECTURE'],
                       "The call goes out, the arrow points in",
                       "inward, always"),
    "clean-architecture-with-spring": (['CLEAN ARCHITECTURE', 'WITH SPRING'],
                                   "Same graph, wired by a container",
                                   "who calls new?"),
    "producer-consumer": (['PRODUCER', 'CONSUMER'],
                     "Orders arrive faster than they are packed",
                     "queue.put(order)"),
    "thread-pool": (['THREAD', 'POOL'],
                "A thread per order, until the server stops",
                "OutOfMemoryError"),
    "future-promise": (['FUTURE', 'PROMISE'],
                   "An answer you are promised but do not have yet",
                   "future.get()"),
    "read-write-lock": (['READ-WRITE', 'LOCK'],
                    "A thousand readers, one price change",
                    "readLock().lock()"),
    "monitor-object": (['MONITOR', 'OBJECT'],
                   "The object that guards its own state",
                   "synchronized decrement()"),
    "active-object": (['ACTIVE', 'OBJECT'],
                  "A call that returns before the work does",
                  "mailbox.offer(msg)"),
    "data-mapper": (["DATA", "MAPPER"],
                  "The object that does not know it is a row",
                  "mapper.insert(customer)"),
    "identity-map": (["IDENTITY", "MAP"],
                  "The same customer, loaded twice",
                  "map.get(customerId)"),
    "unit-of-work": (["UNIT OF", "WORK"],
                  "Save half an order and nothing else",
                  "work.commit()"),
    "lazy-load": (["LAZY", "LOAD"],
                  "Loading one order, getting the catalogue",
                  "order.lines()"),
    "repository": (["REPOSITORY", "PATTERN"],
                  "Query the collection, not the table",
                  "customers.findById(id)"),
    "service-layer": (["SERVICE", "LAYER"],
                  "Where does placing an order live?",
                  "orders.place(request)"),
    "dto": (["DATA TRANSFER", "OBJECT"],
                  "The object that crosses the boundary",
                  "new CustomerDto(customer)"),
    "identity-map-with-jpa": (["IDENTITY MAP", "WITH JPA"],
                  "The persistence context is the map",
                  "em.find(Customer.class, id)"),
    "unit-of-work-with-spring": (["UNIT OF WORK", "WITH SPRING"],
                  "The flush you did not write",
                  "@Transactional"),
    "lazy-load-with-hibernate": (["LAZY LOAD", "WITH HIBERNATE"],
                  "The exception everybody has met",
                  "LazyInitializationException"),
    "repository-with-spring-data": (["REPOSITORY", "SPRING DATA"],
                  "An interface with no implementation",
                  "interface CustomerRepository"),
    "null-object": (["NULL", "OBJECT"],
                  "The discount that is not there",
                  "NoDiscount.apply(price)"),
    "object-pool": (["OBJECT", "POOL"],
                  "Expensive to make, cheap to borrow",
                  "pool.borrow()"),
    "registry": (["REGISTRY", "PATTERN"],
                  "The well-known place everything is kept",
                  "Registry.get(PaymentGateway.class)"),
    "service-locator": (["SERVICE", "LOCATOR"],
                  "Ask a middleman for what you need",
                  "locator.find(Notifier.class)"),
    "dependency-injection": (["DEPENDENCY", "INJECTION"],
                  "Stop asking; be given",
                  "new CheckoutService(policy, gateway)"),
    "dependency-injection-with-spring": (["DEPENDENCY INJECTION", "WITH SPRING"],
                  "The same graph, wired by a container",
                  "@Component"),
    "registry-with-spring": (["REGISTRY", "WITH SPRING"],
                  "The context is a registry you did not write",
                  "ctx.getBean(Gateway.class)"),
    "object-pool-with-hikaricp": (["OBJECT POOL", "WITH HIKARICP"],
                  "The mature answer to leaks and dirty state",
                  "dataSource.getConnection()"),
    "service-locator-with-consul": (["SERVICE LOCATOR", "WITH CONSUL"],
                  "Real service discovery, and its stale cache",
                  "consul.find(\"payment-gateway\")"),
    "thread-pool-with-spring": (["THREAD POOL", "WITH SPRING"],
                  "@Async, and the pool behind it",
                  "@Async"),
    "future-promise-with-spring": (["FUTURE PROMISE", "WITH SPRING"],
                  "CompletableFuture through @Async",
                  "@Async CompletableFuture"),
    "active-object-with-spring": (["ACTIVE OBJECT", "WITH SPRING"],
                  "A single-thread executor as a mailbox",
                  "@Async single thread"),
    "singleton-with-spring": (["SINGLETON", "WITH SPRING"],
                  "A singleton the container owns",
                  "@Scope singleton"),
    "prototype-with-spring": (["PROTOTYPE", "WITH SPRING"],
                  "A prototype bean inside a singleton",
                  "@Scope prototype"),
    "proxy-with-spring": (["PROXY", "WITH SPRING"],
                  "Spring AOP and the call that bypasses it",
                  "@Transactional proxy"),
    "observer-with-spring": (["OBSERVER", "WITH SPRING"],
                  "ApplicationEvent and @EventListener",
                  "@EventListener"),
    "strategy-with-spring": (["STRATEGY", "WITH SPRING"],
                  "Strategies as beans, chosen by name",
                  "Map<String, Strategy>"),
    "template-method-with-spring": (["TEMPLATE METHOD", "WITH SPRING"],
                  "JdbcTemplate is the pattern",
                  "jdbcTemplate.query"),
    "chain-of-responsibility-with-spring": (["CHAIN OF", "RESPONSIBILITY"],
                  "Servlet filters, in order",
                  "OncePerRequestFilter"),
    "interpreter-with-spel": (["INTERPRETER", "WITH SPEL"],
                  "An expression language you did not write",
                  "parser.parseExpression"),
    "circuit-breaker-with-resilience4j": (["CIRCUIT BREAKER", "RESILIENCE4J"],
                  "The real library, and its defaults",
                  "@CircuitBreaker"),
    "retry-with-resilience4j": (["RETRY", "RESILIENCE4J"],
                  "Backoff, jitter, and annotation order",
                  "@Retry"),
    "bulkhead-with-resilience4j": (["BULKHEAD", "RESILIENCE4J"],
                  "Semaphore and thread-pool bulkheads",
                  "@Bulkhead"),
    "api-gateway-with-spring-cloud-gateway": (["API GATEWAY", "SPRING CLOUD"],
                  "A real gateway, routes and filters",
                  "RouteLocator"),
    "load-balancing-with-spring-cloud-loadbalancer": (["LOAD BALANCING", "SPRING CLOUD"],
                  "Client-side balancing, and its cache",
                  "@LoadBalanced"),
    "layered-architecture-with-spring-boot": (["LAYERED", "WITH SPRING BOOT"],
                  "Real layers, enforced by a test",
                  "@RestController"),
    "mvc-with-spring-mvc": (["MVC", "WITH SPRING MVC"],
                  "A controller, a model, a view",
                  "@Controller"),
    "hexagonal-architecture-with-spring-boot": (["HEXAGONAL", "WITH SPRING BOOT"],
                  "Ports, adapters and the wiring",
                  "@Configuration"),
}

GROUP = {
    "simple-factory": "creational", "static-factory": "creational",
    "factory-method": "creational", "abstract-factory": "creational",
    "builder": "creational", "prototype": "creational",
    "singleton": "creational",
    "adapter": "structural", "bridge": "structural",
    "composite": "structural", "decorator": "structural",
    "facade": "structural", "flyweight": "structural", "proxy": "structural",
    "strategy": "behavioural",
    "observer": "behavioural",
    "command": "behavioural",
    "template-method": "behavioural",
    "state": "behavioural",
    "chain-of-responsibility": "behavioural",
    "iterator": "behavioural",
    "mediator": "behavioural",
    "memento": "behavioural",
    "visitor": "behavioural",
    "interpreter": "behavioural",
}

# The microservices projects all live in one directory, and there are twelve of
# them, so listing each by hand above would be twelve lines saying the same
# thing.
GROUP.update({slug: "micro-services-design-patterns" for slug in (
    "api-gateway", "service-discovery", "load-balancing", "retry",
    "circuit-breaker", "bulkhead", "database-per-service", "api-composition",
    "cqrs", "saga", "transactional-outbox", "idempotent-consumer")})

# The platform projects likewise share one directory, and Sidecar accounts for
# three of the eight slugs.
GROUP.update({slug: "platform-design-patterns" for slug in (
    "externalised-configuration", "distributed-tracing",
    "backends-for-frontends", "sidecar", "sidecar-java-proxy",
    "sidecar-on-kubernetes", "event-sourcing", "strangler-fig")})

# The architectural projects share one directory too, and Clean Architecture
# accounts for two of the five slugs.
GROUP.update({slug: "architectural-design-patterns" for slug in (
    "layered-architecture", "mvc", "hexagonal-architecture",
    "clean-architecture", "clean-architecture-with-spring")})

GROUP.update({slug: "concurrency-design-patterns" for slug in (
    "producer-consumer", "thread-pool", "future-promise",
    "read-write-lock", "monitor-object", "active-object")})

GROUP.update({slug: "foundational-design-patterns" for slug in (
    "dependency-injection-with-spring",
    "registry-with-spring",
    "object-pool-with-hikaricp",
    "service-locator-with-consul",

    "null-object",
    "object-pool",
    "registry",
    "service-locator",
    "dependency-injection",
    )})

GROUP.update({slug: "enterprise-design-patterns" for slug in (
    "data-mapper",
    "identity-map",
    "unit-of-work",
    "lazy-load",
    "repository",
    "service-layer",
    "dto",
    "identity-map-with-jpa",
    "unit-of-work-with-spring",
    "lazy-load-with-hibernate",
    "repository-with-spring-data",
    )})


GROUP.update({slug: "concurrency-design-patterns" for slug in (
    "thread-pool-with-spring",
    "future-promise-with-spring",
    "active-object-with-spring",
    )})

GROUP.update({slug: "creational" for slug in (
    "singleton-with-spring",
    "prototype-with-spring",
    )})

GROUP.update({slug: "structural" for slug in (
    "proxy-with-spring",
    )})

GROUP.update({slug: "behavioural" for slug in (
    "observer-with-spring",
    "strategy-with-spring",
    "template-method-with-spring",
    "chain-of-responsibility-with-spring",
    "interpreter-with-spel",
    )})

GROUP.update({slug: "micro-services-design-patterns" for slug in (
    "circuit-breaker-with-resilience4j",
    "retry-with-resilience4j",
    "bulkhead-with-resilience4j",
    "api-gateway-with-spring-cloud-gateway",
    "load-balancing-with-spring-cloud-loadbalancer",
    )})

GROUP.update({slug: "architectural-design-patterns" for slug in (
    "layered-architecture-with-spring-boot",
    "mvc-with-spring-mvc",
    "hexagonal-architecture-with-spring-boot",
    )})


def f(path, size):
    return ImageFont.truetype(path, size)


def fit(path, text, max_width, start):
    """Largest font size at which `text` still fits `max_width`."""
    size = start
    while size > 12 and f(path, size).getlength(text) > max_width:
        size -= 2
    return f(path, size)


def gradient(img):
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)],
               fill=tuple(int(a + (b - a) * t) for a, b in zip(TOP, BOTTOM)))


def render(slug):
    names, promise, code = META[slug]
    img = Image.new("RGB", (W, H), BOTTOM)
    gradient(img)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, W, 10], fill=GOLD)

    d.text((64, 46), "JAVA  ·  DESIGN PATTERNS", font=f(SANS_B, 26), fill=GOLD)

    # The name is the one thing that has to be legible at any size, so it is
    # grown until the widest of its lines fills the frame. A one-word name
    # like PROXY therefore ends up far bigger than a two-line one, which is
    # the point -- the space is there, and dead space below the text is what
    # makes a thumbnail look unfinished.
    pattern_font = f(SANS_B, 64)
    promise_font = fit(SANS_B, promise, W - 128, 44)
    code_font = fit(MONO_B, code, W - 200, 38)

    # Everything below the name has a known height, so the name gets what is
    # left. Fitting it to the frame width alone is not enough -- a two-line
    # name sized to the width would run off the bottom and collide with the
    # author credit -- so it is capped by the vertical budget as well.
    below = (pattern_font.size + 24 + 8 + 40
             + promise_font.size + 26 + code_font.size + 34)
    per_line = (H - 110 - 130 - below) // len(names) - 6
    widest = max(names, key=len)
    name_font = f(SANS_B, min(fit(SANS_B, widest, W - 128, 190).size,
                              per_line))

    block_h = len(names) * (name_font.size + 6) + below
    y = max(110, (H - block_h) // 2 + 20)

    for line in names:
        d.text((64, y), line, font=name_font, fill=TEXT)
        y += name_font.size + 6
    d.text((64, y), "PATTERN", font=pattern_font, fill=ACCENT)
    y += pattern_font.size + 24

    d.rectangle([64, y, 260, y + 8], fill=GREEN)
    y += 40

    d.text((64, y), promise, font=promise_font, fill=TEXT)
    y += promise_font.size + 26

    box_w = int(code_font.getlength(code)) + 56
    d.rounded_rectangle([64, y, 64 + box_w, y + code_font.size + 34],
                        radius=14, fill=CODE_BG, outline=GREEN, width=4)
    d.text((92, y + 14), code, font=code_font, fill=GREEN)

    # Author credit, bottom right, out of the way of the name.
    af = f(SANS_B, 28)
    aw = int(af.getlength(AUTHOR)) + 44
    d.rounded_rectangle([W - 64 - aw, H - 86, W - 64, H - 32],
                        radius=27, outline=CYAN, width=3)
    d.text((W - 64 - aw // 2, H - 74), AUTHOR, font=af, fill=CYAN, anchor="ma")

    out = os.path.join(ROOT, GROUP[slug], slug + "-pattern",
                       "docs", "thumbnail.png")
    img.save(out, optimize=True)
    kb = os.path.getsize(out) // 1024
    print("wrote %s  (%dx%d, %d KB)"
          % (os.path.relpath(out, ROOT), W, H, kb))


def main():
    wanted = sys.argv[1:]
    for slug in META:
        if wanted and slug not in wanted:
            continue
        # META covers the whole series, including projects not built yet.
        if not os.path.isdir(os.path.join(ROOT, GROUP[slug],
                                          slug + "-pattern")):
            if wanted:
                print("%s: not built yet - skipped" % slug)
            continue
        render(slug)


if __name__ == "__main__":
    main()
