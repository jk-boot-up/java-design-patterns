#!/usr/bin/env python3
"""Write `docs/spec.md` and `docs/spec.html` for every pattern project.

Each project gets one specification: what it teaches, what its code has to
be true of, and the quality bar its video and its YouTube publication have to
meet.

Why this is generated rather than fourteen hand-written files. Roughly half of
each spec -- the video pipeline, the poster and thumbnail rules, the
publishing requirements, the conformance checklist -- is identical across all
fourteen projects by design, because thirteen of the build scripts are
generated from abstract factory's. Hand-maintaining fourteen copies of that
guarantees they drift, and a spec that disagrees with the pipeline is worse
than no spec. The per-project half lives in `META` below, and every number in
the shared half (runtime, scene count, loudness, test count) is read from the
project's own files at generation time rather than typed in.

The HTML is rendered from the Markdown by the same run, for the same reason:
two hand-maintained copies of one document drift, and the stale one is always
the one somebody reads.

Usage:
    python3 docs/make_specs.py                  # all projects
    python3 docs/make_specs.py proxy builder    # named projects
    python3 docs/make_specs.py --no-measure     # skip the ffmpeg loudness pass
"""

import base64
import html
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Learning order. The end screen of each video points at the next one.
ORDER = [
    ("creational", "simple-factory"),
    ("creational", "static-factory"),
    ("creational", "factory-method"),
    ("creational", "abstract-factory"),
    ("creational", "builder"),
    ("creational", "prototype"),
    ("creational", "singleton"),
    ("structural", "adapter"),
    ("structural", "bridge"),
    ("structural", "composite"),
    ("structural", "decorator"),
    ("structural", "facade"),
    ("structural", "flyweight"),
    ("structural", "proxy"),
    ("behavioural", "strategy"),
    ("behavioural", "observer"),
    ("behavioural", "command"),
    ("behavioural", "template-method"),
    ("behavioural", "state"),
    ("behavioural", "chain-of-responsibility"),
    ("behavioural", "iterator"),
    ("behavioural", "mediator"),
    ("behavioural", "memento"),
    ("behavioural", "visitor"),
    ("behavioural", "interpreter"),
    # The microservices category. Its directory name is the long one, and the
    # group string is used verbatim as the directory, so it stays spelled out.
    ("micro-services-design-patterns", "api-gateway"),
    ("micro-services-design-patterns", "service-discovery"),
    ("micro-services-design-patterns", "load-balancing"),
    ("micro-services-design-patterns", "retry"),
    ("micro-services-design-patterns", "circuit-breaker"),
    ("micro-services-design-patterns", "bulkhead"),
    ("micro-services-design-patterns", "database-per-service"),
    ("micro-services-design-patterns", "api-composition"),
    ("micro-services-design-patterns", "cqrs"),
    ("micro-services-design-patterns", "saga"),
    ("micro-services-design-patterns", "transactional-outbox"),
    ("micro-services-design-patterns", "idempotent-consumer"),
    # The platform category. Six patterns across eight projects: Sidecar is
    # taught three times, once per deployment choice, and each version is a
    # project of its own. Build order is not learning order -- event-sourcing
    # goes first as the category's reference project.
    ("platform-design-patterns", "externalised-configuration"),
    ("platform-design-patterns", "distributed-tracing"),
    ("platform-design-patterns", "backends-for-frontends"),
    ("platform-design-patterns", "sidecar"),
    ("platform-design-patterns", "sidecar-java-proxy"),
    ("platform-design-patterns", "sidecar-on-kubernetes"),
    ("platform-design-patterns", "event-sourcing"),
    ("platform-design-patterns", "strangler-fig"),
    # The architectural category. Four architectures across five projects:
    # Clean Architecture is taught twice, once wired by hand and once wired by
    # Spring, and each version is a project of its own. The order here is the
    # learning order, because each project is one step from the one before it.
    ("architectural-design-patterns", "layered-architecture"),
    ("architectural-design-patterns", "mvc"),
    ("architectural-design-patterns", "hexagonal-architecture"),
    ("architectural-design-patterns", "clean-architecture"),
    ("architectural-design-patterns", "clean-architecture-with-spring"),
    # The concurrency category. Six patterns in a dependency order: the queue
    # (producer-consumer), what consumes it (thread pool), how a caller gets
    # an answer back (future/promise), the two ways shared state is protected
    # (read-write lock, monitor object), and the capstone that assembles all
    # four (active object).
    ("concurrency-design-patterns", "producer-consumer"),
    ("concurrency-design-patterns", "thread-pool"),
    ("concurrency-design-patterns", "future-promise"),
    ("concurrency-design-patterns", "read-write-lock"),
    ("concurrency-design-patterns", "monitor-object"),
    ("concurrency-design-patterns", "active-object"),
    # The enterprise category. Fowler's dependency order: seven patterns by
    # hand, and the four that get a framework project of their own.
    ("enterprise-design-patterns", "data-mapper"),
    ("enterprise-design-patterns", "identity-map"),
    ("enterprise-design-patterns", "unit-of-work"),
    ("enterprise-design-patterns", "lazy-load"),
    ("enterprise-design-patterns", "repository"),
    ("enterprise-design-patterns", "service-layer"),
    ("enterprise-design-patterns", "dto"),
    ("enterprise-design-patterns", "identity-map-with-jpa"),
    ("enterprise-design-patterns", "unit-of-work-with-spring"),
    ("enterprise-design-patterns", "lazy-load-with-hibernate"),
    ("enterprise-design-patterns", "repository-with-spring-data"),
    # The foundational category: how an object gets hold of another, and what
    # happens when there is not one. The last three are one argument in three moves.
    ("foundational-design-patterns", "null-object"),
    ("foundational-design-patterns", "object-pool"),
    ("foundational-design-patterns", "registry"),
    ("foundational-design-patterns", "service-locator"),
    ("foundational-design-patterns", "dependency-injection"),
    ("foundational-design-patterns", "dependency-injection-with-spring"),
    ("foundational-design-patterns", "registry-with-spring"),
    ("foundational-design-patterns", "object-pool-with-hikaricp"),
    ("foundational-design-patterns", "service-locator-with-consul"),
    # Framework versions of patterns from the earlier categories, each its own project.
    ("concurrency-design-patterns", "thread-pool-with-spring"),
    ("concurrency-design-patterns", "future-promise-with-spring"),
    ("concurrency-design-patterns", "active-object-with-spring"),
    ("creational", "singleton-with-spring"),
    ("creational", "prototype-with-spring"),
    ("structural", "proxy-with-spring"),
    ("behavioural", "observer-with-spring"),
    ("behavioural", "strategy-with-spring"),
    ("behavioural", "template-method-with-spring"),
    ("behavioural", "chain-of-responsibility-with-spring"),
    ("behavioural", "interpreter-with-spel"),
    ("micro-services-design-patterns", "circuit-breaker-with-resilience4j"),
    ("micro-services-design-patterns", "retry-with-resilience4j"),
    ("micro-services-design-patterns", "bulkhead-with-resilience4j"),
    ("micro-services-design-patterns", "api-gateway-with-spring-cloud-gateway"),
    ("micro-services-design-patterns", "load-balancing-with-spring-cloud-loadbalancer"),
    ("micro-services-design-patterns", "service-discovery-with-spring-cloud-consul"),
    ("domain-driven-design-patterns", "value-object"),
    ("domain-driven-design-patterns", "aggregate"),
    ("domain-driven-design-patterns", "domain-event"),
    ("domain-driven-design-patterns", "specification"),
    ("domain-driven-design-patterns", "anti-corruption-layer"),
    ("architectural-design-patterns", "layered-architecture-with-spring-boot"),
    ("architectural-design-patterns", "mvc-with-spring-mvc"),
    ("architectural-design-patterns", "hexagonal-architecture-with-spring-boot"),
    ("domain-driven-design-patterns", "bounded-context"),
    ("enterprise-design-patterns", "transaction-script"),
    ("enterprise-design-patterns", "active-record"),
    ("enterprise-design-patterns", "optimistic-offline-lock"),
    ("enterprise-design-patterns", "pessimistic-offline-lock"),
    ("enterprise-design-patterns", "front-controller"),
    ("enterprise-design-patterns", "gateway"),
    ("micro-services-design-patterns", "cache-aside"),
    ("micro-services-design-patterns", "rate-limiter"),
    ("micro-services-design-patterns", "timeout"),
    ("micro-services-design-patterns", "queue-based-load-leveling"),
    ("micro-services-design-patterns", "competing-consumers"),
    ("micro-services-design-patterns", "claim-check"),
    ("micro-services-design-patterns", "leader-election"),
    ("micro-services-design-patterns", "publisher-subscriber"),
    ("micro-services-design-patterns", "pipes-and-filters"),
    ("micro-services-design-patterns", "scatter-gather"),
    ("concurrency-design-patterns", "double-checked-locking"),
    ("concurrency-design-patterns", "balking"),
    ("concurrency-design-patterns", "guarded-suspension"),
    ("concurrency-design-patterns", "thread-local-storage"),
    ("concurrency-design-patterns", "fork-join"),
    ("concurrency-design-patterns", "actor"),
    ("concurrency-design-patterns", "two-phase-termination"),
    ("messaging-integration-patterns", "message-channel"),
    ("messaging-integration-patterns", "content-based-router"),
    ("messaging-integration-patterns", "splitter-aggregator"),
    ("messaging-integration-patterns", "dead-letter-channel"),
    ("messaging-integration-patterns", "event-bus"),
    ("architectural-design-patterns", "event-driven-architecture"),
    ("architectural-design-patterns", "microkernel"),
    ("architectural-design-patterns", "pipe-and-filter-architecture"),
    ("architectural-design-patterns", "mvp-and-mvvm"),
    ("architectural-design-patterns", "onion-architecture"),
    ("architectural-design-patterns", "serverless"),
    ("platform-design-patterns", "blue-green-and-canary"),
    ("platform-design-patterns", "feature-toggle"),
    ("platform-design-patterns", "service-mesh"),
    ("platform-design-patterns", "consumer-driven-contract"),
    ("foundational-design-patterns", "multiton"),
    ("foundational-design-patterns", "type-object"),
    ("foundational-design-patterns", "fluent-interface"),
    ("foundational-design-patterns", "execute-around"),
    ("foundational-design-patterns", "callback"),
    ("foundational-design-patterns", "delegation"),
]

# Demos that mint an identifier per run, so their output is not byte-stable.
NONDETERMINISTIC = {"simple-factory", "factory-method", "facade"}

NAMES = {
    "simple-factory": "Simple Factory", "static-factory": "Static Factory",
    "factory-method": "Factory Method", "abstract-factory": "Abstract Factory",
    "builder": "Builder", "prototype": "Prototype", "singleton": "Singleton",
    "adapter": "Adapter", "bridge": "Bridge", "composite": "Composite",
    "decorator": "Decorator", "facade": "Facade", "flyweight": "Flyweight",
    "proxy": "Proxy",
    "strategy": "Strategy",
    "observer": "Observer",
    "command": "Command",
    "template-method": "Template Method",
    "state": "State",
    "chain-of-responsibility": "Chain of Responsibility",
    "iterator": "Iterator",
    "mediator": "Mediator",
    "memento": "Memento",
    "visitor": "Visitor",
    "interpreter": "Interpreter",
    "api-gateway": "API Gateway",
    "service-discovery": "Service Registry and Discovery",
    "load-balancing": "Client-Side Load Balancing",
    "retry": "Retry with Backoff",
    "circuit-breaker": "Circuit Breaker",
    "bulkhead": "Bulkhead",
    "database-per-service": "Database per Service",
    "api-composition": "API Composition",
    "cqrs": "CQRS",
    "saga": "Saga",
    "transactional-outbox": "Transactional Outbox",
    "idempotent-consumer": "Idempotent Consumer",
    "externalised-configuration": "Externalised Configuration",
    "distributed-tracing": "Distributed Tracing",
    "backends-for-frontends": "Backends for Frontends",
    "sidecar": "Sidecar",
    "sidecar-java-proxy": "Sidecar with a Java Proxy",
    "sidecar-on-kubernetes": "Sidecar on Kubernetes",
    "event-sourcing": "Event Sourcing",
    "strangler-fig": "Strangler Fig",
    "layered-architecture": "Layered Architecture",
    "mvc": "Model View Controller",
    "hexagonal-architecture": "Hexagonal Architecture",
    "clean-architecture": "Clean Architecture",
    "clean-architecture-with-spring": "Clean Architecture with Spring",
    "producer-consumer": "Producer–Consumer",
    "thread-pool": "Thread Pool",
    "future-promise": "Future/Promise",
    "read-write-lock": "Read–Write Lock",
    "monitor-object": "Monitor Object",
    "active-object": "Active Object",
    "data-mapper": "Data Mapper",
    "identity-map": "Identity Map",
    "unit-of-work": "Unit of Work",
    "lazy-load": "Lazy Load",
    "repository": "Repository",
    "service-layer": "Service Layer",
    "dto": "DTO",
    "identity-map-with-jpa": "Identity Map with JPA",
    "unit-of-work-with-spring": "Unit of Work with Spring",
    "lazy-load-with-hibernate": "Lazy Load with Hibernate",
    "repository-with-spring-data": "Repository with Spring Data",
    "null-object": "Null Object",
    "object-pool": "Object Pool",
    "registry": "Registry",
    "service-locator": "Service Locator",
    "dependency-injection": "Dependency Injection",
    "dependency-injection-with-spring": "Dependency Injection with Spring",
    "registry-with-spring": "Registry with Spring",
    "object-pool-with-hikaricp": "Object Pool with HikariCP",
    "service-locator-with-consul": "Service Locator with Consul",
    "thread-pool-with-spring": "Thread Pool with Spring",
    "future-promise-with-spring": "Future/Promise with Spring",
    "active-object-with-spring": "Active Object with Spring",
    "singleton-with-spring": "Singleton with Spring",
    "prototype-with-spring": "Prototype with Spring",
    "proxy-with-spring": "Proxy with Spring",
    "observer-with-spring": "Observer with Spring",
    "strategy-with-spring": "Strategy with Spring",
    "template-method-with-spring": "Template Method with Spring",
    "chain-of-responsibility-with-spring": "Chain of Responsibility with Spring",
    "interpreter-with-spel": "Interpreter with SpEL",
    "circuit-breaker-with-resilience4j": "Circuit Breaker with Resilience4j",
    "retry-with-resilience4j": "Retry with Resilience4j",
    "bulkhead-with-resilience4j": "Bulkhead with Resilience4j",
    "api-gateway-with-spring-cloud-gateway": "API Gateway with Spring Cloud Gateway",
    "load-balancing-with-spring-cloud-loadbalancer": "Load Balancing with Spring Cloud LoadBalancer",
    "service-discovery-with-spring-cloud-consul": "Service Discovery with Spring Cloud Consul",
    "value-object": "Value Object",
    "aggregate": "Aggregate",
    "domain-event": "Domain Event",
    "specification": "Specification",
    "anti-corruption-layer": "Anti-Corruption Layer",
    "layered-architecture-with-spring-boot": "Layered Architecture with Spring Boot",
    "mvc-with-spring-mvc": "MVC with Spring MVC",
    "hexagonal-architecture-with-spring-boot": "Hexagonal Architecture with Spring Boot",
    "bounded-context": "Bounded Context",
    "transaction-script": "Transaction Script",
    "active-record": "Active Record",
    "optimistic-offline-lock": "Optimistic Offline Lock",
    "pessimistic-offline-lock": "Pessimistic Offline Lock",
    "front-controller": "Front Controller",
    "gateway": "Gateway",
    "cache-aside": "Cache-Aside",
    "rate-limiter": "Rate Limiter",
    "timeout": "Timeout",
    "queue-based-load-leveling": "Queue-Based Load Leveling",
    "competing-consumers": "Competing Consumers",
    "claim-check": "Claim Check",
    "leader-election": "Leader Election",
    "publisher-subscriber": "Publisher-Subscriber",
    "pipes-and-filters": "Pipes and Filters",
    "scatter-gather": "Scatter-Gather",
    "double-checked-locking": "Double-Checked Locking",
    "balking": "Balking",
    "guarded-suspension": "Guarded Suspension",
    "thread-local-storage": "Thread-Local Storage",
    "fork-join": "Fork-Join",
    "actor": "Actor",
    "two-phase-termination": "Two-Phase Termination",
    "message-channel": "Message Channel",
    "content-based-router": "Content-Based Router",
    "splitter-aggregator": "Splitter and Aggregator",
    "dead-letter-channel": "Dead Letter Channel",
    "event-bus": "Event Bus",
    "event-driven-architecture": "Event-Driven Architecture",
    "microkernel": "Microkernel",
    "pipe-and-filter-architecture": "Pipe-and-Filter Architecture",
    "mvp-and-mvvm": "MVP and MVVM",
    "onion-architecture": "Onion Architecture",
    "serverless": "Serverless Functions",
    "blue-green-and-canary": "Blue-Green and Canary",
    "feature-toggle": "Feature Toggle",
    "service-mesh": "Service Mesh",
    "consumer-driven-contract": "Consumer-Driven Contract",
    "multiton": "Multiton",
    "type-object": "Type Object",
    "fluent-interface": "Fluent Interface",
    "execute-around": "Execute Around",
    "callback": "Callback",
    "delegation": "Delegation",
}

# ---------------------------------------------------------------------------
# Per-project content.
#
#   purpose      -- what this project teaches, in the store's terms
#   nongoals     -- what a reader must not mistake it for
#   problem      -- the scenario and what the pattern has to deliver. The full
#                   treatment stays in the project's problem-statement.md; this
#                   is the summary a specification needs.
#   roles        -- (role, types) rows mapping the pattern's vocabulary onto
#                   the actual class names
#   requirements -- the properties the code must have, each one falsifiable
# ---------------------------------------------------------------------------

META = {

"simple-factory": dict(
purpose="""
Teach how a *value* -- a dropdown selection, a JSON field, a database column --
becomes an *object*, and why that conversion belongs in one named place rather
than wherever it is first needed.
""",
nongoals=[
    "Not a payment integration. `CreditCardPayment` prints; it does not "
    "authorise anything.",
    "Not a Gang of Four pattern. Simple Factory is not in the book -- it is "
    "the everyday idiom that Factory Method and Abstract Factory both grow "
    "out of, which is why it comes first in the learning order.",
    "Not an argument against dependency injection. A DI container solves an "
    "overlapping problem, and the written notes say so.",
],
problem="""
The payment step of an online store offers four methods -- credit card, UPI,
PayPal, net banking. They do the same job from the outside, taking a
`PaymentRequest` and returning a `PaymentReceipt`, so one interface covers
them all.

The choice, though, arrives as data. It comes from a dropdown, a JSON field or
a database column: a `String` or an enum, never a Java type. Something has to
turn that value into an object, and if that something is a `switch` inside
`CheckoutService`, then checkout knows about every payment method that exists.
Adding a fifth means editing checkout, and every other place that had to make
the same decision.

**What the pattern must deliver:** exactly one place in the codebase that
names the concrete payment classes. Everywhere else asks for a `PaymentMethod`
and is told nothing about which one it got.
""",
roles=[
    ("Product interface", "`PaymentMethod`"),
    ("Concrete products", "`CreditCardPayment`, `UpiPayment`, `PayPalPayment`, `NetBankingPayment`"),
    ("Factory", "`PaymentMethodFactory`"),
    ("Client", "`CheckoutService`"),
    ("Value objects", "`PaymentRequest`, `PaymentReceipt`, `PaymentType`"),
    ("Entry point", "`SimpleFactoryDemo`"),
],
requirements=[
    "**The factory is the only place a concrete method is named.** Grepping "
    "for `new CreditCardPayment()` must find exactly one call site.",
    "**The client never branches on the payment type.** If `CheckoutService` "
    "contains a `switch` over `PaymentType`, the decision has been duplicated, "
    "not centralised.",
    "**An unknown type fails loudly**, with a message naming the value that "
    "was not recognised. Silently returning a default is how a customer pays "
    "by a method they did not choose.",
],
),

"static-factory": dict(
purpose="""
Teach why a constructor's name -- which is to say, the class's name, because a
constructor has no name of its own -- is often the wrong thing to have to say,
and what you gain by replacing it with a static method that can be named.
""",
nongoals=[
    "Not a Gang of Four pattern. This is the Effective Java idiom, included "
    "because it is the cheapest possible introduction to the idea that "
    "construction is a decision worth naming.",
    "Not a money library. `Money` exists so the arithmetic is readable; use "
    "`BigDecimal` and a real currency type in production.",
    "Not a promotions engine. Real discount stacking has rules about "
    "precedence and exclusivity that this deliberately does not model.",
]  ,
problem="""
The store needs four kinds of discount -- a percentage off, a flat amount off,
free shipping, and no discount at all -- and marketing promises more.

A constructor cannot express that. `new Discount(10)` is ambiguous the moment
both "10% off" and "£10 off" exist, and the language will not even let you
declare both, because two constructors taking a `double` have the same
signature. The usual escape is a flag parameter or an enum argument, which
means every call site has to be read carefully to find out what it does.

**What the pattern must deliver:** construction that says what it means at the
call site. `Discount.percentage(10)` and `Discount.amountOff(Money.pounds(10))`
cannot be confused for one another, can return different implementations, and
can return a cached instance where one will do.
""",
roles=[
    ("Abstraction", "`Discount`"),
    ("Implementations", "`PercentageDiscount`, `AmountOffDiscount`, `FreeShippingDiscount`, `NoDiscount`, `BestOfDiscount`"),
    ("Client", "`CheckoutService`"),
    ("Value objects", "`Money`, `Order`, `Receipt`"),
    ("Entry point", "`StaticFactoryDemo`"),
],
requirements=[
    "**Constructors are not public.** If callers can still write `new "
    "PercentageDiscount(...)`, the named methods are decoration rather than "
    "the way in.",
    "**Every factory method names its intent**, not its parameters. "
    "`Discount.percentage(10)` reads at the call site; `Discount.of(10, true)` "
    "does not.",
    "**Factory methods return the abstraction**, so which implementation comes "
    "back stays a private decision -- that freedom is the whole point of the "
    "idiom.",
],
),

"factory-method": dict(
purpose="""
Teach the case where a workflow is fixed but one step inside it varies: the
base class owns the sequence, and a subclass decides only the thing that
genuinely differs.
""",
nongoals=[
    "Not a carrier integration. The couriers print and return a `Shipment`.",
    "Not a claim that inheritance is the right tool here in production -- a "
    "constructor parameter often is. The written notes cover when the "
    "subclass hook earns its keep and when it does not.",
    "Not Template Method, though the two are close relatives and the "
    "explained document draws the line between them.",
],
problem="""
The shipping step offers four delivery tiers, each handing the parcel to a
different carrier: Standard to a postal courier, Express to an air courier,
Same Day to a bike courier, International to a freight courier.

The carriers share one interface, so picking between them is easy. The part
that matters is that shipping is not just "pick a carrier". Every tier runs
the same workflow -- validate the order, log that the parcel is being
prepared, hand it over, log the tracking number. Writing that workflow four
times means four places to fix when the logging changes, and four chances for
them to diverge.

**What the pattern must deliver:** the workflow written once, with a single
hole in it that each tier fills. A new tier supplies a courier and inherits
the sequence; it cannot accidentally reorder the steps, because it never sees
them.
""",
roles=[
    ("Creator", "`DeliveryService`"),
    ("Concrete creators", "`StandardDelivery`, `ExpressDelivery`, `SameDayDelivery`, `InternationalDelivery`"),
    ("Product interface", "`Courier`"),
    ("Concrete products", "`PostalCourier`, `AirCourier`, `BikeCourier`, `GlobalCourier`"),
    ("Value objects", "`Order`, `Shipment`, `TrackingIds`"),
    ("Entry point", "`FactoryMethodDemo`"),
],
requirements=[
    "**The base class never names a concrete courier.** It calls its own "
    "factory method and nothing else.",
    "**Subclasses override the factory method and nothing else.** A subclass "
    "that also overrides the workflow has defeated the pattern.",
    "**The workflow is identical for all four tiers**, demonstrably: the "
    "printed output differs only in the carrier and the timings.",
],
),

"abstract-factory": dict(
purpose="""
Teach the case where several objects must be chosen *together*, and where any
mixed selection is a bug: one decision produces a whole consistent family.
""",
nongoals=[
    "Not a production tax or currency library. `UkVatCalculator` hard-codes "
    "20%; a real system reads rates from a table that changes by legislation.",
    "Not a survey of alternatives. Dependency injection containers, service "
    "locators and enum-based strategies all solve overlapping problems, and "
    "the written notes say so, but the project demonstrates one pattern.",
    "Not a reference for internationalisation. `RupeeFormatter` formats a "
    "number; it is not `java.text.NumberFormat` and does not pretend to be.",
],
problem="""
An online store that has been selling in one country is about to sell in
three. Checkout turns out not to be one piece of logic but three, and all
three change together when the market changes:

| Market | Tax | Money | Address |
| --- | --- | --- | --- |
| United Kingdom | 20% VAT | £1,234.50 · GBP | postcode — `EH1 1YZ` |
| United States | 8.875% Sales Tax | $1,234.50 · USD | ZIP code — `10001` |
| India | 18% GST | ₹1,234.50 · INR | PIN code — `560001` |

Each column is easy alone: three tax calculators, three currency formatters,
three address validators -- nine small classes behind three interfaces.

**The difficulty is that the three must agree.** A receipt showing British VAT
next to a dollar sign is not a small bug, it is a wrong invoice. A checkout
that accepts an American ZIP code and then charges Indian GST is worse. Nine
classes, and only three of the twenty-seven combinations are legal.

The naive client picks each piece for itself, which means three separate
`if`/`else` chains over the same `market` string, in one method, kept in
agreement by hand. Nothing in the type system stops the next developer adding
a case to two chains and forgetting the third; the result compiles, runs, and
produces a wrong invoice silently.

**What the pattern must deliver:** a mismatched family becomes not merely
uncaught but unrepresentable. One decision -- which market -- is made once,
and the three pieces that follow from it cannot disagree, because the client
never selects them individually.

The project is also required to be honest about the cost. Adding a fourth
*market* is cheap: one new factory class, no existing code changed. Adding a
fourth *product kind* -- a shipping-rules interface, say -- is expensive:
every factory in the family must change. The written notes and the video both
cover this, and the video gives it a scene. A teaching project that only shows
the upside teaches the wrong lesson about when to reach for the pattern.
""",
roles=[
    ("Abstract factory", "`MarketFactory`"),
    ("Concrete factories", "`UkMarketFactory`, `UsMarketFactory`, `IndiaMarketFactory`"),
    ("Abstract products", "`TaxCalculator`, `CurrencyFormatter`, `AddressValidator`"),
    ("Concrete products", "`UkVatCalculator`, `UsSalesTaxCalculator`, `IndiaGstCalculator`, `PoundFormatter`, `DollarFormatter`, `RupeeFormatter`, `UkPostcodeValidator`, `UsZipValidator`, `IndiaPinValidator`"),
    ("Client", "`CheckoutService`"),
    ("Value objects", "`Order`, `Quote`"),
    ("Entry point", "`AbstractFactoryDemo`"),
],
requirements=[
    "**The client takes a factory, never a market string.** `CheckoutService` "
    "must have no knowledge of which markets exist. If it can name \"UK\", the "
    "pattern has not been applied -- it has only been moved.",
    "**Concrete product types are never named outside their factory.** "
    "Grepping for `new UkVatCalculator()` must find exactly one call site.",
    "**A factory returns one family or none.** There is no path through the "
    "code that yields a UK tax rule beside a dollar formatter.",
],
),

"builder": dict(
purpose="""
Teach construction of an object with many optional parts: how to keep it
immutable and validated without a constructor whose parameter list nobody can
read.
""",
nongoals=[
    "Not Lombok's `@Builder`. Writing the builder by hand is the point; "
    "generating it hides exactly the decisions being taught.",
    "Not a validation framework. `build()` checks what it must; Bean "
    "Validation is a different tool for a different job.",
    "Not an argument that everything needs a builder. Two or three "
    "parameters do not.",
],
problem="""
Placing a purchase order involves two facts that never change -- who is buying,
and where it ships -- and a pile of options that vary: gift wrapping, a gift
message, priority handling, a coupon code, a note for the warehouse.

A constructor taking all of them is unreadable at the call site: a row of
booleans and nulls whose meaning depends entirely on position, where swapping
two arguments of the same type compiles cleanly and ships the wrong thing.
Telescoping overloads multiply instead of solving it. Setters fix the
readability and give up immutability and validation, leaving an object that
can exist in a half-built state.

**What the pattern must deliver:** a call site that names each option it sets,
an object that is immutable once built, and a single place where "is this
order actually valid" is answered -- before the object exists, not after.
""",
roles=[
    ("Product", "`PurchaseOrder`"),
    ("Builder", "`PurchaseOrder.Builder`"),
    ("Presets", "`PurchaseOrderPresets`"),
    ("Value objects", "`LineItem`, `Address`, `Money`"),
    ("Entry point", "`PurchaseOrderDemo`"),
],
requirements=[
    "**`PurchaseOrder` has no public constructor and no setters.** The builder "
    "is the only way to make one, and a built order cannot be changed.",
    "**`build()` validates.** A missing customer or an empty item list is "
    "rejected there, so an invalid `PurchaseOrder` cannot exist.",
    "**Collections are copied on the way in and unmodifiable on the way out**, "
    "so a caller holding the original list cannot mutate a built order.",
],
),

"prototype": dict(
purpose="""
Teach copying a configured object as an alternative to rebuilding it, and --
more importantly -- how to decide, field by field, what a copy must duplicate
and what it may share.
""",
nongoals=[
    "Not an endorsement of `Cloneable` and `Object.clone()`. The project "
    "implements its own `Prototype` interface, and the written notes explain "
    "why the built-in mechanism is best avoided.",
    "Not a serialization-based deep-copy utility. Those exist and have their "
    "place; they hide the decision this project is about.",
    "Not a caching layer. The registry stores masters to copy, not results.",
],
problem="""
A seller lists "Wireless Earbuds" in black. Getting that one listing right is
real work: a category from the taxonomy, a description that satisfies
compliance, a shipping profile, a return window and warranty matching the
category's policy, photos, a dozen attributes.

Now the same earbuds in white, and again in blue. Nothing about the category,
the compliance text, the shipping profile, the return window or the warranty
changed -- only the SKU, the title, one attribute and the photos did.
Constructing each variant from scratch means repeating every unchanged
argument, and every repetition is a chance to get one of them subtly wrong.

**What the pattern must deliver:** an existing, correct listing is the
starting point for the next one. Copy it, change the three things that differ,
and the rest is right by construction -- with the copy deep enough that
editing the variant cannot reach back and alter the original.
""",
roles=[
    ("Prototype interface", "`Prototype`"),
    ("Concrete prototype", "`ProductListing`"),
    ("Registry", "`ListingRegistry`"),
    ("Value objects", "`Money`, `ShippingProfile`"),
    ("Entry point", "`ProductListingDemo`"),
],
requirements=[
    "**Mutating a copy never affects its original.** This is the property the "
    "tests exist to defend; a shallow copy of the attribute map breaks it "
    "silently.",
    "**Sharing is deliberate, not accidental.** Immutable values may be shared "
    "by reference, and the code says why at each point rather than deep-copying "
    "everything out of caution.",
    "**The registry hands out copies, never its masters.** A caller that "
    "mutated a registry entry would corrupt every later copy.",
],
),

"singleton": dict(
purpose="""
Teach the case for exactly one instance, how Java actually enforces that
against reflection and serialization, and -- just as much -- when the pattern
is the wrong answer.
""",
nongoals=[
    "Not an endorsement of singletons as a default. The pattern makes "
    "dependencies invisible and tests order-dependent; the written notes are "
    "explicit that a single instance passed by dependency injection is "
    "usually better.",
    "Not a distributed ID generator. One JVM, one counter. Real order numbers "
    "across several instances need a database sequence or a snowflake ID.",
    "Not a lazy-initialisation tutorial. Double-checked locking is discussed "
    "and then not used, because the enum does the job.",
],
problem="""
Every checkout needs an order number -- `ORD-000001`, `ORD-000002` -- handed
out in strict sequence with no gaps and no repeats. Two customers must never
receive the same number, whichever part of the system issued it: checkout, the
admin console raising a manual order, or a background job replaying a failed
payment.

An ordinary class fails immediately: each caller that constructs its own
generator gets its own counter, so three independent components cheerfully
hand out `ORD-000001` three times. A `static` counter fixes the duplication
and introduces a different problem -- nothing stops two threads reading the
same value before either writes back.

**What the pattern must deliver:** one instance that the language guarantees,
not one that a convention requests; and a counter that is correct when several
threads call it at once.
""",
roles=[
    ("Singleton", "`OrderSequenceGenerator`"),
    ("Counter-example", "`LegacyOrderSequenceGenerator`"),
    ("Entry point", "`OrderSequenceGeneratorDemo`"),
],
requirements=[
    "**The singleton is an enum.** That is what makes a second instance "
    "impossible: reflection cannot invoke an enum constructor, and "
    "deserialization returns the existing constant rather than a copy.",
    "**The counter is thread-safe**, and a test proves it by issuing numbers "
    "concurrently and asserting the set of results has no duplicates.",
    "**The broken version stays in the project.** `LegacyOrderSequenceGenerator` "
    "exists to be demonstrated failing; deleting it would remove the reason "
    "the pattern is there.",
],
),

"adapter": dict(
purpose="""
Teach how to put a class you do not control behind the interface your code
already speaks, so that the mismatch is translated in one place instead of at
every call site.
""",
nongoals=[
    "Not a real carrier integration. `AcmeShippingSdk` is a stand-in for a "
    "third-party jar, and is deliberately awkward in the way real ones are.",
    "Not a units library. The conversions are arithmetic in one method "
    "because that is where the lesson is.",
],
problem="""
Checkout needs a shipping cost for a destination and a package weight, in the
units the rest of the codebase already uses: kilograms and dollars. The
company has just signed with a third-party carrier, and their SDK is the only
source of real rates.

The SDK does not match. It takes pounds, returns integer cents, and names the
method something unrelated to anything checkout says. Calling it directly
means the conversion is written wherever a rate is needed -- and the second
time somebody writes it, one of the two will eventually be wrong, or will be
updated when the other is not. The SDK's vocabulary also spreads: checkout
starts mentioning a vendor it should never have heard of.

**What the pattern must deliver:** one class that speaks both languages, and
a checkout that names only its own interface. Swapping the carrier, or falling
back to a flat rate, becomes a change of which implementation is passed in.
""",
roles=[
    ("Target interface", "`ShippingRateProvider`"),
    ("Adapter", "`AcmeShippingAdapter`"),
    ("Adaptee", "`AcmeShippingSdk`"),
    ("Alternative implementation", "`FlatRateShippingProvider`"),
    ("Client", "`CheckoutService`"),
    ("Naive alternatives", "`NaiveCheckoutService`, `NaiveShippingEstimator`"),
    ("Entry point", "`ShippingDemo`"),
],
requirements=[
    "**The unit conversion appears exactly once**, inside the adapter. Two "
    "copies of a pounds-to-kilograms factor is the bug the pattern prevents.",
    "**`CheckoutService` never mentions Acme.** It depends on "
    "`ShippingRateProvider` and cannot tell which implementation it holds.",
    "**The adapter and the flat-rate provider are interchangeable**, "
    "demonstrated by running checkout against both.",
],
),

"bridge": dict(
purpose="""
Teach what to do when two things vary independently and the obvious design
multiplies them together: separate the two hierarchies and let them meet
through composition.
""",
nongoals=[
    "Not a messaging integration. The channels print.",
    "Not a template for every pair of varying concepts. The written notes are "
    "clear that the pattern earns its keep when both dimensions really do keep "
    "growing, and is over-engineering when one of them is fixed.",
],
problem="""
The store sends several *kinds* of notification -- order confirmations,
shipping updates, password resets -- over several *channels* -- email, SMS,
push. Every kind must be sendable over every channel.

The obvious shape is a class per pair: `OrderConfirmationEmail`,
`OrderConfirmationSms`, `ShippingUpdateEmail`, and so on. Three kinds and
three channels is nine classes; adding a fourth channel adds four more, and
adding a fourth notification adds another four. Worse, the wording of a
notification and the mechanics of a channel end up interleaved in the same
method, so changing how SMS is delivered means editing every notification that
can be sent by SMS.

**What the pattern must deliver:** kinds and channels that grow independently.
A new channel is one class and touches no notification; a new notification is
one class and touches no channel. Nine classes become three plus three.
""",
roles=[
    ("Abstraction", "`Notification`"),
    ("Refined abstractions", "`OrderConfirmationNotification`, `ShippingUpdateNotification`, `PasswordResetNotification`"),
    ("Implementor interface", "`MessageChannel`"),
    ("Concrete implementors", "`EmailChannel`, `SmsChannel`, `PushChannel`"),
    ("Naive alternatives", "`NaiveOrderConfirmationEmail`, `NaiveOrderConfirmationSms`, `NaiveShippingUpdateEmail`, `NaiveShippingUpdateSms`"),
    ("Entry point", "`NotificationDemo`"),
],
requirements=[
    "**A notification holds a `MessageChannel`, never a concrete channel.** "
    "If `OrderConfirmationNotification` names `EmailChannel`, the two "
    "hierarchies are still fused.",
    "**Adding a channel changes no notification class**, and adding a "
    "notification changes no channel class. This is the property that "
    "distinguishes the pattern from a plain interface.",
    "**Channels are testable without I/O**, via a recording channel the tests "
    "supply in place of a real one.",
],
),

"composite": dict(
purpose="""
Teach how to treat a single thing and a collection of things through the same
interface, so that code walking a tree never has to ask which one it is
holding.
""",
nongoals=[
    "Not a catalog engine. The tree is built in code; a real one comes from a "
    "database and needs paging.",
    "Not a claim that every hierarchy should be a composite. The written notes "
    "cover the cost: a shared interface that leaves half its methods "
    "meaningless on a leaf is a warning sign, not a success.",
],
problem="""
The catalog is a tree. `Electronics` holds a phone directly and also an
`Accessories` category, which holds a case and a charger plus a nested
`Cables` category holding a USB-C cable. Categories hold products, and they
hold more categories, to whatever depth merchandising wants.

Three operations are needed over that tree: the total price beneath a node,
how many products it contains, and an indented print of the whole thing.

If products and categories share nothing, the children must be held as
`List<Object>`, and every one of those three operations becomes a recursive
walk full of `instanceof` and casts. Each new operation repeats the same
type-dispatch, and each is a chance to forget a case -- and adding a third
kind of node means finding and updating every one of those chains.

**What the pattern must deliver:** one interface implemented by both the leaf
and the container, so that the client asks the node for its total and the
recursion lives inside the container. No `instanceof`, no casts, no depth
limit.
""",
roles=[
    ("Component interface", "`CatalogComponent`"),
    ("Leaf", "`Product`"),
    ("Composite", "`Category`"),
    ("Naive alternatives", "`NaiveProduct`, `NaiveCategory`, `NaiveCatalogPrinter`"),
    ("Entry point", "`CatalogDemo`"),
],
requirements=[
    "**No `instanceof` and no casting in client code.** This is checkable by "
    "grep and is the single clearest signal that the pattern is doing its job.",
    "**The recursion lives in `Category`**, not in the caller. A client that "
    "walks children itself has taken the responsibility back.",
    "**Depth is unbounded**, and the demo tree is nested deeply enough -- "
    "three levels -- that a design only working one level down would fail.",
],
),

"decorator": dict(
purpose="""
Teach adding behaviour to an object at runtime by wrapping it, and why that
beats a subclass for every combination of options a customer might pick.
""",
nongoals=[
    "Not a pricing engine. Real checkout pricing has tax interactions and "
    "ordering rules this deliberately does not model.",
    "Not a claim that decorators are free. The written notes cover the cost: "
    "a deep stack is hard to debug, and the object you hold is no longer the "
    "one you created.",
],
problem="""
A product has a base price, and at checkout the customer can add optional
extras: gift wrapping, shipment insurance, express handling. Any combination
should be selectable -- one of them, all three, or none.

A class per combination is the obvious first move and collapses immediately.
Three extras is seven classes; a fourth extra makes fifteen. The fee for gift
wrapping is duplicated into every class that includes it, so changing it means
finding all of them, and the combination the customer actually wants has to
have been anticipated at compile time.

**What the pattern must deliver:** each extra written once, applied to
anything that has a price, and composable in any combination and any order --
decided at runtime, when the customer chooses, rather than by the set of
classes somebody thought to write.
""",
roles=[
    ("Component interface", "`PricedItem`"),
    ("Concrete component", "`Product`"),
    ("Base decorator", "`ProductDecorator`"),
    ("Concrete decorators", "`GiftWrapDecorator`, `InsuranceDecorator`, `ExpressHandlingDecorator`"),
    ("Naive alternatives", "`NaiveGiftWrappedProduct`, `NaiveInsuredProduct`, `NaiveGiftWrappedInsuredProduct`"),
    ("Entry point", "`PricingDemo`"),
],
requirements=[
    "**A decorator is itself a `PricedItem`.** That is what lets decorators "
    "wrap decorators, and it is the whole mechanism.",
    "**Each fee is defined in exactly one class.** If the gift-wrap fee "
    "appears twice, the pattern has been applied to the shape but not to the "
    "duplication.",
    "**Decorators stack in any order**, with a test that builds the same set "
    "of extras two ways and asserts the price agrees.",
],
),

"facade": dict(
purpose="""
Teach putting one simple entry point in front of a multi-step workflow across
several subsystems, without hiding those subsystems from anyone who needs them
directly.
""",
nongoals=[
    "Not a transaction manager. A real place-order needs compensation when "
    "step three fails after step two charged the card; the written notes "
    "raise this and the code does not solve it.",
    "Not a service layer template. A facade that grows business rules of its "
    "own has stopped being a facade, and the notes say where that line is.",
],
problem="""
When a customer clicks **Place Order**, four things must happen in a specific
order: reserve the stock so nobody else takes the last item, charge the card
but only once stock is confirmed, schedule the shipment, and email a
confirmation carrying the tracking number.

Each step lives in its own service, written by a different team, each with its
own vocabulary and its own return type that the next step needs. A caller
doing this itself has to know all four APIs, the order they go in, and which
output feeds which input. Every screen that can place an order repeats that
knowledge, and the ordering constraint -- stock before payment -- is enforced
only by everyone remembering it.

**What the pattern must deliver:** one method that takes an `OrderRequest` and
returns an `OrderConfirmation`, with the sequence and the plumbing in one
place. The four services stay public and directly usable, because a facade
that locks them away has replaced a hard API with a limited one.
""",
roles=[
    ("Facade", "`OrderFacade`"),
    ("Subsystems", "`InventoryService`, `PaymentService`, `ShippingService`, `NotificationService`"),
    ("Value objects", "`OrderRequest`, `OrderConfirmation`"),
    ("Entry point", "`FacadeDemo`"),
],
requirements=[
    "**The facade adds no business rules.** It sequences calls and moves data "
    "between them; a discount calculation appearing here means the "
    "responsibility has drifted.",
    "**The subsystems remain usable on their own.** Nothing is made "
    "package-private to force callers through the facade -- the facade is a "
    "convenience, not a wall.",
    "**The ordering constraint is enforced in one place**: stock is reserved "
    "before the card is charged, and that fact lives in the facade rather "
    "than in every caller.",
],
),

"flyweight": dict(
purpose="""
Teach separating the state that is genuinely per-object from the state that is
identical across thousands of objects, and sharing the second kind instead of
copying it.
""",
nongoals=[
    "Not a general memory-optimisation guide. Flyweight is worth reaching for "
    "when profiling has shown duplicated immutable state, and the written "
    "notes are blunt that applying it speculatively costs clarity for nothing.",
    "Not a cache. The factory's map is a pool of shared values with a fixed "
    "key space, not an eviction policy.",
],
problem="""
Every catalog listing can carry a badge -- `NEW`, `SALE`, `BESTSELLER`,
`LOW_STOCK`. A badge is more than a label: it has an icon, a background
colour, a text colour, a bold rule, and the rasterised artwork the design
system hands over.

There are four distinct badge designs. There are, this quarter, one hundred
thousand listings. Giving each listing its own badge object builds a hundred
thousand copies of four designs, and the artwork -- the expensive part -- is
duplicated with them. The data is identical, immutable, and copied anyway.

**What the pattern must deliver:** four `BadgeStyle` instances, shared by
every listing that uses them, with the per-listing part -- which listing,
which position -- kept outside. Asking twice for the same badge type must
return the *same object*, not an equal one.
""",
roles=[
    ("Flyweight (intrinsic state)", "`BadgeStyle`"),
    ("Flyweight factory", "`BadgeStyleFactory`"),
    ("Context (extrinsic state)", "`CatalogBadge`"),
    ("Key", "`BadgeType`"),
    ("Naive alternative", "`NaiveListingBadge`"),
    ("Entry point", "`BadgeDemo`"),
],
requirements=[
    "**`BadgeStyle` is immutable.** A shared mutable object is not an "
    "optimisation, it is a defect affecting every listing at once.",
    "**The factory returns the identical instance** for a repeated type, "
    "asserted with `assertSame` rather than `assertEquals` -- equality would "
    "pass even if nothing were shared.",
    "**No extrinsic state is stored on the flyweight.** The moment a "
    "`BadgeStyle` knows which listing it belongs to, it cannot be shared.",
],
),

"proxy": dict(
purpose="""
Teach standing something in front of an object that has the same interface,
and using that position to control when the real object is built and who is
allowed to reach it.
""",
nongoals=[
    "Not an image library. Loading is simulated and counted so the saving is "
    "visible.",
    "Not an authorisation framework. The role check is deliberately trivial; "
    "real systems need policies, not an enum comparison.",
    "Not a dynamic-proxy tutorial. `java.lang.reflect.Proxy` and the "
    "frameworks built on it are mentioned in the written notes and not used, "
    "because the hand-written version is what makes the mechanism visible.",
],
problem="""
A category page shows sixty listings. Each has a full-resolution image that is
expensive to decode, and only a handful are ever scrolled into view. Some
images -- unreleased products, supplier-restricted assets -- may only be
viewed by catalog staff.

Loading eagerly pays for sixty decodes to show six. Putting the access check
in the listing page means every screen that can display an image repeats it,
and the screen that forgets is the one that leaks. Both concerns are about
*getting to* the image rather than about the image itself, so both are in the
wrong class.

**What the pattern must deliver:** two small stand-ins with the same interface
as the real image. One defers construction until the image is actually
displayed and then keeps it; the other refuses callers who are not entitled,
before any loading happens. Because they share the interface, they compose --
and the caller cannot tell it is not holding the real thing.
""",
roles=[
    ("Subject interface", "`ProductImage`"),
    ("Real subject", "`HighResolutionProductImage`"),
    ("Virtual proxy", "`LazyProductImage`"),
    ("Protection proxy", "`RestrictedProductImage`"),
    ("Naive alternatives", "`NaiveProductListing`, `NaiveAdminImageViewer`"),
    ("Supporting type", "`Role`"),
    ("Entry point", "`ProductImageDemo`"),
],
requirements=[
    "**Both proxies implement `ProductImage`.** A proxy with its own interface "
    "is a wrapper, and the client would have to know which it holds.",
    "**The real image is constructed at most once**, however many times the "
    "lazy proxy is asked, with a load counter proving it.",
    "**Denial happens before any load.** A protection proxy that fetches the "
    "image and then refuses to show it has leaked the expensive work and, on "
    "a metered backend, the fact of the request.",
],
),

"strategy": dict(
purpose="""
Teach lifting one *decision that varies* out of the class that uses it, so the
using class holds a behaviour rather than a flag and never branches on which
behaviour it holds.
""",
nongoals=[
    "Not a shipping-rate engine. The four rules are arithmetic chosen to be "
    "checkable by hand, not carrier tariffs.",
    "Not a claim that the `switch` disappears. It moves to `ShippingRules`, "
    "runs once at the edge instead of on every quote, and the written notes "
    "say so plainly rather than pretending otherwise.",
    "Not State. The rules here are chosen from outside and do not decide what "
    "comes next; the difference is spelled out in the notes and the video.",
],
problem="""
An online shop prices delivery four ways. A flat rate for everything, weight
bands for bulky goods, a per-hundred-miles charge for distance, and a campaign
that makes delivery free once the basket passes fifty pounds. Marketing
invents a fifth every quarter.

Written the obvious way, that is one `quote` method with one `switch` over a
shipping-method flag, and every rule's arithmetic inlined into its own branch.
Each new rule edits the method every existing rule depends on. Testing the
weight bands means constructing a checkout and steering it there through the
flag. Worst of all, the `switch` needs a `default`, and the honest default for
a value nobody recognised is the one that charges zero -- so the day an
unknown method reaches it, the shop ships for free and nothing fails.

**What the pattern must deliver:** one small interface for "work out the
delivery cost of this shipment", four independent implementations of it, and a
checkout service that holds one and calls it. A fifth rule must be a new file,
compiled against nothing but the interface, with no edit to checkout at all.
""",
roles=[
    ("Strategy interface", "`ShippingCostRule`"),
    ("Concrete strategies", "`FlatRateRule`, `WeightBandedRule`, `DistanceBasedRule`, `FreeOverThresholdRule`"),
    ("Context", "`CheckoutService`"),
    ("Parameter object", "`Shipment`"),
    ("Selection", "`ShippingRules`"),
    ("Naive alternative", "`NaiveCheckoutService`"),
    ("Supporting types", "`Money`, `Quote`, `ShippingMethod`"),
    ("Entry point", "`ShippingCostDemo`"),
],
requirements=[
    "**`CheckoutService` contains no branch that depends on which rule it "
    "holds.** Not a `switch`, not an `instanceof`, not a name comparison -- "
    "and the strategy interface must expose nothing that would let it ask.",
    "**Each rule reads only the `Shipment` fields it needs** and knows "
    "nothing about the others, so its arithmetic can be tested on its own "
    "without a checkout.",
    "**A rule defined outside the shipped source works unchanged.** A test "
    "declares its own `ShippingCostRule` and hands it to `CheckoutService`, "
    "which proves the extension point is real rather than a list of four.",
    "**Selecting by an unknown name fails loudly.** `ShippingRules.byName` "
    "throws and names the rules it knows, because the naive version's silent "
    "`default` is the specific bug this project is written to kill.",
],
),

"observer": dict(
purpose="""
Teach letting the object that changes *announce* the change to a list it knows
nothing about, so reactions can be added, removed and made to fail
independently of the thing they react to.
""",
nongoals=[
    "Not a message broker. Notification is synchronous, in-process and "
    "in-order; there is no queue, no delivery guarantee and no retry.",
    "Not a demonstration of `java.util.Observer`. That API was deprecated in "
    "Java 9 for reasons the notes explain; the project writes its own "
    "interface, which is what modern code does.",
    "Not thread-safety. `CopyOnWriteArrayList` is used so a listener can "
    "unsubscribe itself *during* a notification, and the notes say so, "
    "because the usual assumption is that it is there for concurrency.",
    "Not Mediator. The subject here coordinates nothing; the distinction is "
    "drawn explicitly in the notes and the video.",
],
problem="""
An online order moves from Placed to Paid to Shipped to Delivered, and four
unrelated systems care. Inventory releases the reservation once it ships.
Email tells the customer. Analytics counts the transition for the funnel
report. The warehouse feed writes the line that gets the parcel picked.

Written the obvious way, that is an order service holding all four and calling
them one after another. Adding a fifth reaction edits a method four working
systems depend on, and adds a constructor parameter that breaks every test
that builds the class. Analytics wants *every* transition, so every
status-changing method ever written has to remember it. And the second call
talks to a mail server: the afternoon it times out, the order is already
marked shipped, the stock is already released, analytics never runs, and the
warehouse feed is never written -- so nobody picks the parcel, and the
exception that surfaces says `SMTP timeout` and nothing about a parcel.

**What the pattern must deliver:** one small listener interface, a subject
that keeps a list of them and announces transitions to it, and four
independent listeners that know nothing about each other. A fifth reaction
must be a new class and one `addListener` call, and one listener throwing must
not stop the others.
""",
roles=[
    ("Subject", "`Order`"),
    ("Observer interface", "`OrderListener`"),
    ("Concrete observers", "`InventoryListener`, `EmailListener`, `AnalyticsListener`, `WarehouseFeedListener`"),
    ("Event", "`OrderEvent`"),
    ("Failure report", "`ListenerFailure`"),
    ("Naive alternative", "`NaiveOrderService`"),
    ("Supporting types", "`OrderStatus`"),
    ("Entry point", "`OrderEventsDemo`"),
],
requirements=[
    "**`Order` names none of its listeners.** Searching the class for "
    "`email`, `inventory` or `warehouse` must find nothing, and the listener "
    "interface must expose nothing that would let `Order` tell them apart.",
    "**One listener throwing does not stop the rest.** The `try`/`catch` sits "
    "inside the notification loop and every failure comes back as a named "
    "`ListenerFailure`, because the outage in the naive version is the "
    "specific bug this project is written to kill.",
    "**A listener defined outside the shipped source works unchanged.** A "
    "test declares its own `OrderListener` and attaches it, which proves the "
    "extension point is real rather than a list of four.",
    "**The status is updated before the listeners run, and an unchanged "
    "status announces nothing**, so a listener sees the world the event "
    "describes and no duplicate transition is ever delivered.",
    "**A listener can remove itself while being notified.** The one-shot "
    "subscription is a normal case, not an error, and a test pins it.",
],
),

"command": dict(
purpose="""
Teach turning a request into an object, so that an edit can be stacked,
described, replayed and — the part everything else is in service of —
reversed, using state the command captures for itself while it runs.
""",
nongoals=[
    "Not Memento. Undo here is per-edit inverses, not snapshots of the whole "
    "cart; the notes and the video set the two against each other explicitly "
    "rather than pretending Command is the only answer to undo.",
    "Not a task queue. Commands run synchronously, in-process, on one cart. "
    "Queuing and scheduling are named as things the pattern makes possible, "
    "and are not implemented.",
    "Not thread-safety. `CartHistory` is single-threaded by design; undo "
    "ordering is a contract, and concurrent editing of one cart is out of "
    "scope.",
    "Not a lambda tutorial. `execute` alone would be a `Runnable`; the "
    "project exists to show what the *second* method needs, which is state "
    "that survives between two calls.",
],
problem="""
A customer edits their shopping cart -- adds an item, removes one, changes a
quantity, applies a discount code -- and then expects to be able to take any
of it back.

Written the obvious way, that is a cart edited directly with a stack of notes
beside it saying what was asked for, and an `undo` that switches over the kind
of note. It is a third of the code and, for a cart that only ever gains brand
new lines, it is correct. It falls apart the moment an edit's effect depends
on what was already there. A customer with 3 headphones adds 2 more; the note
says "add 2 of H-100"; undo removes the line, and the 3 they chose last week
go with it. A customer applies `BLACKFRIDAY` over `WELCOME10`; the note says
"coupon BLACKFRIDAY"; undo clears the coupon, and a discount they never
touched is gone. Nothing throws. The customer is simply charged the wrong
amount.

**What the pattern must deliver:** one small command interface with `execute`
and `undo`, four independent commands that each capture what their own
inverse needs *at the moment they run*, and an invoker holding two stacks of
that interface and no knowledge of any edit. A fifth kind of edit must be one
new class, and undoing must restore quantity, position and coupon exactly.
""",
roles=[
    ("Command interface", "`CartCommand`"),
    ("Concrete commands", "`AddItemCommand`, `RemoveItemCommand`, `ChangeQuantityCommand`, `ApplyCouponCommand`"),
    ("Receiver", "`Cart`"),
    ("Invoker", "`CartHistory`"),
    ("Naive alternative", "`NaiveCartEditor`"),
    ("Supporting types", "`CartLine`, `Coupon`, `Money`"),
    ("Entry point", "`CartCommandsDemo`"),
],
requirements=[
    "**Undo state is captured inside `execute`, from the receiver.** No "
    "command may work out its inverse in its constructor, because an earlier "
    "undo can invalidate that guess before the command runs. A field the "
    "constructor does not set is the visible sign of it.",
    "**Undo restores what was there, not the opposite of what was asked.** "
    "Undoing a merged add returns the previous quantity; undoing a removal "
    "restores the line's *position*; undoing a coupon restores the coupon it "
    "replaced. Each has a test written against a cart that was not empty.",
    "**`CartHistory` names no edit.** Searching the class for `coupon`, "
    "`quantity` or `sku` must find nothing, and a command defined outside the "
    "shipped source must execute and undo unchanged -- a test declares its "
    "own gift-wrapping `CartCommand` to prove it.",
    "**A command that throws is never pushed onto the undo stack**, because "
    "reversing a half-applied edit applies the inverse of something that "
    "never fully happened.",
    "**A new command clears the redo stack**, since taking a different branch "
    "makes the old future unreachable -- the behaviour of every editor the "
    "learner has used.",
],
),

"template-method": dict(
purpose="""
Teach fixing the *order* of an algorithm in one `final` method on a base
class, while leaving each individual step for a subclass to fill in -- and
teach the choice between a step that must be answered, a step with a default,
and a hook that exists only to be opted into.
""",
nongoals=[
    "Not Strategy. The steps here are not swappable at run time and are not "
    "independent of each other; the notes and the video set the two against "
    "each other explicitly, and recommend Strategy where it is the better "
    "answer, rather than pretending inheritance always wins.",
    "Not Factory Method. That pattern is this one narrowed to a single hole "
    "that returns a product. The distinction is drawn in the notes because "
    "it is the most common confusion in this corner of the catalogue, but no "
    "factory is built here.",
    "Not a defence of inheritance. The project says out loud that the pattern "
    "spends the subclass's one inheritance slot permanently, and that this is "
    "the reason composition is the better modern default for most problems.",
    "Not a workflow engine. There is one sequence, six steps long, in one "
    "process. Conditional branches, retries, compensation and persistence are "
    "all out of scope.",
],
problem="""
An online shop fulfils every order through the same six steps -- validate,
reserve, charge, pack, dispatch, notify -- and that order is not a style
choice. Charging before reserving takes money for goods the shop cannot
supply; notifying before dispatching emails a customer a reference that does
not exist yet. What varies, and varies enormously, is the inside of each step:
the shop fulfils from its own warehouse, from marketplace sellers, and as
digital downloads, and one of those has no shipping address at all.

Written the obvious way, that is three methods, each spelling the sequence out
from beginning to end. It is a third of the code of the alternative and on the
day each was written it was correct. But the sequence exists only as a
convention typed by hand in three places, and nothing in the language, the
compiler or the test suite knows those six calls have an order -- so the
copies drift one line at a time. The digital copy now notifies before it
dispatches, so a customer is emailed `Key: (not dispatched)` and the correct
licence key, minted a microsecond later, is never sent to anybody. The
marketplace copy charges before the seller confirms, so a customer is charged
£42.00 and then told the order is refused. Nothing throws, nothing fails to
compile, and both orders are marked fulfilled.

**What the pattern must deliver:** one `final` template method that owns the
order and is the only thing that does; abstract steps for the parts no default
could get right; defaults for the parts most routes want unchanged; hooks for
the parts a route may need to opt into or out of; and a fourth route that is
one new class with no edit to the base class or to any route that already
works.
""",
roles=[
    ("Abstract class", "`FulfilmentProcess`"),
    ("Template method", "`fulfil(Order)` -- `final`"),
    ("Private step", "`validate`"),
    ("Abstract steps", "`routeName`, `reserveStock`, `charge`, `dispatch`"),
    ("Steps with defaults", "`pack`, `notifyCustomer`"),
    ("Hooks", "`requiresShippingAddress()`, `afterFulfilment()`"),
    ("Concrete routes",
     "`WarehouseFulfilment`, `MarketplaceFulfilment`, `DigitalFulfilment`"),
    ("Naive alternative", "`NaiveFulfilment`"),
    ("Supporting types",
     "`Order`, `OrderLine`, `FulfilmentReport`, `Money`, `StockLedger`, "
     "`SellerApi`, `LicenceKeys`, `FulfilmentException`"),
    ("Entry point", "`FulfilmentDemo`"),
],
requirements=[
    "**The template method is `final`.** A route may decide how a step "
    "behaves and may never decide when the steps run; attempting to override "
    "`fulfil` must be a compile error, not a code-review comment.",
    "**Every step records itself on a report**, so the pattern's central "
    "claim is observable rather than asserted: the demo prints the step names "
    "of four routes side by side and they are character-for-character "
    "identical, and a `RecordingRoute` in the tests asserts on the call order "
    "directly.",
    "**A later step may rely on an earlier step's work.** "
    "`DigitalFulfilment.notifyCustomer` quotes the licence key that its own "
    "`dispatch` minted, using the same two lines the naive copy has in the "
    "wrong order -- and it is safe only because `fulfil` is `final`.",
    "**`validate` is `private`, and the hook is the only say a route gets.** "
    "The digital route answers `requiresShippingAddress()` with `false` and "
    "gets its addressless orders through, without weakening the address check "
    "for any other route and without being able to skip validation.",
    "**A hook must not be able to change the sequence.** "
    "`afterFulfilment` posts a *note* rather than a step, so the marketplace "
    "route's commission entry cannot alter a step list a test asserts on.",
    "**The naive alternative is argued against honestly.** Its warehouse copy "
    "is still correct, so the case is drift rather than incompetence, and its "
    "two bugs are pinned by *passing* tests that assert the wrong behaviour.",
],
),

"state": dict(
purpose="""
Teach replacing a status field and its conditionals with one class per state,
so that the behaviour of an object changes with the state it is in -- and
teach, just as firmly, what separates State from Strategy when the two have
identical class diagrams, and when an enum is the better answer.
""",
nongoals=[
    "Not Strategy, although the class diagram is the same one. The notes, the "
    "diagrams and the video all say so explicitly rather than pretending a "
    "structural difference exists: a Strategy is chosen by the caller and "
    "does not change itself, while a State is entered as a consequence of "
    "what the object did, and states hand control to one another.",
    "Not a claim that every status field wants this. The demo's final section "
    "says out loud that for a small, stable machine an enum plus a map of "
    "permitted transitions is often clearer, and that the pattern earns its "
    "keep only when the behaviour varies by state rather than the permissions.",
    "Not a workflow engine. Seven states, six requests, one process. "
    "Persistence, retries, timers, parallel branches and distributed "
    "coordination are all out of scope.",
    "Not stateful state objects. Every state here is stateless and shared as "
    "a single INSTANCE, which is a property of this domain rather than of the "
    "pattern, and the notes flag what changes when a state needs a field.",
],
problem="""
An order in an online shop moves through a small, well understood lifecycle --
`PLACED`, `PAID`, `PACKED`, `SHIPPED`, `DELIVERED`, plus the terminal
`CANCELLED` and `REFUNDED` -- and six things can be asked of it: pay, pack,
ship, deliver, cancel and refund. The answer to every one of them depends on
where the order currently is, and cancelling in particular is not one rule
with a guard on it: cancelling a `PLACED` order moves no money, cancelling a
`PAID` one refunds, cancelling a `PACKED` one refunds *and* returns stock
somebody has already boxed, and cancelling a `SHIPPED` one is not a thing that
can be done at all.

Written the obvious way, that is an enum and a chain of conditionals at the
top of each method -- short, readable, and with the whole lifecycle in one
file. But the rules are then written down once per method, each copy phrased
in whichever direction its author found natural, and the copies drift.
`cancel` was written as "anything that has not arrived yet", which reads
sensibly and quietly includes `SHIPPED`, so a parcel on a van is refunded.
`refund` was widened to accept `CANCELLED` so support could sort out cancelled
orders, and since a cancel has already refunded, it pays the customer a second
time and leaves the ledger at `-£97.49` over two refunds. A third copy, the
`switch` written for the screen, is correct -- so the cancel button is never
drawn and the endpoint accepts the call anyway.

**What the pattern must deliver:** one class per state holding everything true
about that state; refusal as the default, so a rule nobody wrote is a refusal
rather than an accident; a context with no conditional that mentions a status;
one answer that the screen and the endpoint cannot disagree about; and a new
state that can be added without editing the context.
""",
roles=[
    ("Context", "`Order`"),
    ("State interface", "`OrderState` -- six requests, every default throws"),
    ("Concrete states",
     "`PlacedState`, `PaidState`, `PackedState`, `ShippedState`, "
     "`DeliveredState`, `CancelledState`, `RefundedState`"),
    ("Transition hook", "`Order.transitionTo` -- package-private"),
    ("Refusal", "`IllegalTransitionException`, built from `allowedActions()`"),
    ("Evidence", "`Ledger`, `OrderEvent` history"),
    ("Naive alternative", "`NaiveOrder`"),
    ("Supporting types", "`Money`, `OrderLine`"),
    ("Entry point", "`OrderStateDemo`"),
],
requirements=[
    "**Every request on the interface refuses by default.** A state lists "
    "what it allows by overriding, and everything else throws without a line "
    "of code being written -- so the mistake made when nobody is paying "
    "attention closes a transition rather than opening one, which is the "
    "exact opposite of the enum's failure mode.",
    "**The context contains no conditional that mentions a status.** Every "
    "public method on `Order` is a single delegation, and `transitionTo` is "
    "package-private so an order's state can change only as a consequence of "
    "asking it to do something.",
    "**States do genuinely different work for the same verb.** `cancel` "
    "refunds nothing in `PlacedState`, refunds in `PaidState`, and refunds "
    "and returns stock in `PackedState`. If the states differed only in what "
    "they permitted, the project would be an over-engineered enum and would "
    "say so.",
    "**The buttons and the endpoints cannot disagree.** `allowedActions()` "
    "lives on the state beside the methods it describes, and a test walks all "
    "seven states and all six actions checking that `canDo` predicts whether "
    "the call throws.",
    "**A refusal explains itself from the state's own data**, so the message "
    "cannot go stale: the reason is built from `allowedActions()`, except "
    "where a state overrides `cancel` purely to give a human a better one.",
    "**The naive alternative is argued against honestly.** Its happy path is "
    "still correct, so the case is drift rather than incompetence; its two "
    "bugs are pinned by *passing* tests that assert the wrong behaviour, each "
    "paired with the same scenario refused by the state version.",
    "**The cost is stated, not hidden.** Seven classes where there was one "
    "enum, and a transition table that no longer exists anywhere readable -- "
    "the demo's final section and the notes both recommend the enum for a "
    "small, stable machine.",
],
),

"chain-of-responsibility": dict(
purpose="""
Teach turning a fixed sequence of checks into a set of independent links that
are assembled at runtime, so that which checks run, in what order, and what
happens when none of them speaks up all become wiring rather than control
flow -- and teach the cost of that honestly, because a request can travel the
whole chain and come out unanswered.
""",
nongoals=[
    "Not Decorator, although both are objects holding a reference to the next "
    "object. The explainer states the distinguishing question rather than "
    "observing a resemblance: a decorator always delegates onward and adds "
    "something on the way, so every layer runs, while a handler may answer "
    "and stop, so the layers behind it never run at all.",
    "Not a claim that four checks always want this. The demo's final section "
    "and the notes say plainly that when the set of checks and their order "
    "never change, four sequential `if` statements are the right answer and "
    "are easier to read.",
    "Not a rules engine, a workflow engine or a DSL. The chain is assembled "
    "in Java, in code a reader can see, and there is no configuration file, "
    "no scripting and no dynamic dispatch by name.",
    "Not a validation framework. Nothing here accumulates a list of every "
    "problem with a request -- the first link that decides ends the run, "
    "which is the behaviour the pattern is for and the reason a validator "
    "that must report all errors should not be built this way.",
],
problem="""
Before an order is accepted it is screened: the address has to be somewhere a
courier goes, the warehouse has to be able to pick every line, the risk score
has to be under threshold, and the issuer has to be willing to authorise the
total on that card. Written the obvious way that is one `validate` method with
four checks and an early return on each, which is short, readable, and has the
whole policy in one file.

Three things go wrong once it is real, and all three cost money. **The order is
welded in.** The card is checked above fraud, so an order scoring 92 out of 100
is rejected as a card problem -- the customer is invited to try another card
and does, and the fraud team never hears the account exists. **There is no
third answer.** The result is a boolean, so the review band the risk model was
bought for has to be forced into yes or no, and it is accepted. **Variants are
copies.** Trade accounts are invoiced rather than charged, so the method was
copied and the card check deleted; the address check went with it in the same
edit, and two desks are now shipped to an island no courier serves.

**What the pattern must deliver:** one class per check, testable without
constructing the state the checks above it demand; the order of the checks as a
line of wiring rather than a line of control flow; a variant flow built by
leaving a link out rather than by copying a method; evidence of which link
decided and which links never ran; and a deliberate, named answer to the
question of what a chain means when nobody decides.
""",
roles=[
    ("Handler", "`ScreeningHandler` -- holds its successor, walks the chain in a `final` method"),
    ("Concrete handlers",
     "`AddressCheck`, `StockCheck`, `FraudScoreCheck`, `PaymentLimitCheck`"),
    ("Chain / client", "`ScreeningChain` -- assembles links and names the fallback"),
    ("Request", "`CheckoutRequest` -- immutable, never mutated by a link"),
    ("Answer", "`Decision`, `Outcome` -- approved, rejected, or referred to a human"),
    ("Evidence", "`ScreeningReport` -- who decided, and which links never ran"),
    ("Naive alternative", "`NaiveScreening`, and its nested `Result`"),
    ("Supporting types", "`BasketItem`"),
    ("Entry point", "`CheckoutScreeningDemo`"),
],
requirements=[
    "**Walking the chain is written once.** `ScreeningHandler.screen` is "
    "`final`, so a subclass cannot forget to call the next link -- which is "
    "the classic bug in the textbook version of this pattern, where a handler "
    "declines to handle something, omits the `else`, and the request "
    "disappears without an error.",
    "**A link is not obliged to reject.** `FraudScoreCheck` can reject, refer "
    "or say nothing, and the base class knows about none of those answers -- a "
    "link stops the chain whenever it is willing to own the answer, whatever "
    "that answer is.",
    "**No link knows the shape of the chain.** There is no index, no count "
    "and no loop over handlers anywhere; the chain hands the request to the "
    "first link and the links do the rest, which is what makes reordering a "
    "wiring change.",
    "**Falling off the end is dealt with deliberately.** The fallback "
    "decision is a required constructor argument and there is no constructor "
    "that omits it, so the wiring has to say out loud whether an unclaimed "
    "order fails open or fails closed rather than leaving it a `null`.",
    "**The interaction is visible, not just the verdict.** Every report "
    "prints the links consulted in order, what each said, who decided, and -- "
    "the part four sequential `if` statements can never give you -- which "
    "links never ran at all.",
    "**Each link is testable in a chain of one.** Exercising the fraud "
    "thresholds needs no deliverable address, no stocked basket and no card "
    "with headroom; the tests demonstrate the contrast against the naive "
    "method, where the fraud rule is only reachable by satisfying the three "
    "statements above it.",
    "**The naive alternative is argued against honestly.** Its happy path is "
    "correct and its author was not careless, so the case is drift; its bugs "
    "are pinned by *passing* tests that assert the wrong behaviour, each "
    "paired with the same scenario put through a chain.",
    "**The cost is stated, not hidden.** The order of the checks now lives in "
    "the wiring rather than in one readable method, answering \"which link "
    "rejected this?\" requires the report, and a handler instance belongs to "
    "exactly one chain -- the demo's closing lines say so and recommend the "
    "four `if` statements when the checks never change.",
],
),

"iterator": dict(
purpose="""
Teach handing out a small object that remembers where a caller has got to, so
that walking an awkward collection is written once instead of once per caller
-- and teach the split the pattern turns on, which is that the collection
knows what is in it and the iterator knows where you are, in two different
objects, with no exceptions.
""",
nongoals=[
    "Not an argument for wrapping a `List`. A `List` already has an "
    "iterator, and the notes say plainly that writing another one around it "
    "is ceremony; the pattern earns its keep here because the storage is "
    "paged, and the explainer names the other cases -- trees, streams of "
    "lines, sequences with no end -- rather than implying it is always "
    "worthwhile.",
    "Not a streams tutorial, and not an argument against streams. The "
    "comparison section places index loops, iterators and streams side by "
    "side and states explicitly that streams are built on this pattern "
    "rather than being an alternative to it. `java.util.stream` is not "
    "imported anywhere in the project.",
    "Not a lesson in generics. `Iterable<Product>` and `Iterator<Product>` "
    "are read, never written; no class in the project declares a type "
    "parameter, because a beginner should not have to learn generic class "
    "declarations to learn this pattern.",
    "Not concurrency. `ConcurrentModificationException` gets one mention in "
    "the pitfalls and nothing more; there are no threads, no fail-fast "
    "modification counting, and no synchronisation anywhere.",
    "Not a real paged API. `CatalogueFeed` fakes the warehouse with a list "
    "and a counter, so there is nothing to install, connect to or stub -- "
    "the counter is the point, because it turns laziness into something a "
    "test can assert.",
],
problem="""
The shop's catalogue does not live in the application. It lives in the
warehouse system, which hands products over three at a time: you ask for page
zero, then page one, and you know you have reached the end when a page comes
back empty. There is no `size()` and no `hasMorePages()`. Everything else a
caller might want, it works out by hand, in a loop.

`NaiveCatalogueBrowser` is what that looks like after three people have each
needed to walk the catalogue. Three methods, three hand-written copies of the
same page loop, and two of them are wrong. `countProducts()` hard-codes three
pages, so it is correct today and silently under-counts on the day a tenth
product is added. `findCheapest()` starts its page counter at one instead of
zero, never looks at page zero, and so never sees the four-pound socks -- it
returns the eight-pound Coffee Mug, which is a real product at a real price,
correctly formatted, and not the cheapest thing in the shop. Neither bug
throws, neither is logged, and both can live in production indefinitely.

**What the pattern must deliver:** the page loop written exactly once, in a
class with a name that can be tested on its own; a catalogue that can be used
in a `for`-each loop without any caller naming a page; fetching that happens
only when a caller actually reaches the page, so stopping early costs nothing;
and two simultaneous walks over one catalogue that do not disturb each other.
""",
roles=[
    ("Aggregate", "`java.lang.Iterable` -- not written here; the JDK's"),
    ("Iterator", "`java.util.Iterator` -- not written here either"),
    ("Concrete aggregate",
     "`ProductCatalogue` -- holds the feed, and no position at all"),
    ("Concrete iterator",
     "`CatalogueIterator` -- package-private; every field on it is position"),
    ("Awkward storage",
     "`CatalogueFeed` -- pages of three, and a counter of pages fetched"),
    ("Element", "`Product` -- a record"),
    ("Naive alternative", "`NaiveCatalogueBrowser` -- three methods, three loops"),
    ("Entry point", "`CatalogueDemo`"),
],
requirements=[
    "**The page loop exists once.** `CatalogueIterator.hasNext` is the only "
    "place in the project that increments a page number or knows that an "
    "empty page means the end. Nothing else -- not the catalogue, not the "
    "demo, not any test -- contains a second copy.",
    "**The aggregate holds no position.** `ProductCatalogue` has one field, "
    "the feed. It has no page number, no index and no `next()`, and "
    "`iterator()` returns a new instance on every call rather than a cached "
    "one, which is what makes two simultaneous walks possible.",
    "**Fetching is lazy, and the build proves it.** `CatalogueFeed` counts "
    "its own calls, so the tests can assert that creating an iterator fetches "
    "nothing and that consuming two products fetches exactly one page of "
    "three. Moving the first fetch into a constructor turns that test red.",
    "**Two iterators do not interfere.** A test advances one iterator over a "
    "catalogue and asserts the other is still at the first product. This is "
    "the test that catches the most common first-attempt mistake, which is "
    "putting the position on the aggregate.",
    "**`hasNext()` is safe to call repeatedly.** It consumes nothing, so "
    "calling it twice in a row returns the same answer and skips no element; "
    "`next()` calls it rather than trusting the caller, and throws "
    "`NoSuchElementException` with a readable message at the end.",
    "**The caller never names a page.** The demo's second section is a plain "
    "`for`-each loop, and the word `page` does not appear in it. Crossing a "
    "page boundary is invisible from outside the iterator.",
    "**The naive alternative is argued against honestly.** Its `allProducts` "
    "method is correct and its author was not careless; the case against it "
    "is that the loop was written three times and so could be got wrong three "
    "ways. Both bugs are pinned by *passing* tests that assert the wrong "
    "behaviour, each paired with the same question put through the iterator.",
    "**The cost is stated, not hidden.** The notes say that over an "
    "`ArrayList` this pattern is pure ceremony, that a `hasNext()` which "
    "consumes is a real and easy bug, and that `remove()` is left "
    "unimplemented on purpose -- with an explanation of what it would have to "
    "do to work against a paged source.",
],
),

"mediator": dict(
purpose="""
Teach moving the rules about how a group of objects affect one another out of
the objects themselves and into one hub, so that the wiring grows with the
number of parts rather than with the square of it -- and teach the honest
consequence, which is that the hub becomes the one class that knows the whole
page and has to be kept from turning into a god object.
""",
nongoals=[
    "Not a GUI tutorial. There is no window, no toolkit and no event loop: "
    "the widgets are plain objects holding a value, and the demo prints to "
    "the console, so nothing about the lesson depends on Swing, Android or a "
    "browser.",
    "Not Observer, and not an argument against it. The comparison section "
    "puts the two side by side -- Observer broadcasts a fact to whoever "
    "subscribed, Mediator decides what a change means -- and says plainly "
    "that a page can use both.",
    "Not an event bus, a message broker or a framework. The mediator is one "
    "interface with one method, and the project never suggests reaching for "
    "infrastructure to get the same decoupling.",
    "Not an argument that objects must never reference each other. The notes "
    "recommend two controls wired directly when there really are only two, "
    "and name the point -- roughly the third rule -- at which the hub starts "
    "paying for itself.",
],
problem="""
A checkout page has five controls: a country selector, a shipping selector, a
gift-wrap checkbox, a total, and a Place Order button. Four rules tie them
together. The country decides which couriers are offered; the country decides
whether gift wrapping is available at all; the courier and the gift wrap both
move the total; and the button is enabled only once a country and a courier
are both chosen.

`NaiveCheckoutForm` is what that looks like when each rule is added on its own
day, by whoever needed it. Five controls hold nine references to one another,
two of them mutual, and no single file contains the behaviour of the page.
Two bugs follow from that arrangement rather than from carelessness. Changing
the country to one that cannot be gift wrapped withdraws the option but leaves
the tick where it was, so the form charges two pounds for wrapping that will
not happen -- a total of forty-two pounds that is wrong in a way no exception
will ever mention. And the country selector, having reshaped the courier list,
never re-checks the button, so Place Order stays enabled with no courier
selected.

**What the pattern must deliver:** every rule about the page in one readable
method; controls that hold a reference to the hub and to nothing else, so the
tangle is not merely absent but unrepresentable; a form whose behaviour can be
asserted without constructing any user interface; and wiring that stays linear
as controls are added.
""",
roles=[
    ("Mediator", "`CheckoutMediator` -- one method, `changed(FormWidget)`"),
    ("Concrete mediator",
     "`CheckoutForm` -- the rules of the page, all of them, in `changed`"),
    ("Colleague",
     "`FormWidget` -- a name and a mediator, and deliberately nothing else"),
    ("Concrete colleagues",
     "`CountrySelector`, `ShippingSelector`, `GiftWrapCheckbox`, "
     "`TotalLabel`, `PlaceOrderButton`"),
    ("Naive alternative",
     "`NaiveCheckoutForm` -- nine references on five controls, in one file"),
    ("Entry point", "`CheckoutFormDemo`"),
],
requirements=[
    "**No colleague holds another colleague.** `FormWidget` has two fields, a "
    "name and a mediator. `WidgetIsolationTest` walks every widget's declared "
    "fields by reflection and fails naming the offender, so the constraint is "
    "enforced by the build rather than promised by a comment.",
    "**Every rule lives in one method.** `CheckoutForm.changed` is the only "
    "place in the project that knows the country reshapes the courier list, "
    "that gift wrap is domestic-only, or that the button needs both. Reading "
    "it is reading the page.",
    "**The refreshes are unconditional.** `changed` recomputes the total and "
    "the button on every change rather than trying to work out which of them "
    "the change could have affected. That is what makes the naive form's "
    "forgotten re-check structurally impossible rather than merely fixed.",
    "**The mediator pushes; colleagues do not pull.** Every method the "
    "mediator calls on a widget is package-private and announces nothing, so "
    "a widget cannot ask the mediator a question and cannot start a cascade "
    "by being updated.",
    "**A widget's own change announces itself once.** Setting a value calls "
    "`mediator.changed(this)` and stops; no widget works out what its change "
    "means, because none of them can see far enough to know.",
    "**The naive alternative is argued against honestly.** Nobody sat down "
    "and decided to write nine references; each was added alone, for a good "
    "reason, on a different day. Both of its bugs are pinned by *passing* "
    "tests that assert the wrong behaviour -- the forty-two pound total and "
    "the enabled button -- each paired with the same interaction put through "
    "the mediator.",
    "**The arithmetic is stated.** The notes give the growth curve directly: "
    "up to n(n-1) relationships wired directly against n through a hub, with "
    "the three-, five- and ten-control rows written out, because the curve "
    "matters more than any single line of the tangle.",
    "**The cost is stated, not hidden.** The mediator is the one class that "
    "knows everything, and the notes say what to do when that class grows too "
    "large, name the god-object risk out loud, and recommend wiring two "
    "controls directly when there really are only two.",
],
),

"memento": dict(
purpose="""
Teach saving an object's state so it can be put back later, without opening the
object up to do it -- and teach the half of the definition that beginners skip,
which is that the thing holding the copy must still be unable to see inside it.
""",
nongoals=[
    "Not serialization or storage. Snapshots are ordinary objects held in "
    "memory; `Serializable`, JSON, files and databases appear nowhere, "
    "because none of them are needed to make the point.",
    "Not Command, and not an argument against it. The comparison section "
    "places the two side by side -- state before the change against the "
    "operation and its inverse -- and states when Command is the better "
    "trade, which is when the state is large and the operations invert "
    "cleanly.",
    "Not a deep-copy tutorial. The copy here is shallow and safe, and the "
    "notes say exactly what makes it safe (`BasketLine` is a record) and what "
    "would silently make it unsafe, rather than teaching a cloning recipe.",
    "Not concurrency, and not a transaction manager. There are no threads and "
    "no rollback machinery; database transactions get one line in the "
    "\"where you have seen it\" list and nothing more.",
],
problem="""
A shopper's basket holds two things: its lines, and a voucher code worth five
pounds off the whole order. The ticket says add an undo button, because
shoppers keep removing the wrong line and then have to go and find the product
again.

`NaiveBasket` is the obvious afternoon's work, and it is wrong twice.
`savedLines = lines` records where the list is rather than what is in it, so
the save and the live basket are one list under two names; undo then clears the
list it was about to restore from, and the shopper's basket comes back empty
with no exception and nothing in the log. And the voucher is not saved at all
-- not because anyone decided against it, but because it was not on anybody's
mind on the day undo was written, which is a class of bug no code review can
catch, since the defect is the absence of a line.

The obvious repair is worse than the bug: making the basket's fields public so
the undo code can copy them buys one feature at the cost of the basket's
encapsulation, permanently.

**What the pattern must deliver:** a complete copy of the basket's state, taken
by the basket itself; a history that can stack those copies and hand them back
without ever being able to read one; undo that keeps working when a field is
added, by editing two methods and nothing else; and the basket's fields exactly
as private afterwards as they were before.
""",
roles=[
    ("Originator",
     "`Basket` -- the only class that writes a snapshot or reads one back"),
    ("Memento",
     "`BasketSnapshot` -- a sealed copy; public outside, opaque inside"),
    ("Caretaker",
     "`BasketHistory` -- a capped stack of snapshots it cannot open"),
    ("Element", "`BasketLine` -- a record, and that is load-bearing"),
    ("Naive alternative",
     "`NaiveBasket` -- an alias for a copy, and a forgotten voucher"),
    ("Entry point", "`BasketUndoDemo`"),
],
requirements=[
    "**The snapshot copies.** `BasketSnapshot`'s constructor calls "
    "`List.copyOf`, so a snapshot is a photograph rather than a window. A "
    "test empties the basket completely *after* taking a snapshot and then "
    "restores, which is the aliasing bug written as an assertion.",
    "**The narrow interface is enforced by the build.** `label()` is public; "
    "`lines()`, `voucher()` and the constructor have no modifier at all, so "
    "only `Basket` can use them. `SnapshotEncapsulationTest` walks the "
    "class's declared methods by reflection and fails naming any public one "
    "outside a short allowed list.",
    "**One place knows what the state is.** `Basket.save` and "
    "`Basket.restore` are the only six lines in the project aware that a "
    "basket has lines and a voucher; adding a field means editing them and "
    "nothing else.",
    "**The caretaker never opens an envelope.** `BasketHistory` pushes "
    "snapshots, pops them, hands them to the basket and reads the label. It "
    "does its entire job without knowing that a basket contains anything.",
    "**Restore does not consume.** `restore` reads a snapshot without "
    "changing or discarding it, so the same one can be restored twice -- "
    "which is what makes redo an addition of about ten lines rather than a "
    "rewrite.",
    "**The naive alternative is argued against honestly.** Its two methods "
    "look like opposites and its author was not careless. Both failures are "
    "pinned by *passing* tests that assert the wrong answers -- the empty "
    "basket and the voucher that does not come back -- so the cost of the "
    "alternative is stated by the build rather than claimed by a README.",
    "**The memory cost is stated, not hidden.** Every snapshot is a full "
    "copy, `BasketHistory` caps the stack at twenty for exactly that reason, "
    "and the notes say that Command is the better trade when the state is "
    "genuinely large.",
    "**The shallow copy is explained rather than assumed.** The notes state "
    "the rule in both directions: immutable parts make a shallow copy safe, "
    "mutable parts make it a bug waiting to be found -- and warn that "
    "snapshotting after the change instead of before makes every undo one "
    "step off, which looks like the pattern failing when it is the caller.",
],
),

"interpreter": dict(
purpose="""
Teach writing one small class for each kind of phrase in a tiny language, so
that a promotion rule becomes a line of text an editor can change rather than a
branch that needs a release -- and teach the sentence beginners skip, which is
that this pattern is only affordable while the language stays small.
""",
nongoals=[
    "Not a parser tutorial. `RuleParser` is two string splits and a `throw`, "
    "it is labelled as not part of the pattern everywhere it appears, and the "
    "one exercise that asks for brackets is deliberately unfinishable so the "
    "limit is felt rather than asserted.",
    "Not a rules engine, and not an argument against one. The notes say "
    "plainly that production shops often buy one, and that this project is "
    "what such a thing looks like on the inside.",
    "Not Composite, although it is built from one. The comparison section "
    "states that the difference is intent rather than structure: Composite is "
    "about treating one thing and many things alike, Interpreter is about "
    "meaning.",
    "Not a claim that an `if` is wrong. Three settled promotions are better "
    "written as three branches, and the explainer says so before it says "
    "anything else.",
],
problem="""
An online shop runs promotions, and a promotion is three things: a code, a
percentage, and a rule about who qualifies. Written in Java the first one is
four lines, and there is nothing wrong with it. The trouble arrives with the
fourth, because by then each new offer is written by copying the one above it
and changing the numbers, which is the fastest correct-looking thing anybody
can do.

`NaiveVoucherRules` is that shop, and it is wrong in both directions at once.
SAVE15 was ticketed as fifteen percent on UK baskets over a hundred pounds, but
the UK part sat in the paragraph above the sentence somebody read, so no line
was ever written for it and every large overseas order now takes fifteen
percent off. FREESHIP was copied from a welcome offer that retired last spring
and kept its `firstOrder()` test, so a returning UK shopper with three items is
offered nothing -- and nobody reports that one, because a missing discount
looks exactly like a shopper who did not qualify. Neither bug throws, neither
is logged, and both passed review.

Underneath the two bugs is one structural fact: a rule change is a code change.
Moving fifty pounds to seventy-five is a branch, a pull request, a review and a
release, written by somebody who did not read the campaign brief, and the
people who own the offers cannot read the version that actually runs.

**What the pattern must deliver:** promotion rules as text the shop's own staff
can read and write; a rule that can be evaluated against an order and can also
say what it says, in the words it was written in; a new kind of condition added
without touching any existing rule class; a typo refused when the promotion is
saved rather than when an order is priced; and an honest statement of where the
arrangement stops paying.
""",
roles=[
    ("Abstract expression",
     "`Rule` -- two methods, `matches(Order)` and `describe()`, no fields"),
    ("Terminal expressions",
     "`BasketOver`, `CountryIs`, `ItemsAtLeast`, `FirstOrder` -- one "
     "comparison each, and no rule inside"),
    ("Non-terminal expressions",
     "`AndRule`, `OrRule`, `NotRule` -- hold other rules and answer by "
     "asking them"),
    ("Context", "`Order` -- basket total, country, item count, first order"),
    ("Client-side parser",
     "`RuleParser` -- builds the tree, and is not part of the pattern"),
    ("Holder", "`Promotion` and `PromotionBook` -- a code, a percentage, "
     "and a rule as text"),
    ("Naive alternative",
     "`NaiveVoucherRules` -- one branch per offer, copied from the one above"),
    ("Entry point", "`VoucherRuleDemo`"),
],
requirements=[
    "**Two kinds of class, and no third.** Every rule implements `Rule`; the "
    "terminals hold values and the non-terminals hold rules. The class "
    "diagram shows exactly one aggregation looping back into `Rule`, and that "
    "loop is the whole of the recursion.",
    "**Only the leaves read the context.** `AndRule` and `OrRule` never touch "
    "an `Order`; they ask their parts and combine the answers, which is why a "
    "whole other tree drops into either slot without a line changing.",
    "**A rule can say what it says.** `describe()` walks the same nodes as "
    "`matches` and rebuilds the sentence from the objects rather than "
    "remembering the line that was read in, and "
    "`parsingAndDescribingRoundTrip` asserts it -- so the audit log and the "
    "tree the checkout obeys cannot drift apart.",
    "**The grammar is asserted, not assumed.** `andBindsTighterThanOr` pins "
    "the precedence that falls out of splitting on `or` first, so the "
    "exercise that swaps the two splits fails the build instead of quietly "
    "changing what every promotion in the shop means.",
    "**A typo is refused on Wednesday.** `RuleParser` does not guess: it "
    "names the phrase it cannot read and throws while the promotion is being "
    "saved. The contrast is stated explicitly -- a mistyped Java condition is "
    "valid Java, and misprices an order on Friday.",
    "**Adding a condition touches nothing that exists.** A new terminal is "
    "one record and one `if` in the parser; the session guide has the room "
    "do it and then asks what the same change would have been in "
    "`NaiveVoucherRules`.",
    "**No fact about eligibility lives in code.** `PromotionBook` mentions no "
    "country, no basket threshold and no item count; every such fact is a "
    "line of text, which is the point of the whole exercise.",
    "**The naive alternative is argued against honestly.** Both of its bugs "
    "are pinned by *passing* tests that assert the wrong answers, so the cost "
    "is stated by the build rather than claimed by a README.",
    "**The limit is stated as plainly as the benefit.** One class per phrase "
    "is fine for seven phrases and unbearable for seventy; the parser is the "
    "part that grows; every node is an object and every evaluation a virtual "
    "call; and when the rules never change, two `if` statements are the "
    "better code.",
],
),

"visitor": dict(
purpose="""
Teach separating an operation from the structure it runs over, so that a new
report on the product catalog is a new class rather than a new method on every
node type -- and teach the price of that separation just as plainly, because
the same arrangement makes a new node type expensive on every report that
already exists.
""",
nongoals=[
    "Not Composite. The catalog tree is borrowed wholesale from "
    "`structural/composite-pattern` and the project links back to it; nothing "
    "here teaches how to build the tree, only what to do with one you already "
    "have.",
    "Not an argument that a method on the node is wrong. The demo's own "
    "inventory report is correct in both designs and agrees to the penny, and "
    "the notes recommend writing the method directly when the operations are "
    "few and settled.",
    "Not a general substitute for pattern matching. The explainer states when "
    "a `switch` over sealed types is the better answer and does not pretend "
    "the double dispatch is more readable than it is.",
],
problem="""
An online shop's catalog is a tree of categories, products and bundles, and it
has been the same three node types for years. What is not settled is what the
business asks about it: the value of the stock, the number of lines in each
category, a CSV export for finance every Monday, and a compliance audit naming
the items that cannot travel by air. Written the obvious way each of those is a
method on every node class, so a class describing a thing on a shelf ends up
carrying an RFC 4180 quoting rule, the bundle class copied from the product
class eighteen months later drops the quoting and reads a restriction field it
never sets, and the fifth report is a fifth method on three finished classes.
The pattern has to let a report be added without opening a model file, keep one
traversal rather than one per report, give a bundle a different rule from a
product without a type test, and state out loud what a new node type would
cost.
""",
roles=[
    ("Element", "`CatalogComponent` -- `name()` and `accept(CatalogVisitor)`, and nothing else"),
    ("Concrete elements", "`Product`, `Bundle`, `Category` -- each `accept` is one line"),
    ("Composite element", "`Category` -- owns the only traversal in the project"),
    ("Visitor", "`CatalogVisitor` -- one `visit` per node type, plus a `leave(Category)` default"),
    ("Concrete visitors",
     "`InventoryValueVisitor`, `CategoryCountVisitor`, `CsvExportVisitor`, "
     "`ComplianceAuditVisitor`, `DispatchTraceVisitor`"),
    ("Convenience base", "`CategoryPathVisitor` -- path tracking, and explicitly not part of the pattern"),
    ("Naive alternative", "`NaiveCatalogNode`, `NaiveProduct`, `NaiveBundle`, `NaiveCategory`"),
    ("Supporting types", "`Money`, `Restriction`, `Catalog`"),
    ("Entry point", "`CatalogReportDemo`"),
],
requirements=[
    "**The model carries no reporting method.** `CatalogComponent` declares "
    "`name()` and `accept` only, and a reflection test with an allow-list "
    "fails the build if a report method is ever added back onto `Product`.",
    "**A report written later needs no change to anything.** A visitor "
    "declared inside the demo file and another declared inside a test method "
    "both walk a tree whose classes were compiled without them, and the "
    "demo's fifth report changes no interface, no node type and no other "
    "report.",
    "**The traversal is written once and lives in the structure.** "
    "`Category.accept` is the only loop over children in the project; a "
    "visitor containing no loop and no recursion still receives all 17 calls "
    "of the demo tree, and that is asserted rather than asserted about.",
    "**No visitor performs a type test.** There is no `instanceof` and no "
    "`switch` on node type in any report; each node calls `visitor.visit(this)` "
    "from inside its own class, and the demo's dispatch section shows the two "
    "hops interleaving.",
    "**A third node type earns the double dispatch.** `Bundle` is worth its "
    "kit price rather than the sum of its parts, and is restricted by what is "
    "in the box rather than by a field of its own, so `visit(Bundle)` and "
    "`visit(Product)` state materially different rules in every report that "
    "cares.",
    "**The naive alternative is argued against honestly.** Its inventory "
    "total agrees with the visitor to the penny, and its two bugs -- the "
    "dropped CSV quoting and the unset copied `restriction` field -- are "
    "pinned by *passing* tests, each paired with the visitor answering the "
    "same question correctly.",
    "**The cost is runnable, not rhetorical.** The demo's final section "
    "prints the class names a single new node type would break, the notes "
    "state that adding a node type breaks every visitor, and the awkwardness "
    "of `node.accept(v)` calling `v.visit(node)` straight back is named "
    "rather than defended.",
    "**The pruning limitation is asserted.** A report wanting only one branch "
    "is offered every node in the tree and filters, because the walk belongs "
    "to the structure; a test pins the 7-offered-against-5-wanted numbers.",
],
),
"api-gateway": dict(
purpose="""
Teach why a client that talks to many services should talk to one service
instead, and what that one service is allowed to do -- route, join, check the
token once -- as against what it must never start doing, which is thinking.
""",
nongoals=[
    "Not an HTTP server. Nothing binds a port; a remote call is a "
    "`RemoteCall` that advances a simulated clock and writes a line into a "
    "timeline.",
    "Not a proof that the page is correct. Both versions of the app return "
    "the same product page, so any test asserting the page's contents would "
    "pass on the naive version too and prove nothing.",
    "Not business logic. The gateway must not price, discount or decide -- "
    "the moment it does, it is a second copy of the shop, and a test pins the "
    "price it publishes to Pricing's answer unmodified.",
    "Not a distributed system. One JVM, no mesh, no partitions, no capacity "
    "planning; what the project teaches is the pattern's shape.",
],
problem="""
The shop's mobile app shows a product page, and that page is made of four
services' worth of information: the name from Catalog, the price from Pricing,
availability from Inventory, and "customers also bought" from
Recommendations.

The obvious app calls all four itself, and it works. It is also four network
crossings from a phone on a train instead of one, four token checks instead of
one, and -- the expensive part -- it loses the entire product page on the day
Recommendations goes down, because a feature nobody would miss is wired into
the page with the same importance as the price.

**What the pattern must deliver:** the phone makes one call. Behind that call,
the four services are asked in parallel, the token is checked once, and a
failure in an optional service costs its own section of the page and nothing
else.
""",
roles=[
    ("Gateway", "`ProductPageGateway`"),
    ("Naive client", "`NaiveMobileApp`"),
    ("Client", "`MobileApp`"),
    ("Downstream services", "`AuthService`, `CatalogService`, `PricingService`, `InventoryService`, `RecommendationsService`"),
    ("Service registry for the demo", "`StoreServices`"),
    ("Response", "`ProductPage`"),
    ("Simulation harness", "`SimulatedClock`, `RemoteCall`, `CallLog`, `ServiceUnavailableException`"),
    ("Entry point", "`ProductPageDemo`"),
],
requirements=[
    "**One crossing from the client.** A test counts the calls the phone "
    "makes and asserts one against the naive app's five.",
    "**The token is checked once.** `CallLog.countFor(\"Auth\")` is 1 for the "
    "gateway and 4 for the naive app.",
    "**Parallel, and the clock proves it.** The gateway's page arrives in "
    "240ms where the naive app's sequential calls take 800ms; both numbers "
    "are asserted against `SimulatedClock`, not measured.",
    "**An optional service failing degrades the page.** With "
    "Recommendations down the page still carries name, price and stock, and "
    "says it has no recommendations rather than pretending there are none.",
    "**An essential service failing fails honestly.** With Catalog down the "
    "gateway raises the failure rather than serving a page with a blank "
    "name.",
    "**The gateway adds no logic.** The published price equals Pricing's "
    "answer; the test exists to stop a future feature being put in the "
    "wrong place.",
],
),

"service-discovery": dict(
purpose="""
Teach that the address of a service is a runtime fact rather than a
configuration constant, and -- the half that matters -- that the list of
addresses is always a little bit wrong, so a caller must be written to survive
being handed a dead one.
""",
nongoals=[
    "Not Eureka, Consul or DNS. `ServiceRegistry` is a map with leases; the "
    "point is the contract those products implement, not their features.",
    "Not load balancing. Choosing *which* healthy instance to call is the "
    "next pattern; this one is about getting a list at all.",
    "Not health checking as a subsystem. A lease that expires when "
    "heartbeats stop is the whole health model here, deliberately.",
    "Not an argument that discovery removes the outage. It bounds the window "
    "and makes the bound a number you choose.",
],
problem="""
The shop's Pricing service runs as three instances. One is restarted during
every deployment, another is added on Black Friday morning, and one crashes at
some point because processes do.

A caller with `PRICING_URL` written into it has an outage every time that set
changes, while healthy instances sit idle, paid for and unreachable. Worse, the
failure is silent from the caller's side: it is holding an address that was
true when somebody typed it.

**What the pattern must deliver:** instances announce themselves on startup and
keep announcing; callers ask for a list at call time; and when the list is
wrong -- because a crashed instance never got to say goodbye -- the caller
works down it instead of trusting the first entry.
""",
roles=[
    ("Registry", "`ServiceRegistry`"),
    ("Registration", "`ServiceInstance`"),
    ("The instances", "`PricingCluster`"),
    ("Discovering client", "`DiscoveringPricingClient`"),
    ("Naive client", "`HardcodedPricingClient`"),
    ("Simulation harness", "`SimulatedClock`, `RemoteCall`, `CallLog`"),
    ("Entry point", "`ServiceDiscoveryDemo`"),
],
requirements=[
    "**A new instance is used without anybody deploying a caller.** "
    "Registering a fourth instance is visible to the very next lookup.",
    "**The hardcoded client breaks on the same event**, and its test says so "
    "by passing -- it fails when its one address is restarted.",
    "**A crashed instance is still on the list.** A test asserts the registry "
    "reports an instance that is not answering, because a crash cannot "
    "deregister.",
    "**The caller survives a stale address.** It tries the next instance and "
    "gives up only when the list is exhausted, logging `STALE` for the dead "
    "one.",
    "**The lease expires on the clock.** With a 3000ms lease and heartbeats "
    "stopped, the instance is listed at 2000ms and gone at 4000ms; the "
    "simulated clock makes that assertion exact.",
    "**The stale window is named as the cost**, in the demo output and the "
    "notes, together with why a shorter lease only trades it for traffic.",
],
),

"load-balancing": dict(
purpose="""
Teach that when a service runs as several identical copies, the decision of
which copy to call is a strategy the caller holds -- and that the choice
between those strategies is decided by what happens when one copy is sick, not
by which one spreads calls most evenly.
""",
nongoals=[
    "Not a load balancer appliance or an nginx configuration. The balancing "
    "here is client-side, which is where the pattern lives in a service mesh "
    "too.",
    "Not service discovery. The list of instances is a given; this project "
    "is about picking from it.",
    "Not a benchmark. The cluster's latencies are fixed and deliberately "
    "uneven so that the comparison is arithmetic rather than luck.",
],
problem="""
Catalog runs as three instances, and they are not equal: one is fast, one is
ordinary, one is on a bad host and answers slowly. A client that always calls
the first entry on the list sends every request to one instance, and if that
instance is the slow one, every customer sees the slow page while two healthy
machines idle.

**What the pattern must deliver:** an interface with one method -- choose an
instance -- and several implementations behind it, so the caller's code does not
change when the policy does. The demo must show what each policy actually
costs in milliseconds, and it must show two clients taking turns without
colliding.
""",
roles=[
    ("Strategy interface", "`LoadBalancer`"),
    ("Policies", "`RoundRobinBalancer`, `RandomBalancer`, `LeastLatencyBalancer`, `FirstInstanceBalancer`"),
    ("The instances", "`CatalogCluster`, `ServiceInstance`"),
    ("Client", "`CatalogClient`"),
    ("Simulation harness", "`SimulatedClock`, `RemoteCall`, `CallLog`"),
    ("Entry point", "`LoadBalancingDemo`"),
],
requirements=[
    "**Round-robin is exactly fair.** Nine calls across three instances give "
    "three each, asserted per instance rather than in aggregate.",
    "**Always-first is measurably worse**, and its own test class passes: it "
    "sends all nine calls to one instance and the total time says what that "
    "costs.",
    "**Least-latency tries everyone once.** No instance is written off "
    "unmeasured, and after the measuring round the fast instances take the "
    "majority of the traffic.",
    "**Two clients do not collide.** Each client keeps its own cursor, so "
    "two round-robin clients each take perfect turns -- which is also why "
    "client-side balancing is not global balancing, and the notes say so.",
    "**The pattern is named as Strategy.** The notes state that this is the "
    "behavioural pattern from project 15 applied to a network, so the reader "
    "meets one idea twice rather than two ideas once.",
],
),

"retry": dict(
purpose="""
Teach the two halves of retrying -- deciding *whether* a failure is worth
retrying, and waiting before the next attempt -- and the third thing nobody
does, which is making the operation safe to attempt twice.
""",
nongoals=[
    "Not Resilience4j. `Retrier` is about thirty lines; the value is in the "
    "policy decisions, not the library.",
    "Not a defence of retrying everything. Half the project is failures that "
    "must not be retried.",
    "Not idempotency in full -- the duplicate charge is shown here and "
    "solved in projects 36 and 37.",
],
problem="""
Checkout calls the payment gateway, and the gateway times out. Sometimes that
is a blip: a dropped packet, a restarting instance, a moment of GC, and the
same call a second later succeeds. Sometimes it is a declined card, which will
be declined every time, for ever.

A loop that retries both punishes the customer with three declines instead of
one, and a loop with no wait between attempts arrives back at a struggling
service at exactly the moment it is least able to answer.

**What the pattern must deliver:** retry only failures that might not happen
again, wait longer between each attempt, cap the attempts, and be honest about
the case where the call succeeded and the *reply* was lost -- because retrying
that one charges the card twice.
""",
roles=[
    ("Retry mechanism", "`Retrier`"),
    ("Policy", "`RetryPolicy`"),
    ("Client with retries", "`CheckoutService`"),
    ("Naive client", "`NaiveCheckoutService`"),
    ("Remote service", "`PaymentGateway`"),
    ("Failures", "`GatewayTimeoutException` (retryable), `CardDeclinedException` (not)"),
    ("Value objects", "`PaymentRequest`, `Receipt`, `Money`"),
    ("Entry point", "`RetryDemo`"),
],
requirements=[
    "**A transient failure is absorbed.** Two timeouts followed by a success "
    "produce one receipt and three attempts, and the caller sees no error.",
    "**A permanent failure is not retried.** A declined card is attempted "
    "exactly once; the test counts gateway calls, so a future change to the "
    "policy cannot quietly retry it.",
    "**The backoff is on the clock.** With a 100ms base and doubling, the "
    "third attempt starts at 300ms of waiting, asserted against "
    "`SimulatedClock` -- nothing sleeps.",
    "**Attempts are capped**, and the last failure is what the caller "
    "receives, not a wrapper that hides which call failed.",
    "**The duplicate charge is demonstrated, not mentioned.** A call that "
    "succeeds and loses its reply is retried and charges twice; the test "
    "asserts two charges and the notes name idempotency as the fix.",
],
),

"circuit-breaker": dict(
purpose="""
Teach a caller to stop calling a service that is already down -- and then teach
the harder half, which is deciding what to do during the outage, dependency by
dependency.
""",
nongoals=[
    "Not a replacement for retry. The two answer different questions, and the "
    "project states the question that separates them: is the next attempt "
    "plausibly going to work?",
    "Not a rate limiter or a timeout. The breaker's only input is the recent "
    "failure history of one dependency.",
    "Not an argument that every dependency deserves a fallback. One of this "
    "project's classes exists to show a fallback that must never be written.",
],
problem="""
The shop's Recommendations service stops answering, and each call sits for a
three-second timeout before giving up. A caller with retries makes that nine
seconds per shopper, and aims three times the traffic at a service that is
already on its knees. Ten shoppers is ninety seconds of waiting and thirty
calls into a hole.

Payments failing is the same mechanism with a completely different answer: there
is no substitute for taking the money, so nothing can be faked.

**What the pattern must deliver:** after a threshold of consecutive failures,
calls are refused without being made and cost nothing; after a cooling period
one probe is allowed through, and the breaker closes if it works; and each
dependency has an explicit answer to "what do we do while it is open?".
""",
roles=[
    ("Breaker", "`CircuitBreaker`, `BreakerState`, `CircuitOpenException`"),
    ("Degrading caller", "`ProductPageService`"),
    ("Naive caller", "`RetryingProductPageService`"),
    ("Refusing caller", "`CheckoutService`, `CheckoutUnavailableException`"),
    ("The fallback that must never be written", "`PretendItWorkedCheckoutService`"),
    ("Downstream services", "`RecommendationsService`, `PaymentsService`"),
    ("Response", "`ProductPage`"),
    ("Entry point", "`CircuitBreakerDemo`"),
],
requirements=[
    "**Retrying an outage is shown to be worse**, with its own passing test: "
    "ten shoppers cost 90,000ms of simulated time and thirty calls reach a "
    "service that is down.",
    "**The breaker opens on consecutive failures** -- three in a row -- and "
    "one success resets the count, because a service that answers three times "
    "and fails once is not down.",
    "**An open breaker is free.** Twenty pages served after the trip advance "
    "the simulated clock by zero milliseconds and make zero calls.",
    "**Half-open lets exactly one call through** after the cooling period, "
    "closes on success, and re-opens for a full wait on a single failed "
    "probe.",
    "**Both answers to the open state are implemented.** "
    "Recommendations is hidden behind a `degraded` flag on the page; "
    "Payments is refused honestly with zero cards charged.",
    "**The dishonest fallback is demonstrated and condemned.** "
    "`PretendItWorkedCheckoutService` returns a receipt while charging "
    "nothing; the test asserts a thanked shopper and zero charges, and the "
    "notes state that a fallback hiding a real failure is worse than the "
    "error it replaced.",
],
),

"bulkhead": dict(
purpose="""
Teach that two kinds of work drawing on one pool of threads means the slow kind
can starve the important kind, and that the fix is not a faster pool but a
refusal to share one.
""",
nongoals=[
    "Not a thread-pool tutorial, and not a performance exercise -- the "
    "partitioned version is deliberately slower overall.",
    "Not a circuit breaker. Nothing here is broken; the resource is simply "
    "taken.",
    "Not a claim that bulkheads are free. Idle capacity is the price, and the "
    "demo prints idle threads next to queued jobs.",
],
problem="""
The shop imports a supplier feed and takes payments, and both use the same
executor. The partner's API goes slow, four import batches take every thread,
and checkout -- which needs a thread for a few milliseconds -- cannot get one.
Nothing about checkout is broken. It simply never starts, and by then the
shopper has gone.

**What the pattern must deliver:** two named pools with bounded queues, so that
checkout runs on threads the import could never have taken; a full pool must
refuse immediately rather than queueing for ever; and the throughput lost by
not sharing must be shown rather than glossed over.
""",
roles=[
    ("Bulkhead", "`Bulkhead`"),
    ("Test device for a slow dependency", "`Gate`"),
    ("Timeline", "`JobLog`"),
    ("Important work", "`Checkout`"),
    ("Greedy work", "`SupplierFeed`"),
    ("Rejection", "`BulkheadFullException`"),
    ("Entry point", "`BulkheadDemo`"),
],
requirements=[
    "**The shared pool starves checkout**, proven by a bounded "
    "`Future.get` timing out after 250ms -- the shopper's patience -- while a "
    "second test shows the same checkout succeeding the instant a thread "
    "frees.",
    "**The partition holds with the feed just as stuck.** A test asserts the "
    "feed's threads are all busy, so isolation is demonstrably the reason "
    "checkout completed and not luck; another puts twenty sales through "
    "during the jam.",
    "**The queue is bounded and a full bulkhead refuses at once**, in "
    "single-digit milliseconds, so the caller can shed or degrade.",
    "**The cost is asserted, not admitted.** A test shows the shared pool "
    "running all four batches at once where the partitioned pools leave two "
    "threads idle beside two queued jobs.",
    "**No test sleeps.** This is the category's only real-threads project, "
    "and it uses a closed `Gate` and bounded waits rather than "
    "`Thread.sleep`, with `JobLog` on a `CopyOnWriteArrayList` because worker "
    "threads write to it concurrently.",
],
),

"database-per-service": dict(
purpose="""
Teach what is actually gained and actually lost when two services stop sharing
a database -- and to be honest that the gain is organisational, not technical.
""",
nongoals=[
    "Not a claim that splitting is faster. The split page in this project is "
    "measurably slower than the join it replaces.",
    "Not a recommendation to split. If the two teams are the same three "
    "people, the shared schema wins, and the notes say so.",
    "Not an ORM, a migration tool or a real permissions system. "
    "`NotYourDataException` stands in for a database refusing credentials it "
    "was never given.",
],
problem="""
The order history page needs order rows from Orders and product names from
Catalog. With one schema it is a single query with a join, every row has a name
because a join cannot forget one, and a foreign key guarantees the product row
is there.

Then the catalog team renames a column in a table they own. Their migration is
correct and their tests pass, and the order history page breaks -- because the
query that named that column lives in somebody else's repository, absent from
their code, their tests and their build.

**What the pattern must deliver:** each service owns its tables and refuses
everybody else; the same page is rebuilt from two service calls and an assembly
step; the rename becomes a non-event; and the two things the split takes away --
the join and the foreign key -- are shown costing something real.
""",
roles=[
    ("Owned databases", "`OrderDatabase`, `CatalogDatabase`"),
    ("The shared schema being replaced", "`SharedSchema`"),
    ("Services", "`OrderService`, `CatalogService`"),
    ("Assembly", "`OrderHistoryPage`, `OrderHistoryRow`"),
    ("Refusals", "`NotYourDataException`, `ColumnNotFoundException`"),
    ("Entry point", "`DatabasePerServiceDemo`"),
],
requirements=[
    "**The shared schema is shown working first**, in one round trip, "
    "because the rest of the category is the story of giving that up.",
    "**The cross-team break is a passing test.** Every test in "
    "`SharedSchemaTest` passes, including the one where a correct migration "
    "breaks another team's page.",
    "**Ownership is enforced.** Reading Catalog's data through Orders throws "
    "`NotYourDataException`, and the notes explain that in production the "
    "refusal comes from credentials rather than from Java.",
    "**The rename is a non-event after the split**, asserted against an "
    "unchanged page.",
    "**The batch call is deliberate.** `CatalogService.namesFor` takes a "
    "list, and the notes state that one call per sku turns a fifty-row page "
    "into fifty calls.",
    "**The lost foreign key is demonstrated.** Catalog deletes a product an "
    "order refers to, nothing prevents it, and the page renders "
    "`(no longer in the catalogue)` rather than crashing -- with the notes "
    "saying that a rule which was impossible to break is now merely impolite "
    "to break.",
],
),

"api-composition": dict(
purpose="""
Teach how to build one page from several services: send the independent calls
together, and decide *before* the outage which of them the page cannot do
without.
""",
nongoals=[
    "Not a threading exercise. `Fanout` is a loop over a simulated clock, "
    "because the pattern's lesson is the dependency shape and the "
    "classification, not `CompletableFuture` syntax.",
    "Not a claim that parallelism fixes latency. It removes the addition and "
    "leaves the maximum.",
    "Not CQRS. Composition on demand is what CQRS replaces when these two "
    "costs can no longer be lived with.",
],
problem="""
The order details page needs the order from Orders, product names from Catalog,
and the delivery status from Shipping. Written in the obvious way it is three
lines of ordinary Java, every test passes, and a code review waves it through --
while Shipping waits sixty milliseconds for Catalog's answer and then does not
use it. The shopper pays 30 + 60 + 120 = 210ms for that.

The second problem is worse than the latency. When Shipping is down, the
sequential page throws away an order and a set of product names that had
already arrived, and the shopper gets nothing.

**What the pattern must deliver:** the calls that do not depend on each other
leave together, so the page costs the slowest rather than the sum; every
dependency is classified required or optional in advance; and a page missing an
optional section says what it does not know instead of guessing.
""",
roles=[
    ("Composer", "`OrderDetailsComposer`"),
    ("Naive composer", "`SequentialOrderDetailsComposer`"),
    ("Parallel calls", "`Fanout`, `Fanout.Branch`"),
    ("Availability arithmetic", "`Availability`"),
    ("Response", "`OrderDetailsPage`, `DeliveryStatus`"),
    ("Services", "`OrderService`, `CatalogService`, `ShippingService`"),
    ("Entry point", "`OrderDetailsDemo`"),
],
requirements=[
    "**The sequential version works and is kept.** Its test class passes, "
    "including `itBuildsTheRightPage`, so the comparison is about time and "
    "availability rather than correctness.",
    "**Parallel calls cost the maximum.** 210ms sequential against 150ms "
    "composed, asserted on the simulated clock, with a test checking that "
    "both parallel branches share a start time.",
    "**The dependency shape is honest.** Catalog cannot start until Orders "
    "has named the skus, so the fan-out is one call and then two together, "
    "not a flat three.",
    "**Required and optional are explicit.** Orders required, Catalog and "
    "Shipping optional: `Branch.value()` rethrows and "
    "`Branch.valueOr(fallback)` substitutes, and a required failure refuses "
    "to build a page at all.",
    "**The page names its gaps.** `DeliveryStatus.unknown()` says it cannot "
    "check rather than guessing \"in transit\", and "
    "`OrderDetailsPage.missingSections()` lists what is absent, because a "
    "quietly dropped section is indistinguishable from an order that has not "
    "shipped.",
    "**Availability multiplies, in code.** Three 99.9% services give a "
    "99.7% page -- 129.5 minutes a month against 43.2 -- computed by "
    "`Availability` and pinned by `AvailabilityTest` so the prose cannot "
    "drift from the arithmetic.",
    "**The slowest dependency sets the pace.** With Shipping at 400ms the "
    "page is 430ms, asserted, so the limit of the pattern is a test rather "
    "than a caveat.",
],
),

"cqrs": dict(
purpose="""
Teach keeping two shapes of the same data -- one for changing it safely, one
already in the shape the page needs -- and the three things that costs:
staleness, a second store, and one number you must never sell against.
""",
nongoals=[
    "Not event sourcing. Events update a projection here; the write side is "
    "still the system of record.",
    "Not caching. A cache is implemented alongside so the difference can be "
    "shown rather than asserted.",
    "Not a recommendation. For a page nobody looks at, composing on demand is "
    "the right answer and is always up to the second.",
],
problem="""
The order history page is composed from Orders and Catalog on every view: three
refreshes cost six service calls and produce three identical pages. Reads
outnumber writes by orders of magnitude, and the shop pays the composition every
single time.

**What the pattern must deliver:** a read model updated when events arrive and
read with one lookup; an honest account of the window in which it is wrong; a
demonstration of why a cache with an expiry is not the same thing; and the rule
that a decision about money or stock is made on the write side, never on the
projection.
""",
roles=[
    ("Write side", "`OrderWriteService`, `StockLedger`"),
    ("Read side", "`OrderHistoryReadModel`, `OrderHistoryRow`, `OrdersQueryApi`"),
    ("The version being replaced", "`ComposingOrderHistory`"),
    ("The thing it is confused with", "`CachedOrderHistory`"),
    ("Events", "`EventBus`, `ShopEvent`"),
    ("Entry point", "`CqrsDemo`"),
],
requirements=[
    "**The read is one lookup.** Three views cost 15ms and zero calls to "
    "other services, against 270ms and six calls for composition.",
    "**The work moved rather than vanished**, and the demo says so: Catalog "
    "is called once, when the order is placed.",
    "**The stale window is shown and it closes by itself.** "
    "`EventBus.holdEvents()` lets a test assert a paid, final order that the "
    "customer's own history page does not yet show -- with no polling, "
    "retrying or timer involved in fixing it.",
    "**The cache comparison is code.** `CachedOrderHistory` passes all its "
    "tests, and `itServesAPageItKnowsNothingAbout` plus `thereIsNoFreeSetting` "
    "pin the difference: a read model is corrected by the event that made it "
    "wrong, a cache is wrong for however long its timer says.",
    "**The write side decides the sale.** `StockLedger` checks and decrements "
    "in one step, so two shoppers cannot both take the last kettle; a test "
    "shows the read model still offering it and the ledger refusing.",
    "**The projection can be rebuilt.** `rebuildFrom` discards and replays, "
    "because a read model that cannot be rebuilt is a second copy of the "
    "truth rather than a projection.",
    "**Reads survive an outage.** `readsSurviveAnOutage` answers while "
    "Catalog is down, since nobody is called at read time.",
],
),

"saga": dict(
purpose="""
Teach how a job spanning five services is completed without a transaction: a
sequence of small committed steps, each with an action that undoes it, walked
backwards when one of them refuses.
""",
nongoals=[
    "Not distributed two-phase commit. There is no point in the run where the "
    "five services hold their breath, and the project says so rather than "
    "pretending otherwise.",
    "Not rollback. Compensation adds a new fact -- a refund, a cancellation -- "
    "and never erases the old one.",
    "Not choreography. This is an orchestrated saga; the alternative is "
    "described, with the reason for the choice.",
    "Not a message broker. The steps are method calls over a simulated "
    "network so the ordering is exact.",
],
problem="""
Placing an order reserves stock, takes payment, creates the order, schedules a
shipment and emails the customer -- five services, five databases. There is no
transaction that covers them, so by the time payment is taken the stock
reservation is already committed and visible to everybody.

The code everybody writes instead is four calls in a row inside a `try`, and its
failure mode is the point: the card is charged, the kettle is off the shelf, the
order says CONFIRMED, nothing will ever ship, and nothing threw.

**What the pattern must deliver:** each step's undo is written down beside it;
a failure unwinds the completed steps in reverse; the unwinding carries on when
one undo itself fails and the outcome names the step it could not undo; and the
step that cannot be compensated at all goes last.
""",
roles=[
    ("Orchestrator", "`SagaOrchestrator`"),
    ("Step", "`SagaStep`, `SagaContext`, `PlaceOrderSteps`"),
    ("Outcome", "`SagaOutcome`"),
    ("Naive alternative", "`NaiveCheckoutService`"),
    ("Services", "`StockService`, `PaymentService`, `OrderService`, `ShippingService`, `EmailService`"),
    ("Failures", "`OutOfStockException`, `CardDeclinedException`, `CannotDeliverException`, `ServiceUnavailableException`"),
    ("Entry point", "`PlaceOrderSagaDemo`"),
],
requirements=[
    "**Compensation runs in reverse**, asserted as an exact list -- create "
    "order, take payment, reserve stock -- because later steps depend on "
    "earlier ones and must come apart in the opposite order.",
    "**A refund is a new fact.** The payment ledger holds two entries, "
    "`CHARGE £70.95` and `REFUND -£70.95`, and nets to zero; the test asserts "
    "two entries rather than an empty ledger.",
    "**An early failure is cheap.** A declined card costs one released "
    "reservation, which is why the steps most likely to fail go first.",
    "**A failed compensation is a third outcome.** `SagaOutcome` has "
    "`NEEDS_HUMAN_HELP`, the unwinding continues past the failure, and the "
    "outcome names the step that could not be undone.",
    "**The non-compensatable step is shown both ways.** The confirmation "
    "email declares `canBeCompensated() == false` and goes last, and "
    "`PlaceOrderSteps.withTheEmailInTheWrongPlace` exists so that a test can "
    "show the promise the shop then has to take back.",
    "**The naive version passes every test.** `NaiveCheckoutServiceTest` is "
    "green while the money stays taken, the stock stays reserved and no "
    "shipment exists -- and the notes state why `@Transactional` on that "
    "method protects nothing outside its own database.",
],
),

"transactional-outbox": dict(
purpose="""
Teach why "save it and tell somebody" cannot be two separate operations, and how
one commit over two tables plus a background relay turns an impossible guarantee
into an achievable one.
""",
nongoals=[
    "Not Kafka or Debezium. `MessageBroker` is a map with subscribers, and the "
    "relay is a method somebody calls.",
    "Not exactly-once delivery. The relay can publish and die before marking "
    "the message sent, so delivery is at-least-once -- which is why the next "
    "project exists.",
    "Not change-data-capture. The relay polls the outbox table, which is the "
    "simpler of the two implementations and the one worth understanding "
    "first.",
],
problem="""
Placing an order writes a row and publishes an `OrderPlaced` event. Written the
obvious way that is two lines: save, then publish. On a good day both happen.

On a bad day the save commits and the process dies before the publish, and the
order exists with nobody told: no confirmation email, no warehouse pick, no
analytics. The failure is rare, silent, and invisible from the order itself --
and swapping the two lines only trades a lost event for an event about an order
that does not exist.

**What the pattern must deliver:** the row and the message are written in one
transaction, so both land or neither does; the broker is never called inside
that transaction; a separate relay sends what the outbox holds and can be run
again safely; and the one remaining gap -- a duplicate delivery -- is stated
plainly rather than hidden.
""",
roles=[
    ("The atomicity being borrowed", "`OrderDatabase`, `OrderDatabase.Transaction`"),
    ("Writer", "`OrderService`"),
    ("Naive writer", "`NaiveOrderService`"),
    ("Relay", "`OutboxRelay`"),
    ("Message", "`OutboxMessage`, `Order`"),
    ("Broker and subscriber", "`MessageBroker`, `NotificationService`"),
    ("The JVM disappearing", "`ProcessDiedException`"),
    ("Entry point", "`OrderPlacedDemo`"),
],
requirements=[
    "**Both or neither.** A crash before the commit leaves no order and no "
    "message; the commit writes one order and one outbox message together, and "
    "the log line says so.",
    "**No broker call inside the transaction.** `OrderService.placeOrder` "
    "touches the database only, so a slow or dead broker cannot lengthen or "
    "fail the write.",
    "**The message outlives the process.** With the broker down the relay "
    "logs `LEFT-IN-TRAY` twice and delivers both messages when it returns; "
    "nothing is lost and nobody minds.",
    "**Delivery is at-least-once, demonstrated.** "
    "`OutboxRelay.dieAfterPublishing()` opens the one gap the pattern cannot "
    "close, and a test asserts the same message delivered twice and two "
    "identical emails.",
    "**The duplicate is recognisable.** The redelivered message carries the "
    "same id, which is exactly what the next pattern needs.",
    "**The naive version passes every test**, including the one where the "
    "order exists and zero events and zero emails went out.",
    "**The family resemblance is named.** The notes connect this to "
    "double-checked locking's bug in a bigger coat: two operations that must "
    "both happen, with no single mechanism covering them.",
],
),

"idempotent-consumer": dict(
purpose="""
Teach how a consumer turns at-least-once delivery into exactly-once effect by
recording the ids it has handled in the same transaction as the effect -- and
teach the question to ask before building any of that.
""",
nongoals=[
    "Not a claim that the duplicate is somebody's fault. A sender whose "
    "acknowledgement is lost must choose between a duplicate and a lost "
    "message, and every production system chooses the duplicate.",
    "Not exactly-once delivery. The delivery is still at-least-once; only the "
    "*effect* happens once.",
    "Not a dedupe library. The pattern is a transaction, and the project's "
    "point is that a `HashSet` is not one.",
],
problem="""
Notifications receives `OrderPlaced` twice, because the previous project's relay
guarantees at-least-once delivery. Two emails is embarrassing; had the consumer
been Payments it would have been two charges.

The obvious answer is a `HashSet` of ids seen, and it catches the duplicate in
the happy case. It has two failures that only appear in production: the set
lives in the heap, so a deploy empties it -- and a restart is often *why* the
acknowledgement was lost -- and the id is written after the work, so a crash in
between keeps the effect and loses the id. Both have one root: the id and the
effect are stored in two different places, so nothing can make them land
together.

**What the pattern must deliver:** the id and the effect committed together; an
honest account of what the store costs, including an expiry window that is
chosen rather than derived; and the prior question -- can the handler be
rewritten so that running it twice simply does not matter?
""",
roles=[
    ("Idempotent consumer", "`IdempotentNotificationConsumer`"),
    ("Naive consumer", "`NaiveNotificationConsumer`"),
    ("The store and its transaction", "`NotificationsDatabase`, `NotificationsDatabase.Transaction`"),
    ("Naturally idempotent consumer", "`ShipmentStatusConsumer`"),
    ("The handler worth rewriting", "`LoyaltyPointsConsumer`"),
    ("At-least-once delivery", "`MessageBroker`, `Message`, `MessageConsumer`"),
    ("The JVM disappearing", "`ProcessDiedException`"),
    ("Entry point", "`OrderPlacedTwiceDemo`"),
],
requirements=[
    "**Exactly once out of at-least-once.** Two deliveries of the same "
    "message produce one confirmation and one stored id.",
    "**The id and the effect share one commit**, logged as one confirmation "
    "and one handled id together, so a crash before the commit writes "
    "neither and the redelivery handles the message properly.",
    "**Both naive failures are shown, and both tests pass.** A restart empties "
    "the in-memory set and produces two confirmations; a crash after the work "
    "and before recording the id does the same.",
    "**The constraint is stated out loud.** The effect is a database row, "
    "which is the only reason it can share the transaction; an external "
    "effect sends you back to the outbox, which is why these two patterns are "
    "taught together.",
    "**Natural idempotence comes first.** `ShipmentStatusConsumer` has no "
    "store, no transaction and no expiry, because setting a status twice sets "
    "the same status.",
    "**Rewriting beats storing.** `LoyaltyPointsConsumer.handle` doubles a "
    "running total to 140 points, and `awardForOrder` sets 70 per order and "
    "stays at 70 when handled twice.",
    "**The expiry window is a guess, and it costs.** With a thirty-second "
    "memory, a duplicate a minute later is handled as new -- a passing test "
    "and a demo line, not a caveat -- and the notes add that the message must "
    "carry a stable id at all.",
],
),

"externalised-configuration": dict(
purpose="""
Teach the decision to move a value out of the compiled program and read it while
the program runs -- and to teach the half of that decision most write-ups leave
out, which is that four guards stayed behind in the source file and have to be
rebuilt deliberately on the outside.
""",
nongoals=[
    "Not a configuration server. `ConfigServer` is a `HashMap` in the same "
    "JVM with a clock bolted on so a write can take four seconds; the "
    "optional `real/` directory is where a live Spring Cloud Config Server "
    "appears.",
    "Not a network lesson. There is no HTTP, no YAML and no JSON. The file "
    "format a source happens to use teaches nothing about the pattern.",
    "Not caching or refresh. Every read reaches the source, because the "
    "point being made is about *where* the read happens, not about how often "
    "it is allowed to be slow.",
    "Not layered sources or secrets. One source, one key. Environment "
    "variables over a file over a server, and how a password differs from a "
    "threshold, are named as omissions in the notes and left as an exercise.",
    "Not a timing measurement. The four seconds a write takes is a modelled "
    "constant, as are the pipeline's 135 minutes -- numbers a test can "
    "assert exactly, where a measurement could not.",
],
problem="""
The shop gives free delivery on baskets over £50, and the threshold is a
`private static final` constant in the checkout class. That constant is not
wrong. It is named, typed as money, in exactly one place, and a reviewer would
approve it without a comment.

Then marketing ask, at 16:30 on a Friday, for £35 from Saturday morning.
`ReleasePipeline` prices that: a fifteen-minute edit, a code review, a build, an
approval and a watched deploy -- 135 minutes of work, inside a weekday 09:00 to
17:00 window, live on Monday at 10:45. The promotion was for the weekend and is
late by two days and one hour forty-five.

No step in that list is unreasonable. Review is how a typo does not reach a
million customers; the window exists because the people who would notice a bad
release are at their desks on weekdays. The problem is not code quality. It is
that a business-policy value is sitting in a place with an engineering change
speed.

**What the pattern must deliver:** the same number, read from outside on every
quote, live in four seconds -- and every guard that number lost on the way out,
put back on purpose.
""",
roles=[
    ("The caller", "`ConfiguredCheckout`"),
    ("The rejected design", "`HardCodedCheckout`"),
    ("The boundary", "`SettingsReader`, `TrustingSettings`, `GuardedSettings`"),
    ("The schema", "`MoneySetting`, `InvalidSettingException`"),
    ("The source", "`ConfigSource`, `ConfigServer`, `ConfigSourceUnavailableException`"),
    ("The audit trail", "`ChangeLog`, `ConfigChange`"),
    ("Provenance", "`SettingValue`, `DeliveryQuote`"),
    ("The price of the alternative", "`ReleasePipeline`"),
    ("Entry point", "`FreeDeliveryDemo`"),
],
requirements=[
    "**The read is inside the method.** `ConfiguredCheckout.quote` fetches "
    "the threshold on every call, and `theThresholdIsReadEveryTime` fails "
    "the moment it is tidied into the constructor -- the difference between "
    "a change landing on the next order and on the next restart.",
    "**Adopting the pattern changes no behaviour.** With nothing configured, "
    "the configured checkout and the hard-coded one quote all three baskets "
    "identically; a test asserts it, so the comparison is fair rather than "
    "rhetorical.",
    "**The cost of the alternative is a number.** `ReleasePipelineTest` pins "
    "135 minutes of work, live Monday 10:45, and late by two days one hour "
    "forty-five -- the figures the README and the narration speak aloud.",
    "**An unreachable source is not a missing key.** `ConfigSource.lookup` "
    "returns `Optional.empty()` for the one and throws "
    "`ConfigSourceUnavailableException` for the other, so an outage cannot "
    "be mistaken for an ordinary default.",
    "**The outage is survivable and silent, and both are shown.** The shop "
    "keeps selling on the compiled-in default, and the demo states plainly "
    "that the promotion is off with no error and no alarm.",
    "**A well-formed wrong value is demonstrated, not warned about.** "
    "`TheBillTest.minusOneGivesEverythingAway` **passes**: `-1` parses, "
    "every basket ships free, and nothing throws or logs.",
    "**A malformed value takes the shop down.** With a trusting reader the "
    "word `fifty` escapes as an `InvalidSettingException` through checkout "
    "and not one basket can be quoted.",
    "**The guard is a declared range, not a type.** `MoneySetting` carries "
    "key, default, lowest and highest; widening the range makes `-1` "
    "acceptable again, which is the exercise the video closes on.",
    "**A rejected value falls back to the last good one.** "
    "`GuardedSettings` prefers the last value that passed validation over "
    "the compiled default, so an unrelated typo cannot silently cancel a "
    "promotion somebody set an hour earlier -- and every rejection is "
    "recorded rather than swallowed.",
    "**The trail is append-only and carries the displaced value.** "
    "`ChangeLog` has no edit or delete, and `ConfigChange.was` is what makes "
    "`ConfigServer.rollback` a lookup rather than an act of memory.",
    "**Rollback is as fast as the change.** The demo rolls back four seconds "
    "after the decision and prints what the same correction would have cost "
    "through the release pipeline: live Monday at 11:15.",
    "**Every quoted number is the program's.** `DemoRunsTest` captures the "
    "demo's output, asserts the figures the README, the notes and the video "
    "narration quote, and asserts that two runs are byte-identical.",
],
),

"distributed-tracing": dict(
purpose="""
Teach the decision to give one customer request one identifier and to have every
unit of work record how long it took *and what asked for it* -- and to teach the
half most write-ups leave out, which is that the resulting picture can be
confidently wrong in three ways, none of which raises an error.
""",
nongoals=[
    "Not a tracing SDK. `Tracer`, `Span` and `Trace` are six small classes in "
    "one JVM; OpenTelemetry, `traceparent` headers, a collector and a "
    "backend belong to the optional `real/` directory.",
    "Not a network lesson. There is no HTTP and no serialisation. A trace "
    "context crossing a process boundary is the same string being passed "
    "along, and the string is what is being taught.",
    "Not a measurement. Every duration is a scripted constant from "
    "`Clock.Scripted`, so the 900ms page and the 340ms model are figures a "
    "test can assert exactly, where a real measurement could not.",
    "Not storage, batching or back-pressure. The spans go into a list. What "
    "the volume costs is made concrete in Act 7 as a count, not as an "
    "architecture.",
    "Not metrics or logs. Both appear, but only to be distinguished from a "
    "trace: Act 2 exists to show what four correct logs cannot say.",
],
problem="""
The shop's product page takes nine hundred milliseconds. Four services
contributed to it -- catalog, pricing, inventory and recommendations -- and all
four are healthy, all four are responding, and all four are writing correct
logs. Nobody in the building can say which of them spent the time. There is
exactly one measurement in the whole situation, and it is the complaint.

Act 2 shows why more logging does not rescue this. Two customers are on the site
at once, and the interleaved log gives `quote started` at 07.120, `quote
started` at 07.160, `quote complete` at 07.300 and `quote complete` at 07.340.
Subtract one way and pricing took 180ms; subtract the other and it took 220ms.
Both look reasonable and one of them pairs one customer's start with another
customer's finish.

Then try to fix it by adding fields. The thread name works until the work
crosses a thread, which it does in Act 6. The pod name is the same for both
customers, and so is the product id. Every candidate fails the same test: **the
same across one request, and different across the next.** What is missing is not
detail. It is an identifier -- and, one level less obviously, a parent.

**What the pattern must deliver:** the 900ms attributed to the service that
actually spent it, drawn from the data rather than from a tool's cleverness --
and each of the three ways that attribution can be wrong while looking right.
""",
roles=[
    ("The caller", "`ProductPage`"),
    ("The rejected design", "`InterleavedLog`"),
    ("The identifier", "`TraceContext`"),
    ("The unit of work", "`Span`, with its `parentSpanId`"),
    ("The boundary", "`Tracer`, `Tracer.Scope`"),
    ("The assembled request", "`Trace`"),
    ("The drawing", "`Waterfall`"),
    ("The price of volume", "`Sampler`"),
    ("The thread failure", "`AsyncHandoff`"),
    ("Determinism", "`Clock`, `Clock.Scripted`"),
    ("Entry point", "`ProductPageDemo`"),
],
requirements=[
    "**The pattern is one field.** `Span.parentSpanId` is a single string, "
    "and `start(context, name)` is the one argument that makes a pile of "
    "timings into a tree; the class diagram's arrow from `Span` to itself is "
    "the whole structure.",
    "**The drawing is derived, not invented.** `Waterfall` computes "
    "indentation from the parent field and horizontal position from the "
    "start time, and nothing else -- so the picture a hosted tool shows is "
    "demonstrably a property of the data.",
    "**Self time, not total time.** The page span lasts the full 900ms and "
    "is charged 0ms of its own, recommendations lasts 400ms and is charged "
    "60, and the six self times sum to exactly 900. The ranking model's "
    "340ms is 37% of the page, and that is the finding.",
    "**A span that is never closed is invisible.** "
    "`TracerTest.anUnclosedSpanIsInvisible` passes, which is why real "
    "instrumentation uses try-with-resources: an exception thrown past an "
    "open span deletes the record of the call that failed.",
    "**An uninstrumented service produces a consistent lie.** In Act 5 "
    "recommendations forwards the context faithfully and opens no span. "
    "`ProductPageTest` asserts the resulting trace has one root, no orphans "
    "and 900ms fully accounted for *and* charges the page 60ms it never "
    "spent -- that pair is the argument, not an oversight.",
    "**The thread failure is one line in the wrong place.** `AsyncHandoff` "
    "reads the context from a `ThreadLocal` on the worker and is handed "
    "`null`, giving `2 separate roots -- this trace is broken`; reading it "
    "on the thread that has it and passing it as a value gives the same two "
    "spans, the same 400ms and one root.",
    "**Sampling is a decision made too early, priced in units.** `Sampler` "
    "keeps 10,000 of a million and discards 990,000, and the demo asks "
    "whether request 862,144 was kept: `no -- it is gone, and it is not "
    "recoverable`. Tail sampling is named as the way out and not "
    "implemented.",
    "**Nothing in the bill throws.** All three failures are the price of the "
    "pattern rather than mistakes made while applying it, and each one is "
    "asserted to produce output rather than an exception.",
    "**The demo is deterministic.** The clock is scripted, span ids are "
    "sequential and the sampler counts rather than randomises, so two runs "
    "are byte-identical -- there is one background thread in the project, in "
    "Act 6, and the demo waits for it.",
    "**Every quoted number is the program's.** `DemoRunsTest` captures the "
    "demo's output and asserts the figures the README, the notes and the "
    "video narration speak aloud.",
],
),

"backends-for-frontends": dict(
purpose="""
Teach the decision to give each kind of client its own small backend, owned by
the team that owns the screen, holding the shape of one screen and nothing else
-- and to teach it against the fix that looks like it makes the pattern
unnecessary, because a `?fields=` query parameter reaches the same byte count
with no new process to run, and a reader who is not shown that working will
file this pattern under payload size and be wrong about it for years.
""",
nongoals=[
    "Not a network lesson. There is no HTTP, no JSON library and no "
    "serialisation. `Doc` is an ordered map that prints and measures itself, "
    "and every claim about round trips is made by *counting* them in "
    "`CallLog`, not by timing them.",
    "Not a performance measurement. `Shop` returns fixed data in "
    "microseconds, so the byte counts are identical on every machine and a "
    "test can assert them exactly, where a measurement could not.",
    "Not concurrency. The four internal calls are sequential where a real "
    "backend would fan them out and wait once, which means the project "
    "**understates** the pattern's benefit rather than overstating it.",
    "Not an API gateway. The two are neighbouring patterns and are commonly "
    "deployed together; Act 6 exists to separate them with a single "
    "question, not to implement either as infrastructure.",
    "Not deployment. Two independently deployable Spring Boot backends "
    "serving the same product over the wire, in front of a third service "
    "holding the shop, belong to the optional `real/` directory, which is a "
    "separate Gradle build.",
],
problem="""
The shop sells one copper coffee maker. On a phone the product screen draws six
things -- title, price, one image, a rating, a rating count, and one line saying
when the parcel arrives. On a desktop the same product fills a page with fifteen,
including the description, a specification table, five images and three written
reviews. Five services hold all of it: catalog, pricing, inventory, reviews and
recommendations. Neither screen is wrong. Both teams are being reasonable. They
disagree about what a product *is*, and everything here comes out of that.

The first design is the one shops arrive at by accident, because it is nobody's
decision: the phone calls all five services itself. Five sequential round trips
before a pixel is drawn -- sequential because pricing cannot be asked about a
product until the catalog has named it -- carrying 1767 bytes and 29 fields, of
which 6 reach the screen.

The second design is one shared endpoint in front of the five, and it genuinely
helps: one round trip instead of five. But one endpoint publishes one document,
and that document must satisfy every client, so it grows into the union of all
of them. 1755 bytes arrive, 212 are drawn, 1543 -- 87% -- are thrown away on
arrival.

And then the obvious fix works. `GET /api/products/4417?fields=...` returns 212
bytes, which is the same saving the finished pattern gets, from a query
parameter, with nothing to deploy. **If this pattern were about payload size,
the story would end there.** It ends instead at the next request: the phone team
wants one line of text -- "Free delivery, arrives Friday" -- joined from stock,
the delivery rules and the clock. Half an hour of work. But it is a new field on
a document five other clients also receive, so it becomes a contract change in a
queue behind work that has nothing to do with the phone. The phone team could
have written it in an afternoon and waits five weeks.

**What the pattern must deliver:** that five-week queue removed, the byte saving
kept, the boundary against a gateway made decidable in one question -- and the
three ways the pattern costs more than it saves, none of which throws.
""",
roles=[
    ("The contract", "`ClientBackend`"),
    ("The two live implementations", "`MobileBff`, `WebBff`"),
    ("The services behind them", "`Shop`"),
    ("The document", "`Doc`"),
    ("The ruler", "`Screens`"),
    ("The first rejected design", "`ChattyPhone`"),
    ("The second rejected design", "`SharedApi`"),
    ("The count that is the evidence", "`CallLog`, `CallLog.Origin`"),
    ("The duplicated belief", "`SavingRules`"),
    ("The gateway's question", "`CrossCutting`"),
    ("How many is too many", "`ClientEstate`"),
    ("Presentation, not policy", "`Money`"),
    ("Entry point", "`ProductScreenDemo`"),
],
requirements=[
    "**Two implementations, both live, on purpose.** `ClientBackend` has two "
    "implementing classes and neither is a fallback: the phone always talks "
    "to `MobileBff` and the desktop always to `WebBff`, at the same time, in "
    "production. Two arrowheads into one interface is the pattern rather "
    "than a detail of it.",
    "**A backend is the size of its screen, and stays that size.** "
    "`MobileBffTest.sendsOnlyWhatIsDrawn` asserts "
    "`assertEquals(Screens.PHONE, screen.paths())` -- equality, not "
    "containment -- so a seventh field fails the build. That assertion is "
    "the only reason a backend does not drift back into a shared endpoint "
    "over a year.",
    "**The two backends must disagree.** "
    "`WebBffTest.disagreesWithThePhonesBackend` asserts the two return "
    "*different* field lists. If they ever converged the shop would be "
    "paying twice for one job and the pattern should be withdrawn rather "
    "than admired.",
    "**The obvious fix is shown succeeding.** Act 2 runs the `?fields=` "
    "query and prints 212 bytes before the pattern is introduced, so the "
    "reader sees the payload argument settled and knows the pattern is not "
    "resting on it.",
    "**The saving that is not bytes.** Act 2 also prints the delivery "
    "sentence as `not available -- a field like this belongs to one client, "
    "and this endpoint belongs to all of them`. The five-week queue is the "
    "problem the pattern removes, and it is organisational with a technical "
    "cause.",
    "**A backend omits calls, not just fields.** `MobileBff` never calls "
    "recommendations, because the phone screen has no related-products "
    "strip; internal calls go 5, 5, 4 across the three designs while device "
    "calls go 5, 1, 1. **The work relocated onto a network that costs "
    "nothing; it was not deleted.**",
    "**Presentation belongs in the backend.** Pricing returns `4799`; the "
    "phone is sent the string `\"£47.99\"`. The conversion happens in a "
    "process that can be corrected this afternoon rather than in an app "
    "customers will still be running in two years.",
    "**Shape inside, belief behind.** Act 5 copies one discount rule into "
    "`MobileBff`, and after the pricing team adds a minimum-duration "
    "condition the desktop claims nothing while the phone advertises `Save "
    "£12.00` for a price that rose 11 days ago. Nothing throws, nothing is "
    "logged, both backends' tests pass, and no test writable inside either "
    "one can notice -- the rule is that anything the shop would still "
    "believe with every client switched off belongs behind the backend.",
    "**The gateway boundary is one question, and the code answers it.** "
    "`CrossCutting.copiesBehindAGateway()` takes no argument, and that "
    "absence is the answer: 8 copies across 2 backends against 4 whatever "
    "the number of backends. *What does this screen need?* is a backend for "
    "a frontend; *is this request allowed in at all?* is a gateway.",
    "**One per disagreement, not per device and not per team.** "
    "`ClientEstate` scores six clients as three genuine disagreements -- the "
    "tablet is the phone's fields in a wider column, the kiosk is the "
    "desktop page with the basket hidden, the partner feed is not a screen. "
    "**Two backends is a pattern. Nine is a department.**",
    "**Every quoted number is the program's.** `DemoRunsTest` captures the "
    "demo's output and asserts the figures the README, the notes and the "
    "video narration speak aloud.",
],
),

"sidecar": dict(
purpose="""
Teach the decision to take a concern that is not about the business out of the
service and run it in a separate process beside it -- and to teach it with the
bill attached, because in a single program a proxy in front of a service is
just Decorator, and a reader who is not shown what the process boundary costs
will either never reach for the pattern or reach for it everywhere.
""",
nongoals=[
    "Not a network lesson. There is no HTTP, no socket and no serialisation. "
    "The sidecar is an object the service calls, and the phrase *separate "
    "process* is carried by the narration and by the optional `real/` "
    "directory rather than by the Java.",
    "Not a performance measurement. `Clock` counts milliseconds and never "
    "sleeps, so the demo finishes instantly and every timing it prints is "
    "identical on every machine and assertable by a test.",
    "Not concurrency. The four services take payments one after another, "
    "which is what makes the shared attempt allowance legible -- in "
    "production they would contend for it, which only sharpens the point.",
    "Not a service mesh. A mesh is this pattern applied to every service at "
    "once with a control plane on top; Act 7 gives the arithmetic that "
    "decides whether you want one, and stops there.",
    "Not Decorator dressed up. Scene 14 of the video and the README both say "
    "plainly that in one JVM this *is* Decorator, and name the two questions "
    "-- redeploy independently, and cross-language -- that are the only "
    "reasons to pay for a process.",
],
problem="""
The shop takes money in four places. Checkout charges a card while a customer
watches a spinner. Refunds gives money back when the coffee maker comes back in
the post. Subscription billing runs at two in the morning against thousands of
saved cards. Marketplace payouts pays the independent sellers on a Friday. Four
teams, four repositories, four release days -- and one payment provider behind
all four.

None of those teams wanted to become an expert on that provider's network
behaviour, and every one of them had to be. How many times to retry. When to
give up. Which transport security profile to present. What to count and what to
call the counters. Four questions, four services, **sixteen answers in four
places** -- and not one of the sixteen is about checkout, or refunds, or
subscriptions, or payouts. They would be identical if the shop sold bicycles.

In March the provider changes the rule: at most three attempts, and wait
properly between them. Three pull requests land in one afternoon. The fourth
does not. Subscription billing runs overnight, its team was not in the meeting,
and it had no open work that sprint; there was no fourth place to look unless
you already knew there was one. **Nothing throws, nothing is logged, and every
test in all four services still passes**, because each tests its own copy and
each copy is internally consistent.

Three weeks later the gateway wobbles for 300ms at two in the morning. The
merchant account allows twelve attempts. Subscription billing is already
running, reaches the wobble first on the old policy, and spends six. Marketplace
payouts arrives fourth, makes one attempt, and is refused -- the sellers are not
paid. Marketplace payouts was updated in March and did exactly what was asked.
It arrived fourth. On Monday somebody opens an incident against the service
whose every line is correct.

**What the pattern must deliver:** those four decisions stated once rather than
copied four times, the missed edit made structurally impossible -- and the three
ways the pattern costs more than it saves, printed as numbers rather than
described.
""",
roles=[
    ("The contract", "`TakesPayments`"),
    ("The four services that copy the concerns",
     "`CheckoutService`, `RefundsService`, `SubscriptionBillingService`, `MarketplacePayoutsService`"),
    ("The proxy that runs beside", "`Sidecar`"),
    ("The service with the concerns removed", "`ServiceBehindASidecar`"),
    ("The one configuration, shared", "`SidecarConfig`, `Settings`"),
    ("The supplier at the other end", "`PaymentGateway`"),
    ("The arithmetic that is the argument", "`Concerns`"),
    ("The evidence", "`CallLog`, `Metrics`"),
    ("Time, counted and never slept", "`Clock`"),
    ("Presentation, not policy", "`Money`"),
    ("The values", "`Payment`, `Receipt`, `PaymentFailed`"),
    ("Entry point", "`PaymentsDemo`"),
],
requirements=[
    "**The fault is an absence, not a mistake.** "
    "`SubscriptionBillingService` has no `applyPolicyReview()` method at "
    "all, and `CopiedConcernsTest.billingHasNoWayToApplyTheReview` asserts "
    "that absence. A reader who goes looking for the bug finds nothing "
    "wrong, which is the whole lesson: the copies did not diverge because "
    "somebody was careless.",
    "**One configuration, not four equal ones.** "
    "`SidecarTest.oneConfigurationForAllOfThem` asserts `assertSame`, not "
    "`assertEquals`. Four equal copies would be March again with better "
    "manners, and only identity rules that out.",
    "**The incident is run twice, both ways.** `TheIncidentTest` replays the "
    "same 300ms wobble with copied concerns (13 attempts against an "
    "allowance of 12, marketplace payouts refused, sellers unpaid) and with "
    "a proxy beside each service (12 of 12, nobody refused) -- the same "
    "network, the same gateway, a different place for the policy.",
    "**The saving scales; the code says so without an argument.** "
    "`Concerns.copiesBesideTheServices()` takes no parameter, while "
    "`copiesInsideTheServices(int)` takes the service count: 16 becomes 20 "
    "with a fifth service the old way and stays 4 beside them. "
    "**The missing argument is the answer.**",
    "**The bill is printed, not described.** Act 5 prints copies 16 to 4 and "
    "places 4 to 1, and in the same table processes 4 to 8 -- twice as many "
    "things to run, patch, version and put in a runbook.",
    "**A proxy that will not start takes everything with it.** Act 6 stops "
    "checkout's sidecar on a healthy network and prints `connection refused "
    "to localhost` with `attempts that reached the gateway: 0`; "
    "`SidecarTest.theServiceCannotFallBack` asserts the service has no retry "
    "code left, because it was deleted on purpose.",
    "**The hop is one millisecond, and it is stated in both currencies.** "
    "Act 7 prints 600ms inside against 603ms beside for the same three "
    "attempts -- nothing on a payment, fifty per cent on a two-millisecond "
    "internal call, and paid twice on every hop in a mesh.",
    "**Time is counted, never slept.** `Clock.waitFor(long)` adds to a total "
    "and returns, so a run that narrates 600 milliseconds of backoff "
    "finishes instantly and two runs are byte-identical.",
    "**The admission is in the material, not just the code.** The project "
    "states that inside one JVM this is Decorator, and reduces the choice to "
    "two questions -- must the concern change without rebuilding the "
    "service, and must it serve a language your library does not support. "
    "No to both, and a shared library is cheaper and has one fewer thing "
    "that can fail.",
    "**Every quoted number is the program's.** `DemoRunsTest` captures the "
    "demo's output and asserts the figures the README, the notes and the "
    "video narration speak aloud, that every line fits on a slide, and that "
    "every amount is in pounds.",
],
),

"sidecar-java-proxy": dict(
purpose="""
Turn the previous project's biggest claim -- that a sidecar is
language-independent, so the proxy can be replaced without touching the service
-- from a sentence into something a reader watches happen. It has one job and
it is not explaining what a sidecar is; §41 does that, and this project links
to it and moves on.
""",
nongoals=[
    "Not a second Sidecar lesson. The pattern belongs to §41. A draft that "
    "spends more than one scene on what a sidecar is for has drifted, and "
    "the README opens by naming §41 as the project to read first.",
    "Not a criticism of nginx. nginx wins on almost every count in the "
    "closing table and the project says so; the gap it has is narrow, "
    "deliberate, and a consequence of the case it was designed for.",
    "Not a network lesson. Tier 1 has no socket and no serialisation. The "
    "port is an object with something bound to it, and the phrase *separate "
    "process* is carried by the narration and by `real/`.",
    "Not a performance measurement. `Clock` counts milliseconds and never "
    "sleeps, so the arrival times are identical on every machine and "
    "assertable by a test.",
    "Not a recommendation to write your own proxy. Act 7 is longer than the "
    "benefit, and the rule it lands on is narrow: swap only when the thing "
    "you need cannot be said in the configuration language at all.",
],
problem="""
§41 finished with checkout taking payments through an nginx proxy running
beside it, and the service itself carrying no retry code, no deadline, no
certificate and no counter. That was the right outcome and this project keeps
all of it.

It shipped with a gap, and the gap is not a bug in anybody's code. The payment
provider asked every merchant for two things in writing: at most three attempts
per payment, **and wait properly between them**. nginx can say the first. It
cannot say the second -- retrying means moving to the next server in an
upstream group, that move happens immediately, and there is no directive
anywhere in the http proxy module that introduces a delay first. So the shop's
configuration honours the half of the agreement that limits it and drops the
half that would have helped.

The consequence is exact and it is arithmetic. The provider wobbles for 300
milliseconds. The proxy makes its three allowed attempts at 1ms, 2ms and 3ms,
all of them inside the bad window, and the payment fails having spent the
entire allowance before the provider had time to get better. Nothing in the
service is wrong. Nothing in the configuration is wrong. The sentence that
would have fixed it does not exist in the language the configuration is
written in.

**What this project must deliver:** the same three attempts, spaced out, with
the service not rebuilt, not restarted and not told -- and an honest accounting
of what writing your own proxy costs, because the answer is usually don't.
""",
roles=[
    ("The address the service talks to, and the only thing a swap touches",
     "`LocalPort`"),
    ("What may be bound to it", "`Proxy`"),
    ("The proxy §41 deployed, and its one gap", "`NginxProxy`"),
    ("The forty lines that close the gap", "`JavaProxy`"),
    ("The service, unchanged and never restarted", "`PaymentsService`"),
    ("The one policy both proxies read", "`ProxyPolicy`"),
    ("The supplier at the other end", "`PaymentGateway`"),
    ("The evidence, taken at the far end", "`CallLog`"),
    ("Time, counted and never slept", "`Clock`"),
    ("Presentation, not policy", "`Money`"),
    ("The values", "`Payment`, `Receipt`, `PaymentFailed`"),
    ("Entry point", "`ProxySwapDemo`"),
],
requirements=[
    "**The swap is proved by identity, not by behaviour.** "
    "`TheSwapTest.theServiceIsUntouched` asserts `assertSame` on the "
    "service's port and equality on its start number across the swap. A "
    "service that merely behaved the same afterwards would be a service "
    "somebody had carefully rebuilt.",
    "**The demo could not restart the service if it wanted to.** There is "
    "exactly one `new PaymentsService(...)` in the whole program, in "
    "`main`, and `ServiceStaysEmptyTest` counts the constructions in the "
    "source with comments stripped to prove it.",
    "**The argument is the spacing, and it is measured at the far end.** "
    "`TheSpacingTest` asserts nginx's three attempts arrive at 1ms, 2ms and "
    "3ms and the Java proxy's at 1ms, 202ms and 603ms, using the provider's "
    "own recorded arrival times rather than anything a proxy says about "
    "itself.",
    "**Neither proxy is greedier than the other.** Both spend exactly three "
    "attempts on the same payment against the same allowance; only one of "
    "them gets paid. The allowance is untouched, so the improvement costs "
    "the provider nothing.",
    "**The nginx tests all pass.** They pin a boundary rather than a defect: "
    "the proxy does exactly what its configuration language can express, and "
    "the payment still fails.",
    "**The service source is checked, not just exercised.** "
    "`ServiceStaysEmptyTest` opens `PaymentsService.java` with its comments "
    "stripped and fails if the words retry, backoff, keystore, truststore, "
    "timeout or tls appear in the code.",
    "**The swap window is shown rather than skipped.** Act 6 vacates the "
    "port on a healthy network and prints `attempts that reached the "
    "provider: 0`, because the retry code that would have covered it was "
    "deleted in §41 on purpose, and concludes that a real swap is a rollout "
    "with the old proxy kept installable.",
    "**The bill is longer than the benefit.** Act 7 prints the two proxies "
    "side by side with their languages and line counts, then lists what the "
    "22 lines of somebody else's configuration brought for free and the 40 "
    "lines of your own do not: TLS termination, a structured access log, "
    "connection pooling, and twenty years of answered advisories.",
    "**The rule it lands on is narrow.** Swap when the thing you need cannot "
    "be said in the configuration language at all -- not when it is awkward, "
    "and not when you would rather write Java.",
    "**Every quoted number is the program's.** `DemoRunsTest` captures the "
    "demo's output and asserts the arrival times, the start numbers, the "
    "zero-attempt window and the closing table.",
],
),

"event-sourcing": dict(
purpose="""
Teach the decision to store the things that happened rather than the total they
add up to, and to teach it with its bill attached -- because this is the most
over-applied pattern in the course, and an introduction that only shows what it
buys is a sales pitch.
""",
nongoals=[
    "Not a database, and not durability. The event store is an `ArrayList`. "
    "Ordering and durability are assumed, not demonstrated, and the README "
    "says so.",
    "Not a concurrency lesson. There is one thread and no optimistic "
    "concurrency check, so the question of two writers appending to one "
    "stream at once does not arise here.",
    "Not a performance measurement. The cost figures in Act 6 are events "
    "examined, not milliseconds -- a count the test can assert exactly, "
    "where a timing could not.",
    "Not CQRS. The two are separate decisions, and Act 9 exists to prove it "
    "by building each one without the other.",
    "Not a recommendation. The project argues that most systems should keep "
    "the total, and the closing question is how to tell which kind you have.",
],
problem="""
The shop runs a loyalty scheme: one point per pound, points spendable on later
orders, and unused points expiring after twelve months. The obvious design
keeps a row per customer with a number in it, and that row is correct. It is
correct now and it will still be correct in five years.

It also cannot say why it is 140. The `award` method is handed the customer,
the points, the order id and the date; it uses the points and drops the other
two on the floor. Nobody wrote a bug -- that is simply what keeping the answer
and discarding the working means.

The expensive version of the same problem is a release that awards points
twice and is not noticed for three weeks. The fix is one line. Finding the
damage is impossible, because a doubled £45 order on top of an earlier £10 one
writes the number 100, and one honest £100 order also writes the number 100.
The bug destroyed the evidence of itself every time it fired.

**What the pattern must deliver:** the balance is derived, every answer
explains itself, and a question invented weeks after the fact is answerable
from data that was already lying in the log.
""",
roles=[
    ("The log", "`LoyaltyEventStore`"),
    ("The facts", "`LoyaltyEvent`, `PointsAwarded`, `PointsRedeemed`, `PointsExpired`"),
    ("The fold", "`EventSourcedLoyaltyAccounts`"),
    ("The rejected design", "`CurrentStateLoyaltyAccounts`"),
    ("The cache, and its hazard", "`Snapshot`, `SnapshotStore`"),
    ("Caller", "`Checkout`"),
    ("CQRS, shown separately", "`OrderHistoryReadModel`"),
    ("Entry point", "`LoyaltyBalanceDemo`"),
],
requirements=[
    "**There is no balance field.** `EventSourcedLoyaltyAccounts` holds no "
    "stored total; every number it returns is a fold over the customer's "
    "events, worked out on the call.",
    "**Every answer explains itself.** `explain` prints one line per event "
    "with the running total, including the expiry -- the line support needs "
    "when a customer asks where their points went.",
    "**A past question needs no forethought.** `balanceOn` answers what the "
    "balance was on an earlier date without any history table having been "
    "designed in advance.",
    "**The repair is a read, not a write.** The duplicate-award fix changes "
    "how the log is interpreted; a test asserts the log is byte-identical "
    "before and after, because the shop really did award twice and the log "
    "was never wrong.",
    "**Replay cost is stated as a number.** `SnapshotTest` asserts 5,000 "
    "events examined for one balance, 5,001 after one more order, and 1 with "
    "a snapshot -- the same answer either way.",
    "**A stale snapshot is silently wrong.** A snapshot taken under the buggy "
    "interpretation reports 90 where the repaired fold gives 45, with nothing "
    "thrown and nothing logged; the cure asserted is to discard every "
    "snapshot and refold.",
    "**Erasure fights the pattern.** Deleting a customer's events destroys "
    "the history that explained them *and* leaves a snapshot still answering "
    "with their balance -- both asserted, so the difficulty is shown rather "
    "than described.",
    "**Old events never gain a field.** Awards written before order ids were "
    "recorded make the duplicate hunt return an empty list on a stream that "
    "plainly contains two identical awards.",
    "**CQRS and event sourcing are separated.** `CqrsDistinctionTest` builds "
    "each without the other, including a read model that falls behind its "
    "row, so the two are shown to be independent decisions.",
    "**Every quoted number is the program's.** `DemoRunsTest` captures the "
    "demo's output and asserts the figures the README, the notes and the "
    "video narration quote, and that two runs are byte-identical.",
],
),

"layered-architecture": dict(
purpose="""
Teach a layered architecture as an enforced rule rather than a folder
convention: four layers, each depending only on the one beneath it, with an
ArchUnit test that fails -- naming the offending class -- the moment a
shortcut crosses a boundary the diagram promised it would not.
""",
nongoals=[
    "Not a claim that layering inverts a dependency. The application layer "
    "still names the infrastructure package to compile, and the project "
    "says so plainly -- that inversion is Hexagonal Architecture, the next "
    "project in this category.",
    "Not a web framework tutorial. `CheckoutScreen` has no HTTP anywhere in "
    "it; a controller is, underneath every framework, a method that takes a "
    "request, calls one thing, and formats the answer.",
    "Not a database integration. `OrderTable` has two in-memory "
    "implementations and no real store; the forced change is choosing "
    "between them, not connecting to one.",
],
problem="""
A customer places an order for three products from the shared feature's
catalogue -- one espresso machine, one grinder, two bags of beans, £382.50 -- and
the code that handles it starts as one class doing validation, pricing,
storage and email together: correct, and untestable without constructing the
whole thing at once.

Splitting it into four layers -- presentation, application, domain,
infrastructure -- fixes that, until a new screen needs data the application
layer has no method for yet. Adding one properly costs three files; reaching
past it into storage costs ten minutes and compiles cleanly. The layers still
exist, the folder names are still correct, and nothing in the build objects
to the shortcut.

**What the pattern must deliver:** the same four layers, with the dependency
rule written as a test that fails -- by name -- the moment a class reaches
past its neighbour, and a forced change (replacing the entire storage layer)
performed and counted to prove the other three layers really were
independent of it.
""",
roles=[
    ("Presentation", "`CheckoutScreen`"),
    ("Application", "`PlaceOrderService`, `PlaceOrderRequest`, `PlaceOrderResult`"),
    ("Domain", "`Order`, `OrderLine`, `OrderStatus`, `Product`, `Money`, `CheckoutRefusedException`"),
    ("Infrastructure", "`OrderTable` (interface), `InMemoryOrderTable`, `AppendOnlyOrderTable`, `ProductTable`, `CardNetwork`, `EmailServer`, `PaymentDeclinedException`"),
    ("Naive counterexamples", "`EverythingOrderService`, `OrderHistoryScreen`"),
    ("Composition root / forced-change counter", "`PlaceAnOrderDemo`, `ForcedChange`"),
    ("Entry point", "`PlaceAnOrderDemo`"),
],
requirements=[
    "**An ArchUnit rule asserts the dependency direction, and a second test "
    "proves it can fail.** `ArchitectureTest` checks the real four layers; "
    "`ArchitectureRuleCatchesTheShortcutTest` widens the same rule to the "
    "naive package and asserts the failure message names "
    "`OrderHistoryScreen` and `InMemoryOrderTable` by name.",
    "**The forced change is counted from real files on disk, not typed in.** "
    "`ForcedChange.countClassesInLayers` walks the four layer packages at "
    "the moment the demo runs, so the printed numbers cannot drift from the "
    "source tree.",
    "**The card is charged before anything is written down.** "
    "`PlaceOrderService.place` orders its four steps so that a declined "
    "card leaves no half-placed order and no reduced stock behind.",
],
),

"mvc": dict(
purpose="""
Teach Model-View-Controller as an enforced guarantee rather than a folder
convention: a Model that computes an order's total exactly once, a View
interface too narrow to be handed anything else to compute from, and an
ArchUnit test that fails -- naming the offending class -- the moment a view
reaches around the model into storage.
""",
nongoals=[
    "Not a UI toolkit tutorial. Every view produces a String; there is no "
    "Swing, JavaFX or web framework anywhere in this project.",
    "Not a claim that this project's controller matches classic Smalltalk "
    "MVC's observation. The controller builds the model once and hands it "
    "to the views asked for, rather than views subscribing and being "
    "notified -- the written notes say so plainly, because a synchronous "
    "console demo has no independent redraw to trigger.",
    "Not MVP or MVVM. Both are named and distinguished in one scene each; "
    "neither is built, because teaching either properly needs a UI toolkit "
    "with real data binding.",
],
problem="""
The same order-placing feature as the rest of this category -- Ada Okafor,
three lines, £382.50 -- reaches the moment just after checkout: a screen
summary, and a confirmation email a moment later. Both must show the same
total.

A real screen already exists, reading a computed model, and it works. A
confirmation email is then added, and because the model has no convenient
method yet for "unit prices rounded to the nearest pound, for a tidier
line", the new email view reaches directly into the product catalogue and
rounds each unit price itself before multiplying. It compiles; a reviewer
would approve the diff. It prints £383.00 where the screen prints £382.50,
because the burr grinder's £89.50 rounds up before it is multiplied.

**What the pattern must deliver:** a Model computed once, a View interface
narrow enough that no view can be handed anything to compute a total from,
and a dependency rule -- no class in view may depend on infrastructure --
enforced as a test that fails, naming the offending class, the moment a view
reaches around the model.
""",
roles=[
    ("Model", "`OrderSummaryModel`"),
    ("View interface", "`OrderSummaryView`"),
    ("Concrete views", "`ScreenSummaryView`, `EmailConfirmationView`, `CompositeOrderView`"),
    ("Controller", "`OrderSummaryController`"),
    ("Application", "`PlaceOrderService`, `PlaceOrderRequest`, `PlaceOrderResult`"),
    ("Infrastructure", "`OrderTable`, `InMemoryOrderTable`, `ProductTable`, `CardNetwork`, `EmailServer`"),
    ("Naive counterexamples", "`EverythingOrderScreen`, `RoundedEmailView`"),
    ("Composition root / forced-change counter", "`PlaceAnOrderDemo`, `ForcedChange`"),
    ("Entry point", "`PlaceAnOrderDemo`"),
],
requirements=[
    "**An ArchUnit rule asserts no view depends on infrastructure, and a "
    "second test proves it can fail.** `ArchitectureRuleCatchesTheShortcutTest` "
    "widens the rule to `naive.view` and asserts the failure names "
    "`RoundedEmailView` and `ProductTable` by name.",
    "**Two real views are proven, by arithmetic, to always agree — and the "
    "naive bug is proven, by arithmetic, to be real.** `ViewsAgreementTest` "
    "asserts both: `twoRealViewsAlwaysAgree` and "
    "`theNaiveShortcutReallyDoesDisagree`, the latter computing the actual "
    "£383.00 rather than asserting it in prose.",
    "**`OrderSummaryView` accepts exactly one parameter type.** No overload "
    "anywhere in the interface accepts a `Product`, a price, or a quantity "
    "a view could multiply for itself.",
],
),

"hexagonal-architecture": dict(
purpose="""
Teach ports and adapters as an inversion enforced by a test: the core
declares every interface it needs, in its own language, and no class in the
core may depend on any adapter -- driven or driving -- with the inversion
proved in both directions at once: a storage swap the core does not notice,
and a new caller the core does not notice either.
""",
nongoals=[
    "Not a claim that this project replaces Layered Architecture. It is one "
    "deliberate move on top of it: the same interface, moved into the core, "
    "so the direction of one import reverses.",
    "Not a real HTTP server or a real database. `HttpCheckoutAdapter` "
    "simulates a JSON body as a `Map`; every adapter in this project is "
    "in-memory, because the lesson is the shape of the dependency, not the "
    "infrastructure behind it.",
    "Not a claim that every application needs this. The written notes name "
    "the honest question directly: for a core that will only ever have one "
    "database and one caller, is either swap ever going to happen?",
],
problem="""
The same order-placing feature as the rest of this category reaches the
point where Layered Architecture's own documents admitted a cost: its
application layer named its storage, payment and notification classes by
importing them directly, because the interfaces describing them lived in
the bottom layer, not with the use case.

Reproduced here as `NaivePlaceOrderService`, whose constructor takes three
concrete adapter types. It works. Testing it means constructing all three
first, and swapping any one of them means editing this class -- not because
its logic changed, but because a type it named no longer exists.

**What the pattern must deliver:** a core that declares its own ports and
depends on nothing else, with the rule enforced as a test that fails,
naming the offending class, the moment the core reaches into an adapter --
proved by swapping a driven adapter (storage) and a driving adapter (who
calls in) at the same time, with zero core classes touched by either.
""",
roles=[
    ("Core", "`PlaceOrderService`, `PlaceOrderRequest`, `PlaceOrderResult`"),
    ("Domain", "`Order`, `OrderLine`, `Money`, `Product`, `OrderStatus`, `CheckoutRefusedException`"),
    ("Ports", "`OrderStore`, `PaymentGateway`, `ProductCatalog`, `Notifier`"),
    ("Driven adapters", "`InMemoryOrderStore`, `AppendOnlyOrderStore`, `InMemoryPaymentGateway`, `InMemoryNotifier`, `InMemoryProductCatalog`"),
    ("Driving adapters", "`HttpCheckoutAdapter`, `CliCheckoutAdapter`"),
    ("Naive counterexample", "`NaivePlaceOrderService`"),
    ("Composition root / forced-change counter", "`PlaceAnOrderDemo`, `ForcedChange`"),
    ("Entry point", "`PlaceAnOrderDemo`"),
],
requirements=[
    "**An ArchUnit rule asserts the core depends on no adapter, and a "
    "second test proves it can fail.** `ArchitectureRuleCatchesTheShortcutTest` "
    "widens the rule to `naive.core` and asserts the failure names "
    "`NaivePlaceOrderService` and the adapter it reached for.",
    "**Both directions of the forced change are proven, not merely "
    "described.** `BothSidesAgreeTest` asserts the same core answers "
    "identically through `HttpCheckoutAdapter` and `CliCheckoutAdapter`, "
    "and that swapping `InMemoryOrderStore` for `AppendOnlyOrderStore` "
    "changes no result.",
    "**`PlaceOrderService` imports nothing from `adapter`.** Every "
    "dependency it has is a type declared inside `core.port`.",
],
),

"clean-architecture": dict(
purpose="""
Teach Clean Architecture as Hexagonal Architecture generalised into three
named rings -- entities, use cases, interface adapters -- with the
dependency-inversion moment shown in running code rather than a diagram, and
proved under the category's largest forced change: an entirely new delivery
mechanism and an entirely new data source, added at the same time, with the
two inner circles measurably untouched.
""",
nongoals=[
    "Not a claim that this project is unrelated to Hexagonal Architecture. "
    "It is a close relative, named as one: the same inward-pointing rule, "
    "generalised into three rings instead of one core/adapter split.",
    "Not a dependency injection container. The whole object graph is "
    "wired by hand in `main()`, deliberately, because watching that "
    "wiring is where the inversion stops being a diagram -- the "
    "container version is `clean-architecture-with-spring`, a separate "
    "project.",
    "Not a recommendation to build every feature this way. The written "
    "notes name this as the most over-applied pattern in the category and "
    "count the file cost of one feature to prove it.",
],
problem="""
The previous project in this category, Hexagonal Architecture, already
inverted the dependency between a use case and its storage. This project's
naive version reproduces the shortcut that discipline slips into:
`NaivePlaceOrderInteractor`, a class calling itself a use case with a
constructor typed as three concrete gateway classes, reaching two circles
further out than a use case should.

**What the pattern must deliver:** concentric circles with one rule stated
once -- source code dependencies point only inward -- and the
dependency-inversion moment shown as two directions disagreeing in real
code: control flowing outward to `orders.save(order)`, while the
dependency, the interface `orders` is typed as, points inward at
something the use case itself declared. Proved by the largest forced
change in the category: a new delivery mechanism and a new data source,
added simultaneously, with zero changes to entities or use cases.
""",
roles=[
    ("Entities", "`Order`, `OrderLine`, `Money`, `Product`, `OrderStatus`, `CheckoutRefusedException`"),
    ("Use cases", "`PlaceOrderInteractor`, `PlaceOrderInputBoundary`, `PlaceOrderInput`, `PlaceOrderOutput`"),
    ("Boundaries", "`OrderRepository`, `ProductRepository`, `PaymentGateway`, `NotificationGateway`"),
    ("Interface adapters — in", "`CheckoutController`, `BatchOrderController`"),
    ("Interface adapters — out", "`InMemoryOrderRepository`, `FileBackedOrderRepository`, `InMemoryPaymentGateway`, `InMemoryNotificationGateway`"),
    ("Naive counterexample", "`NaivePlaceOrderInteractor`"),
    ("Composition root / forced-change counter", "`PlaceAnOrderDemo`, `ForcedChange`"),
    ("Entry point", "`PlaceAnOrderDemo`"),
],
requirements=[
    "**The concentric rule is checked with ArchUnit's own layered-architecture "
    "API, not a hand-rolled rule.** `Architectures.layeredArchitecture()` "
    "declares three named layers and one accessibility sentence per pair; "
    "`ArchitectureRuleCatchesTheShortcutTest` widens an equivalent rule to "
    "`naive.usecases` and asserts the failure names "
    "`NaivePlaceOrderInteractor`.",
    "**Both halves of the forced change are proven working at once, not "
    "narrated.** `BothAddedAtOnceTest` exercises the original HTTP-and-map "
    "path and the new batch-and-file path in the same test run.",
    "**`PlaceOrderInteractor` imports nothing from `adapters`.** Every "
    "dependency it has is a type declared inside its own package.",
],
),

"clean-architecture-with-spring": dict(
purpose="""
Teach the one contrast a container adds to Clean Architecture's hand-wired
graph -- compile-time wiring failure against startup wiring failure -- using
the identical entities, use cases and adapters `clean-architecture-pattern`
already built, copied unchanged, so the only variable is who assembles them.
""",
nongoals=[
    "Not a re-teaching of Clean Architecture. Every entity, use case and "
    "adapter is `clean-architecture-pattern`'s file, unchanged; that "
    "project's own explained document is the authority on all of them.",
    "Not a Spring tutorial. This project uses exactly one dependency, "
    "`spring-boot-starter`, and answers exactly one question -- what "
    "changes when a container does the wiring -- before it stops.",
    "Not a web application. There is no web starter, no HTTP server, "
    "anywhere in this project.",
],
problem="""
`clean-architecture-pattern`'s composition root assembles its object graph
by hand, in about twenty lines of `new SomeClass(...)`, in one method
anyone can read top to bottom. That is also, honestly, not what most teams
do the moment there is more than a handful of objects to wire -- most reach
for a container.

**What this project must deliver:** the identical graph, assembled by a
Spring `ApplicationContext` reading one `@Configuration` class with a
`@Bean` method per object the hand-wired project already constructed --
and, from that one change, the contrast the whole project exists to show.
Delete an argument from the hand-wired constructor call and the project
does not compile. Delete the equivalent `@Bean` method and the project
compiles cleanly, then fails only once the container actually tries to
build the graph, with `UnsatisfiedDependencyException` naming the missing
type.
""",
roles=[
    ("Reused unchanged from §66", "every class in `entities`, `usecases` and `adapters`"),
    ("The real wiring", "`AppConfig`"),
    ("The forced-change demonstration", "`BrokenAppConfig`, missing one `@Bean`"),
    ("Entry point", "`Application`"),
],
requirements=[
    "**The contrast is proven, not narrated.** `WiringContrastTest` builds "
    "a working context from `AppConfig` and asserts `BrokenAppConfig` "
    "throws `UnsatisfiedDependencyException` naming the missing "
    "`NotificationGateway` type.",
    "**Spring appears in no file copied from §66.** A dedicated ArchUnit "
    "test asserts no class in `entities`, `usecases` or `adapters` depends "
    "on any `org.springframework` package.",
    "**`docs/dependencies.md` answers the standing five questions** -- "
    "what Spring is, why this project uses it, what to install with the "
    "version pinned, what it costs, and that skipping this project loses "
    "none of the architecture.",
],
),

"producer-consumer": dict(
purpose="""
Teach the gap between how fast orders arrive at checkout and how fast they
can be packed, and the bounded queue that sits between the two so each side
runs at its own pace without either unblocking a shopper for free or letting
unbounded work pile up unseen. This project also builds the three
determinism-forcing pieces -- a one-shot gate, a rendezvous, and a
step-controlled executor -- that every later project in this category
reuses to make a race reproduce on every single run rather than sometimes.
""",
nongoals=[
    "Not a thread pool. The packer here is exactly one thread; what happens "
    "with more than one consumer taking from the same queue is "
    "`thread-pool-pattern`'s subject.",
    "Not about getting a result back. This queue moves one-way, fire and "
    "forget; a caller that needs the packed outcome back is "
    "`future-promise-pattern`'s subject.",
    "Not an argument against `java.util.concurrent.BlockingQueue`. "
    "`BoundedOrderQueue` wraps `ArrayBlockingQueue` rather than "
    "reimplementing it -- the lesson is the shape of the pattern, not "
    "how to hand-roll a queue.",
],
problem="""
Checkout accepts orders. A packing step -- wrapping and labelling the order
for the courier -- handles each one, and packing is slower than orders
arrive. That gap between arrival speed and processing speed is this
project's entire subject.

The naive fix in two parts, both real code in this project. First,
`InlineCheckout`: checkout packs the order itself and does not return until
packing finishes, so one slow pack blocks every checkout behind it.
Second, `ThreadPerOrderCheckout`: hand each order to a brand new thread and
return immediately -- the shopper is never held up, but thread creation has
a real, measured cost, each thread holds a stack whether or not it is
doing anything, and nothing anywhere applies a brake if arrivals ever
outpace packing. The curve this project measures (safely capped, never
triggering the real `OutOfMemoryError`) points straight at that cliff.

**What the pattern must deliver:** a bounded queue between checkout and
packing. Producers offer orders, one packer thread takes them, and each
runs at its own pace up to the bound. The queue's fullness has to be shown
actually full -- forced deterministically with a latch, not guessed at with
a sleep -- and a producer offering into a full queue has to be shown
rejected. Both ways a running system stops have to be shown too: a poison
pill that drains everything queued ahead of it before the packer stops, and
an interrupt that abandons whatever was still queued.
""",
roles=[
    ("Producer", "`InlineCheckout`, `ThreadPerOrderCheckout` (the two naive versions being replaced)"),
    ("Bounded buffer", "`BoundedOrderQueue`, wrapping `ArrayBlockingQueue<Order>`"),
    ("Consumer", "`Packer`, implementing `Runnable`"),
    ("Work item / shutdown signal", "`Order`; `Packer.POISON`, a sentinel `Order`"),
    ("Entry point", "`PackingWarehouseDemo`, five acts"),
    ("Determinism harness", "`Gate` (one-shot latch), `Rendezvous` (barrier-forced interleaving), `StepExecutor` (queues work without running it)"),
],
requirements=[
    "**The queue's capacity is proven full, not asserted full.** Act "
    "Three holds the packer parked mid-pack with a `Gate`, confirms via a "
    "`CountDownLatch` that it has already taken one order before the "
    "remaining orders are queued, fills the queue to its stated capacity, "
    "then shows a further `offer(..., timeout, unit)` time out and return "
    "`false` -- every run, not sometimes.",
    "**Both shutdowns are shown, and neither is ambiguous.** The poison-pill "
    "act asserts every order enqueued ahead of `Packer.POISON` reaches "
    "`packed()`; the interrupt act asserts whatever was still queued behind "
    "the order being packed when the interrupt landed never does.",
    "**Nothing sleeps to wait for a race.** No test and no act of the demo "
    "calls `Thread.sleep` to synchronise with another thread; `PACK_MILLIS` "
    "is the one named, explicit delay this project measures against, never "
    "a substitute for a `Gate`, a `Rendezvous`, or a latch.",
    "**The harness pieces are proven against a real race, not merely "
    "exercised.** `HarnessSelfTest` shows `Rendezvous` forcing the same "
    "lost update on every one of twenty repeated runs, and shows `Gate` "
    "provably still closed -- not just probably -- at the instant before "
    "it opens.",
],
),

"thread-pool": dict(
purpose="""
Teach that a fixed worker count is only half of what "bounded" means for a
pool -- the queue those workers pull from needs its own explicit capacity,
or the exact unbounded-growth failure Producer-Consumer's naive version
has has simply moved one level over, hidden behind a factory method that
looks correct. This project also demonstrates the deadlock a fixed pool
can reach at any size, and states plainly what Java 21's virtual threads
change and what they do not.
""",
nongoals=[
    "Not a re-teaching of the bounded-queue idea. `BoundedPackingPool` "
    "reuses §46's domain and harness unchanged; its own explainer covers "
    "only what is new here -- a second bound, and a rejection with no "
    "patience window.",
    "Not an argument against `java.util.concurrent.ThreadPoolExecutor`. "
    "The pattern class wraps one directly, built with explicit "
    "arguments in place of a factory method's hidden defaults.",
    "Not a virtual-threads tutorial. Act six measures one honest "
    "comparison and states one honest limit, then stops.",
],
problem="""
Producer-Consumer's naive thread-per-order failure returns unchanged in
this project's first act, seen from the packing team's side. The obvious
next step -- `Executors.newFixedThreadPool(2)` -- really does cap the
worker count at two. What it hands those two workers to pull from is an
unbounded queue, built in behind the factory method with no argument
anywhere to change it: submitting never blocks and never rejects, and the
backlog simply grows, silently, until it is a heap dump instead of a
decision.

**What this project must deliver:** a pool with two bounds, both explicit
constructor arguments -- a fixed worker count and a fixed queue capacity
-- built directly on `ThreadPoolExecutor` rather than a factory method's
defaults. It also has to show, deterministically, the deadlock any fixed
pool can reach regardless of either bound: a task that submits a second
task to its own pool and waits for it, with no worker ever free to run
the second one. And it has to say, honestly, what Java 21's virtual
threads change about the cost measured in act one -- and what they do not
change about the bound act three exists to enforce.
""",
roles=[
    ("Reused unchanged from §46", "`Order`, `Packing`, `Gate`, `Rendezvous`, `StepExecutor`"),
    ("Naive, no bound at all", "`ThreadPerOrderPacking`"),
    ("Naive, one bound of two", "`UnboundedPoolPacking`, wrapping `Executors.newFixedThreadPool`"),
    ("Pattern", "`BoundedPackingPool`, wrapping `ThreadPoolExecutor` with an `ArrayBlockingQueue`"),
    ("The deadlock any fixed pool can reach", "`PoolStarvation`"),
    ("Java's answer, measured honestly", "`VirtualThreadFlood`"),
    ("Entry point", "`PackingTeamDemo`, six acts"),
],
requirements=[
    "**Both bounds are proven full, not asserted full.** Act three parks "
    "the pool's one worker on a `Gate`, confirms via a `CountDownLatch` "
    "that it has already started before the queue is filled, fills the "
    "queue to its stated capacity, then shows a further submission "
    "rejected -- synchronously, with no patience window -- every run.",
    "**The unbounded-queue trap is shown with a real number, not a "
    "claim.** `UnboundedPoolPackingTest` parks both of a two-worker "
    "pool's workers deterministically, submits a fixed burst, and "
    "asserts the exact backlog that results -- proving the factory "
    "method's queue accepted every one of them with nobody free to take "
    "any.",
    "**Pool starvation is proven to need no forcing at all.** "
    "`PoolStarvationTest` shows a fixed pool of one worker, given a task "
    "that submits and waits on a second task in the same pool, always "
    "times out -- and a second test shows a pool with a free second "
    "worker does not, proving the failure is about worker count, not "
    "about nesting a submit call in general.",
    "**Nothing sleeps to wait for a race.** No test calls `Thread.sleep`; "
    "`PACK_MILLIS` is the one named, explicit delay this project reuses "
    "from §46, and the pool-starvation rescue timeout is the wait's own "
    "subject, not a substitute for a `Gate` or a latch.",
],
),

"future-promise": dict(
purpose="""
Teach that each unit of independent work should be submitted and asked
for its result later, not asked for immediately -- and that a
`CompletableFuture` is two roles wearing one name, the reader's Future
half and the writer's Promise half, easy to conflate precisely because
one object plays both. This project also pays, honestly and with real
code, the three costs beginners do not expect: a moved exception, a
`get()` that can hang forever, and a cancellation a task is free to
ignore.
""",
nongoals=[
    "Not a `CompletableFuture` callback tutorial. `thenApply`, "
    "`thenCompose` and `thenCombine` are discussed as a named cost -- "
    "readability collapsing past a few chained steps -- not built up as "
    "a technique this project teaches to use.",
    "Not a re-teaching of the bounded queue or the worker pool. This "
    "project reuses §46's harness unchanged and assumes the reader has "
    "met either §46 or §47 already.",
    "Not an argument against `Future.cancel`. It is a real, useful "
    "signal -- the point is narrower: it is a request a task must "
    "itself check for, never a guarantee.",
],
problem="""
A product page needs three independent catalogue lookups -- price, stock,
a review score -- each measured in this project at two hundred
milliseconds. None depends on either of the other two. The naive version
still calls them one after another, paying all three delays added
together for no reason the data itself demands.

**What this project must deliver:** each lookup submitted at once,
returning a handle to a result that does not yet exist, so the total cost
is roughly the slowest single lookup rather than the sum of all three. It
also has to make the Future/Promise split concrete rather than merely
described -- one object, a reader thread blocked on `get()`, a writer
thread elsewhere calling `complete()` -- and it has to demonstrate,
deterministically, the three costs a beginner reaches for a `Future` and
does not expect: an exception that surfaces later and wrapped, with a
stack trace containing none of the calling thread's frames; a `get()`
with no timeout that is a hang rather than a wait; and a `cancel(true)`
that a task ignoring interruption simply outlives.
""",
roles=[
    ("Reused unchanged from §46", "`Gate`, `Rendezvous`, `StepExecutor`"),
    ("Naive, no overlap", "`SequentialProductPage`"),
    ("Pattern", "`ConcurrentProductPage`, submitting three `Future`s at once"),
    ("The two halves, made explicit", "`FutureAndPromise`"),
    ("The three honest costs", "`AsyncFailure`, `UnboundedWait`, `CooperativeCancellation`"),
    ("Entry point", "`ProductPageDemo`, six acts"),
],
requirements=[
    "**Concurrency is proven, not inferred from a short elapsed time.** "
    "`ConcurrentProductPageTest` parks all three lookups on separate "
    "gates, confirms via a shared `CountDownLatch` that all three have "
    "started before any is released, and only then opens them -- proving "
    "true overlap rather than merely a fast sequence.",
    "**The reader/writer split is proven ordered, not merely fast.** "
    "`FutureAndPromiseTest` parks the writer's own work behind a `Gate` "
    "a second thread opens, so the writer's side effect can only be "
    "observed true after the gate opens -- proving the reader's result "
    "cannot have arrived before the writer's work actually ran.",
    "**The hang is proven to need no forcing at all.** "
    "`UnboundedWaitTest` parks a task on a `Gate` the test never opens; "
    "timing out is not a probability, it is the only possible outcome, "
    "on every run.",
    "**Cancellation ignoring interruption is proven against a real "
    "race, not merely exercised.** `CooperativeCancellationTest` waits "
    "on a `CountDownLatch` confirming the task has actually started "
    "before calling `cancel(true)` -- cancelling before the task starts "
    "would let the executor skip it entirely, proving nothing about a "
    "running task ignoring interruption.",
    "**Nothing sleeps to wait for a race.** No test calls `Thread.sleep`; "
    "`LOOKUP_MILLIS` is the one named, measured subject reused from "
    "§46's convention, `CooperativeCancellation`'s three short sleeps are "
    "the anti-pattern being demonstrated, and the rescue timeout in act "
    "five ends a genuine hang rather than substituting for a `Gate`.",
],
),

"read-write-lock": dict(
purpose="""
Teach that many readers may safely share a lock while a writer needs it
alone, because two reads can never conflict and only a write can -- and
then pay, honestly and with real code, what the pattern does not tell
you: a queued writer can be overtaken, a read lock can never be
upgraded, and for a read as cheap as returning one price the lock can
lose to a plain mutex and to an immutable snapshot.
""",
nongoals=[
    "Not a tour of every `java.util.concurrent.locks` class. "
    "`StampedLock` and optimistic reads are outside this project.",
    "Not a re-teaching of the harness. `Gate`, `Rendezvous` and "
    "`StepExecutor` are reused unchanged from §46.",
    "Not an argument against `ReentrantReadWriteLock`. Act six says "
    "when it loses; it does not say it never wins.",
],
problem="""
A product's price is an amount and a currency kept together, read by a
thousand shoppers and changed now and then by a merchandiser. With no
lock, a reader can land between the writer's two steps and see the new
amount with the old currency -- a price that never existed. One plain
lock fixes that, but makes every reader queue behind every other reader,
though two readers can never conflict.

**What this project must deliver:** a catalogue whose readers share a
read lock while a writer takes the write lock alone. It also has to
demonstrate, deterministically, the torn read it prevents; a queued
writer overtaken by a later reader; a thread that requests the write
lock while holding the read lock and waits on itself; and a measured
comparison in which the lock loses to a plain mutex and to an immutable
snapshot for a read this cheap.
""",
roles=[
    ("Reused unchanged from §46", "`Gate`, `Rendezvous`, `StepExecutor`"),
    ("Domain", "`Price`, an immutable record of amount and currency"),
    ("Naive", "`UnsynchronizedCatalogue`, `SingleLockCatalogue`"),
    ("Pattern", "`ReadWriteCatalogue`, wrapping `ReentrantReadWriteLock`"),
    ("The honest costs", "`WriterBarging`, `UpgradeDeadlock`"),
    ("The honest alternative", "`SnapshotCatalogue`, an `AtomicReference` to an immutable `Price`"),
    ("Entry point", "`CatalogueDemo`, six acts"),
],
requirements=[
    "**The torn read is forced, not hoped for.** The writer signals a "
    "`CountDownLatch` after setting the amount and then parks on a "
    "`Gate` before setting the currency, so the reader is proven to land "
    "in the gap on every run.",
    "**Writer barging is proven from a genuinely queued writer.** "
    "`WriterBargingTest` confirms the writer is waiting on the lock "
    "before the second reader's `tryLock()` is attempted.",
    "**The upgrade deadlock is rescued by a timeout the test owns.** "
    "`UpgradeDeadlockTest` requests the write lock while holding the "
    "read lock and asserts the request never completes on its own.",
    "**Nothing sleeps to wait for a race.** No test calls `Thread.sleep`; "
    "the throughput figures in acts two, three and six are real "
    "measurements and are never asserted as exact numbers.",
],
),

"monitor-object": dict(
purpose="""
Teach that an object which owns its lock and its waiting cannot be used
unsafely, and that a lock left to the caller, a `volatile` field, or a
plain count are each weaker. It also pays the honest costs: a lock that
is a bottleneck by design, a `wait` that must sit in a loop, and two ways
a correct monitor still deadlocks.
""",
nongoals=[
    "Not a tour of `java.util.concurrent`. `AtomicInteger` is named as the "
    "simpler answer for one counter and not built up.",
    "Not a re-teaching of the harness. `Gate`, `Rendezvous` and "
    "`StepExecutor` are reused unchanged from §46.",
    "Not an argument against locks. The point is who should own them.",
],
problem="""
One stock count per product, reduced by many checkout threads and
increased by a delivery thread. A plain count loses updates; `volatile`
does not help; a lock held by the caller is only as good as the least
careful caller.

**What this project must deliver:** a `StockMonitor` whose lock and
condition are private, so callers cannot forget them, and in which a
thread needing stock waits and is signalled. It has to demonstrate,
deterministically, the lost update, the `volatile` half-fix, the
forgetful caller, `if` instead of `while`, nested monitors in opposite
orders, and a callout made while holding the lock.
""",
roles=[
    ("Reused unchanged from §46", "`Gate`, `Rendezvous`, `StepExecutor`"),
    ("Naive", "`PlainStock`, `VolatileStock`, `CallerLockedStock`"),
    ("Pattern", "`StockMonitor`, a `ReentrantLock` and a `Condition`"),
    ("The honest costs", "`IfInsteadOfWhile`, `MonitorHazards`"),
    ("Entry point", "`StockDemo`, six acts"),
],
requirements=[
    "**The lost update is forced, not hoped for.** A two-party "
    "`Rendezvous` runs between the read and the write, so both threads "
    "have read before either writes.",
    "**`if` instead of `while` is proven from the wait queue.** The demo "
    "waits until the condition reports two waiters before adding the item.",
    "**The nested-monitor deadlock is detected by the JVM.** "
    "`ThreadMXBean.findDeadlockedThreads()` reports it, and interrupting "
    "both threads breaks it.",
    "**Nothing sleeps to wait for a race.** No test calls `Thread.sleep`.",
],
),

"active-object": dict(
purpose="""
Teach the capstone of the category: an object with its own thread, whose
calls become messages that return a future at once, and which needs no
lock because exactly one thread owns its state. It is an assembly of the
queue from §46, a thread from §47, a future from §48 and state ownership
from §50, and it says so. It also pays the honest costs: a mailbox that
can back up, errors that arrive later with the worker's stack, and a
single-worker throughput ceiling.
""",
nongoals=[
    "Not a re-teaching of the four projects it is made of. It links to each "
    "and covers only what the assembly adds.",
    "Not an actor framework. Actors and event loops are named as where the "
    "idea went and taught no further.",
    "Not a bounded mailbox. Adding one is the exercise the video ends on.",
],
problem="""
Inventory updates arrive from checkout, returns and a slow back-office
import. A monitor is correct, but a checkout thread waits behind a slow
import while it holds the lock.

**What this project must deliver:** an `InventoryActiveObject` whose calls
return a `CompletableFuture` at once and whose only lock-free state is
owned by one worker thread. It has to demonstrate, deterministically, the
blocked caller under a monitor, the call that returns first, a mailbox
that backs up, an error whose stack is the worker's, and a throughput
ceiling that more callers do not raise.
""",
roles=[
    ("Reused unchanged from §46", "`Gate`, `Rendezvous`, `StepExecutor`"),
    ("Naive", "`MonitorInventory`, the monitor from §50"),
    ("Pattern", "`InventoryActiveObject`, a mailbox, a worker and futures"),
    ("The measured costs", "`Mailbox`, backlog and throughput"),
    ("Entry point", "`InventoryDemo`, six acts"),
],
requirements=[
    "**The call is proven to return first.** The worker is parked on a "
    "`Gate`, confirmed by a `CountDownLatch`, before `reserve` is called.",
    "**No lock is credited for correctness.** Four callers are released "
    "together and the total must be exact with no lock in the class.",
    "**The error's stack is the worker's.** The exception is created "
    "inside the message and the test checks the calling class is absent.",
    "**The ceiling is measured with real work, not sleeping.** Each "
    "message spins for 50 microseconds, and more callers must not double "
    "the rate.",
],
),

"data-mapper": dict(
purpose="""
Teach that a domain object need not know how it is stored: a mapper class
moves data between the object and its rows. The project treats Active Record
fairly first, and shows it working, then pays the honest costs of the
mapper: a second class per entity, a hand-written mapping that can lose a
field without any error, and an indirection to understand before debugging.
""",
nongoals=[
    "Not an argument against Active Record. It is shown working and named as "
    "the right answer for a simple application.",
    "Not object-graph loading. How far a mapper should load belongs to the "
    "Lazy Load project.",
    "Not a framework tutorial. The build files hold no framework; JPA is "
    "named as where you have already met the pattern.",
],
problem="""
The store's customers have a name, an email, a postal address and loyalty
points. Active Record, an object that saves itself, works well. Its cost is
that the customer class then knows tables, columns and the database, so a
domain rule needs a database to test, and one class per table cannot
describe a customer stored across two tables or a table that feeds two
objects.

**What this project must deliver:** a `CustomerMapper` that reads and writes
both tables and builds a `Customer` with no persistence code in it. It has
to show Active Record working, the cost, both awkward shapes, and a mapping
that silently loses a field.
""",
roles=[
    ("The shared fixture", "`Database`, `Table`, `Row`, the toy database"),
    ("Domain", "`Customer`, `Address`, `CustomerSummary`"),
    ("Naive", "`ActiveRecordCustomer`"),
    ("Pattern", "`CustomerMapper`"),
    ("The bill", "`CarelessCustomerMapper`"),
    ("Entry point", "`CustomerDemo`, six acts"),
],
requirements=[
    "**Active Record is shown working first.** `ActiveRecordCustomerTest` "
    "proves save, find and update in three counted operations.",
    "**The customer holds no persistence state.** `CustomerTest` inspects the "
    "class by reflection and constructs one with no database.",
    "**Every count comes from the counter.** The demo prints the toy "
    "database's own operation log.",
    "**The silent field is proven.** `CustomerMapperTest` shows a careless "
    "mapper succeeds and loses the postcode.",
],
),

"identity-map": dict(
purpose="""
Teach that one row should be one object per session: a map from id to the loaded object. The project shows the lost-change bug that two objects for one row cause, why `equals()` does not prevent it, and then pays the costs: a stale cache, held references, and a scope that must be chosen.
""",
nongoals=[
    'Not a caching tutorial. The map is a session-scoped identity guarantee, not a performance cache.',
    'Not JPA. The persistence context is named as where the pattern has been met.',
    'Not concurrency. The toy database is single-threaded throughout.',
],
problem="""
An order is loaded, with its customer, and the same customer is loaded again by id. With a new object per load there are two objects for one row, and saving both loses one change.

**What this project must deliver:** a `CustomerSession` whose `find` returns the same object for the same id, with the costs shown: staleness, memory and scope.
""",
roles=[
    ('The shared fixture', '`Database`, `Table`, `Row`'),
    ('Domain', '`Customer`, `Order`'),
    ('Naive', '`PlainCustomerMapper`'),
    ('Pattern', '`IdentityMap`, `CustomerSession`'),
    ('Entry point', '`CustomerSessionDemo`, six acts'),
],
requirements=[
    '**Identity is proven with `==`, not `equals`.** `CustomerSessionTest` uses `assertSame`.',
    '**The lost change is proven.** `PlainCustomerMapperTest` saves two objects for one row and reads the table.',
    "**The saving is counted.** A second find costs zero operations, read from the toy database's own counter.",
    '**Staleness is proven.** The table is written directly and the session still returns the old value.',
],
),

"unit-of-work": dict(
purpose="""
Teach that a business action which writes several rows should register its changes and write them together, in one short transaction, in an order the database accepts, or not at all. It shows the wreckage of objects that save themselves, fairly treats the transaction-wrapper, and pays the costs of ordering, dirty tracking and memory that disagrees with the database.
""",
nongoals=[
    'Not a transaction manager. The toy database has begin and rollback only.',
    'Not Spring. `@Transactional` is named as where the pattern has been met.',
    'Not concurrency. There is one thread, so lock time is a model in ticks.',
],
problem="""
Placing an order writes seven rows and the third stock update is rejected. Objects that save themselves leave half an order, and a wrapping transaction fixes that but stays open for the whole computation.

**What this project must deliver:** a `UnitOfWork` that registers changes, writes nothing until commit, sorts parents before children, and rolls back completely on failure.
""",
roles=[
    ('The shared fixture', '`Database` with transactions and a foreign key, `Table`, `Row`'),
    ('Domain', '`Product`, `Order`, `OrderLine`, `Shop`'),
    ('Naive', '`SelfSavingPlacement`, `TransactionalPlacement`'),
    ('Pattern', '`UnitOfWork`, `UnitOfWorkPlacement`'),
    ('Entry point', '`OrderDemo`, six acts'),
],
requirements=[
    '**The wreckage is real.** `PlacementTest` fails the sixth write and reads the tables.',
    '**Nothing touches the database until commit.** `UnitOfWorkTest` asserts zero operations after registration.',
    '**Failure rolls back completely.** The seventh write is rejected and every table is read back.',
    '**The ordering cost is real.** Committing in registration order breaks the foreign key.',
],
),

"lazy-load": dict(
purpose="""
Teach that related data should be loaded when asked for, not all at once, and pay the heavy bill honestly: N+1 queries, a field access that is now I/O and can fail, and a load that fails at the point of use after its session has gone. It shows four variants because a reader will meet all four.
""",
nongoals=[
    'Not Hibernate. `LazyInitializationException` is named as where the failure has been met; the Hibernate project reproduces it.',
    'Not a query-tuning guide. Batching is shown as one fix, not built up.',
    'Not concurrency. The toy database is single-threaded.',
],
problem="""
Loading one order eagerly creates thirty-seven objects with twenty-six operations. Loading lazily fixes that and introduces N+1 and a failure that surfaces where the object is used.

**What this project must deliver:** the four lazy variants, N+1 counted as twenty-one queries against two, a failing read, and a closed session that fails at the point of use.
""",
roles=[
    ('The shared fixture', '`Database` with a failing read, `Table`, `Row`'),
    ('Domain', '`Shop`, a seeded store'),
    ('Naive', '`EagerOrderLoader`'),
    ('Pattern', '`LazyInitOrder`, `CustomerProxy`, `ValueHolder`, `GhostCustomer`, `Session`'),
    ('The bill', '`OrderList`, `SessionClosedException`'),
    ('Entry point', '`LazyLoadDemo`, six acts'),
],
requirements=[
    '**The eager count is exact.** `LazyLoadTest` asserts 37 objects and 26 operations.',
    "**N+1 is counted.** Twenty-one queries lazily and two batched, from the toy database's counter.",
    '**A lazy failure is at the point of use.** The proxy is created, the session closed, and the exception thrown only on access.',
    '**Each variant loads once.** Zero before use, one after the first, one after the second.',
],
),

"repository": dict(
purpose="""
Teach that a caller should ask an interface that looks like a collection of domain objects, not a table. It shows the same query drifting across three services, a silent schema-change failure, and then swaps the backing store with no change to the caller, and pays the costs: a method per question, a leak when performance matters, and a swap that is claimed more than it is used.
""",
nongoals=[
    'Not CQRS. The read and write split belongs to the microservices category.',
    'Not Spring Data. It is named as where the pattern has been met.',
    'Not a specification framework. One small specification interface is shown as the fix for method growth.',
],
problem="""
London customers who ordered in the last month are wanted by three teams. Written as a query in each service, the answers differ and a column rename empties all of them silently.

**What this project must deliver:** a `CustomerRepository` interface with two stores behind it, a service that knows only the interface, the swap shown, and the costs shown.
""",
roles=[
    ('The shared fixture', '`Database`, `Table`, `Row`'),
    ('Domain', '`Customer`, `Order`, `Shop`'),
    ('Naive', '`SqlInTheService`'),
    ('Pattern', '`CustomerRepository`, `InMemoryCustomerRepository`, `ToyDatabaseCustomerRepository`, `MarketingService`'),
    ('The bill', '`Specification`, `QueryMethodGrowth`'),
    ('Entry point', '`CustomerDemo`, six acts'),
],
requirements=[
    '**The drift is real.** `SqlInTheServiceTest` shows three answers to one question.',
    '**The swap is proven.** The same service gives the same answer on both stores, and reflection shows it names only the interface.',
    "**The leak is counted.** Seven operations for six customers, from the toy database's counter.",
    '**The rename is silent.** Every list is empty and nothing throws.',
],
),

"service-layer": dict(
purpose="""
Teach that the operations an application offers belong in one layer that every entry point calls, with the rules in the domain and the orchestration and transaction in the service. It anchors on a second entry point whose copied logic drifts, treats putting everything in the domain object fairly, and names the anemic domain model with an honest dividing line.
""",
nongoals=[
    'Not Spring. `@Service` and `@Transactional` are named as where the pattern has been met.',
    'Not a domain-modelling course. Transaction Script and Table Module are named only.',
    'Not concurrency. There is one thread.',
],
problem="""
Placing an order is written into the web controller. When support gets a command line the logic is copied, and later fixes reach one copy only, so a customer is charged or not depending on the door.

**What this project must deliver:** one `OrderService.placeOrder` that both doors call, with the transaction at the service and the rules in the domain, plus the anemic-model cost and the honest line.
""",
roles=[
    ('The shared fixture', '`Database` with transactions, `Table`, `Row`'),
    ('Domain', '`Order`, `Product`, `OrderRequest`, `CartLine`, `Shop`, and the fakes `PaymentGateway`, `EmailService`'),
    ('Naive', '`ControllerLogic`, `CopiedInTheCli`, `SelfPlacingOrder`'),
    ('Pattern', '`OrderService`, `WebController`, `SupportCli`'),
    ('The bill', '`AnemicOrder`'),
    ('Entry point', '`PlaceOrderDemo`, six acts'),
],
requirements=[
    '**The drift is real.** `ServiceLayerTest` shows the copied door charging 6000 pence for a refused order.',
    '**Both doors agree.** With one `placeOrder` the two doors give the same answer.',
    '**A refusal rolls back.** Nothing is written or emailed.',
    '**The rules live in the domain.** Tests call `Order.from` and `Product.reserve` directly.',
],
),

"dto": dict(
purpose="""
Teach that what crosses a boundary should be a separate object shaped for it, not the domain object. It shows the leak, the private-field-name coupling and the lazy history loaded by serialisation, then the DTO record, and pays the costs: mapping code, DTOs that multiply, and a mapping that decides what loads. It shows one DTO and one domain object to keep them from being conflated.
""",
nongoals=[
    'Not Jackson or Spring. They are named as where the pattern has been met; a tiny serialiser is built by hand.',
    'Not MapStruct. It is named as what to take after the tedium has been felt.',
    'Not a REST tutorial. There is no server.',
],
problem="""
An endpoint returns a customer. Returning the domain object leaks the password hash, loads and sends the whole order history, and turns private field names into a public contract.

**What this project must deliver:** a flat `CustomerDto` record, a mapper, and the costs: mapping code, DTOs that multiply, and what the mapping loads.
""",
roles=[
    ('The serialiser', '`MiniJson`, which walks every field'),
    ('Domain', '`Customer`, `LazyOrders`, `Order`, `OrderLine`'),
    ('Naive', '`CustomerEndpointReturningTheDomainObject`, `CustomerAfterRename`'),
    ('Pattern', '`CustomerDto` and its siblings, `CustomerMapper`'),
    ('Entry point', '`CustomerEndpointDemo`, six acts'),
],
requirements=[
    '**The leak is measured.** `DtoTest` asserts the password hash is in the JSON and that the payload exceeds 5000 characters.',
    "**The coupling is shown.** Renaming a private field turns the client's key lookup into null.",
    '**The DTO is measured.** Its JSON is exactly the three fields and loads nothing.',
    '**A DTO is not a model.** The domain object refuses a bad email and the DTO carries it.',
],
),

"identity-map-with-jpa": dict(
purpose="""
Show the Identity Map pattern inside JPA, over the partner project's own customer and order: the persistence context is the map, so two finds in one context give the same object. It then shows the failure of its own, that a second context gives a second object and a change to a detached object is silently not saved, plus staleness and growth.
""",
nongoals=[
    'Not a re-teaching of Identity Map. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a JPA tutorial. Two annotations are introduced and nothing more.',
    'Not Spring. Hibernate is used directly; Spring Boot supplies only version numbers.',
],
problem="""
Identity Map built the pattern by hand. In JPA the `EntityManager` already has one, called the persistence context. This project shows the same customer 7 and order 100 through it, and the failures that are JPA's own.

**What this project must deliver:** `first == second` being true in one context, both changes kept, two contexts giving two objects, a detached change not saved, and a `docs/dependencies.md` saying what Hibernate and H2 are.
""",
roles=[
    ('Reused from the partner', '`Customer` and `CustomerOrder`, with `@Entity`, `@Id` and `@ManyToOne` added'),
    ('Framework setup', '`JpaSetup`, an `EntityManagerFactory` over in-memory H2'),
    ('Entry point', '`CustomerJpaDemo`, six acts'),
],
requirements=[
    '**Identity is proven with `assertSame`.** `PersistenceContextTest`.',
    "**SQL counts come from Hibernate's statistics.** One statement for two finds.",
    '**The detached failure is real.** A change made after the context closed is absent from a new context.',
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"lazy-load-with-hibernate": dict(
purpose="""
Explain LazyInitializationException from its mechanism: a lazy field holds a generated proxy that needs its session to load. It produces the real exception on purpose over the partner project's own store, then shows the three usual fixes and what each honestly costs: an open session with hidden N+1, a join fetch that sends eighty rows for twenty orders, and a projection that needs a class per query.
""",
nongoals=[
    'Not a re-teaching of Lazy Load. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a Hibernate tutorial. Two annotations and a few queries are introduced as they appear.',
    'Not Spring. Hibernate is used directly; Spring Boot supplies only version numbers.',
],
problem="""
Lazy Load built a session-closed failure by hand. Hibernate's version has a name, `LazyInitializationException`, and is among the most searched Java errors.

**What this project must deliver:** the real exception raised on purpose, the proxy shown, and the three usual fixes each with its measured cost, plus a `docs/dependencies.md` saying what Hibernate and H2 are.
""",
roles=[
    ('Reused from the partner', 'The store: customers, orders, lines, products and categories, as entities'),
    ('Framework setup', '`HibernateSetup`, a `SessionFactory` over in-memory H2'),
    ('The failure and the fixes', '`OrderPage`'),
    ('Entry point', '`LazyHibernateDemo`, six acts'),
],
requirements=[
    "**The exception is real.** `LazyLoadHibernateTest` asserts `LazyInitializationException` with 'no session'.",
    '**The proxy is shown.** It is not a `Customer`, is uninitialised, and knows its id without loading.',
    "**Every count is Hibernate's.** Six, twenty-one, one, and eighty rows.",
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"unit-of-work-with-spring": dict(
purpose="""
Show that `@Transactional` is a unit of work: changes held and written at commit, or not at all. It runs the partner project's three-line order through Spring and shows the failures that are Spring's own: a checked exception that commits anyway, a flush written at a line that says nothing about writing, and an annotation ignored by a call on `this`.
""",
nongoals=[
    'Not a re-teaching of Unit of Work. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a Spring tutorial. `@Service` and `@Transactional` are introduced as they appear.',
    'Not a web project. There is no controller and no web starter.',
],
problem="""
Unit of Work built the mechanism by hand. In Spring it is one annotation, whose surprises are its own.

**What this project must deliver:** the writes shown arriving at commit, the same three-line failure rolled back, a checked exception committing half an order, `rollbackFor` as the fix, a query-triggered flush, a `this` call ignoring the annotation, and a `docs/dependencies.md`.
""",
roles=[
    ('Reused from the partner', 'The three-line order and the failing third stock update, as entities'),
    ('Framework setup', '`OrderApplication`, a Spring Boot application over in-memory H2'),
    ('The pattern and its failures', '`TransactionalPlacement`, `CheckedFailurePlacement`, `FlushNobodyWrote`, `SelfInvocation`'),
    ('The comparison', '`SelfSavingPlacement`, `Shelf`'),
    ('Entry point', '`OrderApplication`, six acts'),
],
requirements=[
    "**What is committed is read back.** `TransactionalTest` reads the tables, not the code's intent.",
    '**The checked exception is real.** Half an order is asserted committed under `@Transactional`.',
    "**The flush is counted.** Hibernate's statistics show zero, zero, then one.",
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"repository-with-spring-data": dict(
purpose="""
Show the Repository pattern as Spring Data supplies it: an interface with no implementation that works, and a query generated from a method's own name, run against the partner project's own customers and question. It pays the costs: a name that can be wrong and is unchecked by the compiler, an abstraction that leaks on speed, and the failure of its own, a managed entity that is written with no save inside a transaction and silently lost outside one.
""",
nongoals=[
    'Not a re-teaching of Repository. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a Spring Data tutorial. `JpaRepository` and a few finders are introduced as they appear.',
    'Not a web project. There is no controller and no web starter.',
],
problem="""
Repository built one interface and two implementations by hand. Spring Data needs none.

**What this project must deliver:** an interface with no implementing class, a query generated from a name giving the partner's answer, the name-growth and typo cost, the N+1 and entity-graph counts, the managed-entity leak in both directions, and a `docs/dependencies.md`.
""",
roles=[
    ('Reused from the partner', 'The customers, the orders, and `MarketingService` with its body unchanged'),
    ('Framework setup', '`CustomerApplication`, a Spring Boot application over in-memory H2'),
    ('The pattern', '`CustomerRepository`, an interface with no implementation'),
    ('The failure', '`LeakDemo`'),
    ('Entry point', '`CustomerApplication`, six acts'),
],
requirements=[
    '**There is no implementing class.** `SpringDataRepositoryTest` asserts the injected object is a generated proxy.',
    "**The generated query is counted.** One statement, from Hibernate's statistics.",
    '**The leak is real in both directions.** A change is written with no save inside a transaction, and lost outside one.',
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"null-object": dict(
purpose="""
Teach Null Object, and when not to use it. It shows null checks spreading across eight call sites until one is forgotten and throws a real NullPointerException, then a null object that removes every check with identical behaviour, and pays the bill most treatments omit: a null object hides errors, turning a failed lookup into a silent full-price order. It ends with a plain verdict and the two honest alternatives, Optional and an explicit failure.
""",
nongoals=[
    'Not an argument that null objects are wrong. The verdict is that legitimate absence is the right use.',
    "Not a tour of Optional's API. It is shown as the alternative that keeps absence and failure apart.",
    'Not concurrency. There is one thread.',
],
problem="""
Most customers have no discount. Returning null makes every caller check, and one of eight forgot.

**What this project must deliver:** a `NoDiscount` that removes every check with identical behaviour, the silent-failure cost demonstrated, `Optional` and explicit failure shown fairly, and a plain verdict.
""",
roles=[
    ('Domain', '`Discount`, `LoyaltyDiscount`, `StaffDiscount`, `DiscountDirectory`, `DiscountServiceDown`'),
    ('Naive', '`NaiveCheckout`, eight methods, seven with a null check'),
    ('Pattern', '`NoDiscount`, `NullObjectDirectory`, `NullObjectCheckout`'),
    ('The bill and the alternative', '`ForgivingDirectory`, `OptionalDirectory`'),
    ('Entry point', '`DiscountDemo`, six acts'),
],
requirements=[
    '**The forgotten check is a real `NullPointerException`.** `NullObjectTest` asserts it.',
    '**The behaviour is identical.** The naive and null-object checkouts give the same total for every customer.',
    '**The bill is demonstrated.** A forgiving directory charges 10000 pence instead of 9000 on an outage.',
    '**The verdict is stated aloud.** The video and the explainer end with it.',
],
),

"object-pool": dict(
purpose="""
Teach Object Pool, and when it makes things worse. It shows the pattern earning its keep on an expensive payment connection, then pays the four costs with evidence: pooling a small object measured about three times slower than allocating it with the method documented, a returned connection leaking one customer's data to the next, an exhausted pool that hangs, and a size that is wrong in both directions. It ends with a plain verdict.
""",
nongoals=[
    'Not JMH. The benchmark is hand-rolled with warm-up, medians and a documented method, and claims a direction, not an absolute number.',
    'Not a connection-pool library tutorial. The pool is a small class built here.',
    "Not a re-teaching of Thread Pool. It is linked as the pattern's other correct use.",
],
problem="""
The payment gateway connection takes 200 milliseconds to make. A connection per payment is slow.

**What this project must deliver:** a pool that fixes it, and then honest evidence for the four costs: a small pooled object slower than allocation, a dirty return, a leak, and mis-sizing, ending with a plain verdict.
""",
roles=[
    ('Domain', '`PaymentConnection`, expensive to make and stateful'),
    ('Naive', '`ConnectionPerPayment`'),
    ('Pattern', '`ConnectionPool`'),
    ('The evidence', '`Receipt`, `SmallObjectBenchmark`'),
    ('Entry point', '`PaymentDemo`, six acts'),
],
requirements=[
    '**No test asserts a timing.** `ObjectPoolTest` asserts connection counts, dirty state and timeouts.',
    "**The benchmark's method is written down.** Warm-up, median, and allocation measured with and without escape.",
    '**The dirty return is real.** The next borrower reads the previous card holder.',
    '**The verdict is stated aloud.** Pool what is expensive outside the JVM, and nothing else.',
],
),

"registry": dict(
purpose="""
Teach Registry honestly: a well-known place to find things, which removes the friction of passing a dependency through six constructors and pays for it with global state. It shows the naive version fairly, the registry removing the friction, and then four costs with runnable evidence: dependencies invisible in the signature, a test failing because of the order the tests ran in, contents unanswerable from any one file, and thread safety. It ends with a plain verdict and states the progression to Service Locator and Dependency Injection.
""",
nongoals=[
    'Not an argument that every static lookup is wrong. The verdict names the narrow place a registry is best.',
    'Not a re-teaching of Service Locator or Dependency Injection. They are the next two projects and are linked.',
    'Not a thread-safety tutorial. The map is concurrent, and the point is that the question now exists.',
],
problem="""
The payment gateway is needed six classes down. Passing it through six constructors is friction, and every class but the last only forwards it.

**What this project must deliver:** a registry that removes the friction, and evidence for its costs, ending with a plain verdict.
""",
roles=[
    ('The shared collaborators', '`DiscountPolicy`, `PaymentGateway`, `Notifier`, and `ForwardChain`'),
    ('Naive', '`PassedDownCheckout`'),
    ('Pattern', '`Registry`, `RegistryCheckout`'),
    ('The evidence', '`OrderDependence`'),
    ('Entry point', '`CheckoutDemo`, six acts'),
],
requirements=[
    '**The naive version is treated fairly.** The friction is shown and said to be real, and honest.',
    '**Order dependence is runnable.** `RegistryTest` runs the same two tests in both orders and asserts different outcomes.',
    '**Invisible dependencies are proven.** `new RegistryCheckout()` has a zero-argument constructor and fails on first use.',
    '**The verdict is stated aloud.** Narrowly, and never for what tests must replace.',
],
),

"service-locator": dict(
purpose="""
Teach Service Locator by making the case against it honestly, with runnable evidence, while being fair that it was a reasonable answer to a real problem. It shows the genuine advances over a registry (lazy creation, lifetimes, swapping for a test), then the failures: the compiler silent while a dependency is missing so that a customer is charged before the failure, every class coupled to the locator, and tests that need it configured. It shows where the pattern is still right, java.util.ServiceLoader and plug-in systems, and ends with a plain verdict.
""",
nongoals=[
    'Not a sneer. The project argues, and says the pattern was reasonable and is still right for plug-ins.',
    'Not a re-teaching of Registry or Dependency Injection. They are the neighbouring projects and are linked.',
    'Not a plug-in framework. One `ServiceLoader` demonstration is enough to show the legitimate case.',
],
problem="""
The registry left dependencies invisible and state shared. A locator that can find or create things adds lazy creation, lifetimes and test swapping, and still hides what each class needs.

**What this project must deliver:** the advances shown, the failures shown as evidence, the legitimate use shown with `ServiceLoader`, and a plain verdict.
""",
roles=[
    ('The shared collaborators', '`DiscountPolicy`, `PaymentGateway`, `Notifier`'),
    ('Pattern', '`ServiceLocator`, `LocatorCheckout`, `ReceiptPrinter`, `Auditor`'),
    ('The legitimate case', '`PaymentMethod`, `CardPayment`, `BankTransferPayment`, and `META-INF/services`'),
    ('Entry point', '`LocatorDemo`, six acts'),
],
requirements=[
    '**The compiler-silence failure is runnable.** `ServiceLocatorTest` builds a checkout with a missing notifier, charges the customer, and asserts the failure came after the charge.',
    '**The advances are real.** Lazy singleton, prototype, and a test swap are each asserted.',
    '**The legitimate case is real.** `ServiceLoader` finds two providers listed in `META-INF/services`.',
    '**The verdict is stated aloud.** Prefer the alternative for business logic.',
],
),

"dependency-injection": dict(
purpose="""
Close the Registry, Service Locator, Dependency Injection argument: a class declares what it needs in its constructor and is given it, so the signature is the dependency list, complete and checked by the compiler. The wiring is shown by hand first with its line count, the three forms are given a clear recommendation (constructor, setter for optional, field discouraged with the reason shown), and a container is written from scratch so it is demystified. It pays the costs: wiring that grows, start-up failures for a missing bean or a circular dependency, and the seven-collaborator constructor as a design smell.
""",
nongoals=[
    'Not a Spring tutorial. No framework appears in the build files, and the project says so.',
    'Not a survey of containers. Spring, Guice and Dagger are named and not built.',
    'Not a re-teaching of Registry or Service Locator. They are linked, and the progression is stated.',
],
problem="""
The same checkout, with the same three collaborators. Registry and Service Locator both leave the class asking, so nobody outside it knows what it needs.

**What this project must deliver:** constructor injection with the wiring done by hand and its line count stated, the three forms compared with a recommendation, a container written here, its start-up failures produced on purpose, and the three-part progression stated explicitly.
""",
roles=[
    ('The shared collaborators', '`DiscountPolicy`, `PaymentGateway`, `Notifier`'),
    ('The application', '`CheckoutService`, `ReceiptPrinter`, `Auditor`, `Storefront`'),
    ('Wiring by hand', '`Wiring`'),
    ('The three forms', '`CheckoutService`, `SetterInjectedCheckout`, `FieldInjectedCheckout`'),
    ('A container', '`MiniContainer`, `Injector`, `ContainerFailure`'),
    ('Entry point', '`WiringDemo`, six acts'),
],
requirements=[
    '**The wiring is by hand first, and its length is stated.** `DependencyInjectionTest` counts the lines between the markers.',
    '**A container is built here.** `MiniContainer` builds the same graph, and fails at start on a missing bean and on a cycle.',
    "**Field injection's cost is real.** A `new` object throws `NullPointerException` until reflection fills it.",
    '**The progression is stated explicitly.** In the explainer and aloud in the video.',
],
),

"dependency-injection-with-spring": dict(
purpose="""
Show what Spring's container replaces from the partner Dependency Injection project: the same classes with one @Component each, the wiring code gone, Spring's real start-up failures for a missing bean and a circular dependency, field injection's cost, and what the magic costs. It keeps the verdict unchanged: constructor injection, by hand until the wiring hurts, then a container.
""",
nongoals=[
    'Not a re-teaching of Dependency Injection. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a Spring tutorial. `@Component` and `@Autowired` are introduced as they appear.',
    'Not a web project. There is no controller and no web starter.',
],
problem="""
Dependency Injection wired the application by hand and wrote a container. Spring's container does the same, from annotations.

**What this project must deliver:** the same graph built by Spring, what each annotation replaced, Spring's real missing-bean and circular-dependency failures, field injection's cost, and a `docs/dependencies.md`.
""",
roles=[
    ('Reused from the partner', 'The collaborators and application classes, with `@Component` added and constructors untouched'),
    ('Framework setup', '`SpringDiApplication`, a Spring Boot application'),
    ('The failures', '`Chicken`, `Egg`, `FieldInjectedCheckout`'),
    ('Entry point', '`SpringDiApplication`, six acts'),
],
requirements=[
    "**The partner's constructors are untouched.** `SpringDiTest` asserts the constructor's parameter types.",
    '**Spring builds the same graph.** The same charge and three messages as the hand wiring.',
    "**The failures are Spring's own.** `UnsatisfiedDependencyException` and `BeanCurrentlyInCreationException`.",
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"registry-with-spring": dict(
purpose="""
Show Spring's ApplicationContext as a registry: it fixes the hand-built registry's declared-registration and start-up-checking problems, and the best use is never to call it. It shows getBean inside a business class as a service locator, and the failure that is Spring's own: the test context cache leaking singleton state between tests, proven with real Spring tests, plus an untyped Environment lookup that is silently null and by-type ambiguity at run time.
""",
nongoals=[
    'Not a re-teaching of Registry. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a Spring tutorial. `@Component`, `getBean` and `@DirtiesContext` are introduced as they appear.',
    'Not a web project. There is no controller and no web starter.',
],
problem="""
Registry built a static registry and listed its costs. Spring's context is a registry with those costs mostly fixed, and one of its own.

**What this project must deliver:** the context shown as the registry, injected versus asked, the cache leak proven with real Spring tests and fixed with `@DirtiesContext`, the property-typo and ambiguity failures, and a `docs/dependencies.md`.
""",
roles=[
    ('Reused from the partner', 'The three collaborators, with `@Component` added'),
    ('Framework setup', '`RegistrySpringApplication`, a Spring Boot application'),
    ('Used well and badly', '`InjectedCheckout`, `LocatorStyleCheckout`'),
    ('The failures', '`SharedContextLeakTest`, `Settings`, `SmsNotifier`'),
    ('Entry point', '`RegistrySpringApplication`, six acts'),
],
requirements=[
    '**The cache leak is proven with real Spring.** `SharedContextLeakTest` has a second test that passes only after the first.',
    '**The fix is proven.** `DirtiesContextFixTest` sees a clean gateway after `@DirtiesContext`.',
    "**Each test class has its own context.** So the project's own tests do not depend on class order.",
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"object-pool-with-hikaricp": dict(
purpose="""
Show HikariCP as the mature answer to the hand-built Object Pool's costs over real JDBC connections: it opens what demand needs, resets the JDBC state it knows about on return, and has a configurable timeout with a readable exhaustion message. It also shows what a library cannot fix: state inside the database session is invisible to the pool and leaks to the next borrower, and sizing is still a guess. It states the verdict: use a library, never write your own.
""",
nongoals=[
    'Not a re-teaching of Object Pool. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a HikariCP tuning guide. A few settings are introduced as they appear.',
    'Not Spring. HikariCP is used directly; Spring Boot supplies only version numbers.',
],
problem="""
Object Pool built a pool by hand and found four costs. HikariCP is the mature answer to several.

**What this project must deliver:** the pool shown opening what demand needs, the reset on return, the session-variable leak it cannot fix, exhaustion with a readable timeout, sizing, and a `docs/dependencies.md`. No test asserts a timing.
""",
roles=[
    ('Framework setup', '`Payments`, a payments table over in-memory H2 behind HikariCP'),
    ('Entry point', '`HikariDemo`, six acts'),
],
requirements=[
    '**No test asserts a timing.** `HikariPoolTest` asserts counts, states and exception messages.',
    '**The reset is real.** autoCommit and readOnly return to their defaults for the next borrower.',
    '**The remaining leak is real.** A session variable set by one borrower is read by the next.',
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"service-locator-with-consul": dict(
purpose="""
Show Service Locator as real service discovery, against a real Consul agent and real HTTP service instances: the locator asks for a service by name and is answered with what is healthy, and instances come and go without the caller's code changing. It shows the partner project's costs returning over a network (string names, a silent compiler, a charge that goes through before the failure), a new cost (a cached answer going stale), and the alternative: server-side discovery, with nginx in a Docker container, where the caller is given one address and never asks.
""",
nongoals=[
    'Not a re-teaching of Service Locator. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a Consul tutorial. Registration, TTL checks and a health query are shown, and nothing else.',
    'Not a service-mesh or Kubernetes project. Their DNS and proxies are named as the given form.',
],
problem="""
Service Locator argued against the pattern and said it is still right where what is available is a run-time fact. Service discovery is that case over a network.

**What this project must deliver:** a real Consul agent and real instances, the advance shown, the old costs shown, a stale cache, nginx in Docker as the alternative, and a `docs/dependencies.md` saying what to install and that skipping loses nothing.
""",
roles=[
    ('Real infrastructure', '`ConsulAgent`, `ServiceInstance`, `NginxFront`'),
    ("Consul's API", '`ConsulClient`, `Address`'),
    ('Pattern', '`Locator`, `ConsulLocator`, `CachingLocator`, `Discovery`, `LocatorCheckout`'),
    ('Entry point', '`ConsulDemo`, six acts'),
],
requirements=[
    '**Nothing is simulated.** The tests run a real Consul agent and real HTTP servers, and a real nginx container when Docker is available.',
    '**Tests skip, not fail, without the infrastructure.** `consul` on the PATH, and Docker with the nginx image.',
    '**The stale cache is real.** A cached address is still returned after the instance stopped, and the call fails.',
    '**Nothing is left running.** The agent is stopped and the container removed when a run ends.',
],
),

"sidecar-on-kubernetes": dict(
purpose="""
Show what changes when Kubernetes runs a service and its sidecar: a Pod shares a network namespace by definition rather than by a configuration line that can be forgotten, is scheduled and deleted as one unit, and receives its sidecar by injection into a manifest that never mentions it. It corrects a common claim: a crashing container does not take its neighbour with it, because the kubelet restarts each container alone. It is honest that a cluster is a large cost, and answers whether a small shop needs one yet.
""",
nongoals=[
    'Not a re-teaching of Sidecar. The first project owns the pattern; this one names it in its first paragraph.',
    'Not a Kubernetes tutorial. The model has a Pod, a Cluster and a kubelet loop, and nothing else.',
    'Not a service mesh. A mutating admission webhook is named and not built.',
],
problem="""
The same checkout and proxy as the first Sidecar project, now run by Kubernetes instead of Docker Compose.

**What this project must deliver:** a shared network by definition, one lifecycle, per-container restarts stated correctly, injection, `READY 2/2` and the start-up race, an honest answer to whether a small shop needs a cluster, and a `docs/dependencies.md` that explains Kubernetes first.
""",
roles=[
    ('A manifest', '`PodSpec`, `ContainerSpec`'),
    ('A control plane in a model', '`Cluster`, `Pod`, `Container`, `NetworkNamespace`'),
    ('The comparison', '`Compose`'),
    ('Injection', '`Injector`'),
    ('Entry point', '`PodDemo`, six acts'),
],
requirements=[
    "**A crash does not take a neighbour with it.** `PodTest` asserts the checkout is untouched and only the proxy's restart count rises.",
    '**Sharing by definition is proven.** The Compose model loses the line and the Pod cannot.',
    '**Injection leaves the authored manifest unchanged.** And injecting twice adds nothing.',
    '**Kubernetes is explained first.** `docs/dependencies.md` says what it is, what it costs, and that skipping loses nothing.',
],
),

"strangler-fig": dict(
purpose="""
Teach the Strangler Fig pattern by replacing a checkout without a cutover weekend: a router with a switch per capability, shadow reads that compare old and new on real-shaped orders before anything moves, and a rollback of one capability rather than the whole system. It pays the bill honestly: two systems live at once, two versions of the truth, and the failure that actually happens, a migration that stalls half-finished, shown with a stated cost model where two checkouts forever costs more than either endpoint.
""",
nongoals=[
    'Not a data-migration tool. Two maps are compared; moving rows is named and not built.',
    'Not an API gateway tutorial. The router is a Java class, and gateways are named as where it lives.',
    'Not a measurement of migration cost. The figures are a stated model that shows a shape.',
],
problem="""
The legacy checkout is one large class that must keep taking orders while it is replaced. A big-bang rewrite has one switch and an all-or-nothing rollback.

**What this project must deliver:** a router with a switch per capability, shadow reads that find differences before customers do, a one-capability rollback, the two-systems bill, and the stalled migration named as the likely outcome.
""",
roles=[
    ('The legacy system', '`LegacyCheckout`, one class that does four things'),
    ('The rewrite', '`NewPricing`, `NewStock`, `NewPayment`, `NewMailer`'),
    ('The pattern', '`Router`, `Route`'),
    ('The naive version and the failure', '`BigBang`, `StallModel`'),
    ('Entry point', '`MigrationDemo`, six acts'),
],
requirements=[
    '**Shadow reads catch real differences.** `StranglerFigTest` finds the VAT rounding and the exactly-fifty-pounds delivery difference on a fixed-seed stream.',
    '**Rollback is per capability.** One switch flips and pricing stays moved.',
    '**The stall is named and modelled.** The cost figures are labelled as assumptions.',
    '**The verdict is stated aloud.** Finish it, or do not start.',
],
),

"thread-pool-with-spring": dict(
purpose="""
Show what Spring Boot's @Async gives you: a real thread pool the container owns, whose default is eight core threads and an unbounded queue, the partner project's trap as a default. It shows the queue growing to a thousand with no refusal, a bounded pool refusing with a real TaskRejectedException, an annotation silently skipped by a call on this, and a pool that starves itself, ending with a verdict to configure the pool explicitly.
""",
nongoals=[
    'Not a re-teaching of Thread Pool. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a Spring Boot tutorial. Only what the pattern needs is introduced, as it appears.',
],
problem="""
The Thread Pool project built a bounded pool by hand. `@Async` gives the same thing as one annotation whose defaults are the trap.

**What this project must deliver:** the default executor's numbers, the unbounded backlog, a bounded pool's real refusal, the `this` call that skips the proxy, pool starvation, and a `docs/dependencies.md`.
""",
roles=[
    ('Framework setup', '`PackingApplication`, a Spring Boot application with `@EnableAsync`'),
    ('The service', '`PackingService`, with `@Async` methods'),
    ('Reused from the partner', "`Gate`, and the six acts' scenario"),
    ('Entry point', '`PackingApplication`, six acts'),
],
requirements=[
    '**The defaults are asserted.** `AsyncPoolTest` reads core 8, max and queue `Integer.MAX_VALUE`.',
    '**The backlog is counted.** A thousand orders wait behind eight stuck workers, none refused.',
    '**Every wait is a latch or a gate.** No test sleeps.',
    "**The failures are real.** `TaskRejectedException`, a `this` call on the caller's thread, and starvation.",
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"future-promise-with-spring": dict(
purpose="""
Show what @Async does and does not do for a CompletableFuture: it runs the lookups on the container's pool and completes the future, but the pool, not the annotation, decides how concurrent they are; a void method's exception is lost unless a handler is registered; a thread-local does not cross the thread boundary unless a TaskDecorator copies it; and neither orTimeout nor cancel(true) stops a running task. It ends with a verdict: return a future, never void.
""",
nongoals=[
    'Not a re-teaching of Future/Promise. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a Spring Boot tutorial. Only what the pattern needs is introduced, as it appears.',
],
problem="""
Future/Promise built the handoff by hand. `@Async` gives it as one annotation, and loses four things a caller assumes it keeps.

**What this project must deliver:** concurrency shown as a pool decision, an exception carried by a future and lost by a void method, a thread-local lost and restored, a timeout and a cancel that leave the work running, and composition with a fallback.
""",
roles=[
    ('Framework setup', '`ProductPageApplication`, a Spring Boot application'),
    ('The lookups', '`CatalogueLookups`, with `@Async` methods'),
    ('The failures', '`Flight`, `CustomerContext`, `UncaughtHandler`, `AsyncSettings`'),
    ('Entry point', '`ProductPageApplication`, six acts'),
],
requirements=[
    '**Concurrency is counted, not inferred.** `AsyncFutureTest` gates three lookups and reads the peak in flight: 3, and 1 on a pool of one.',
    '**Every wait is a latch, a gate or a bounded spin.** No test sleeps.',
    '**The losses are proven.** A void exception, a null thread-local, a timeout and a cancel that leave the task running.',
    '**The fixes are proven.** A registered handler, a `TaskDecorator`, and a fallback at the failing step.',
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"active-object-with-spring": dict(
purpose="""
Show an active object built from an @Async bean on a one-thread executor: the executor's queue is the mailbox, the future is the reply, and the state is a plain field with no lock. It shows the mailbox backing up and being bounded with a real TaskRejectedException, then the failures that are Spring's own: a call on this that skips the proxy and loses an update on a forced interleaving, and a direct read that sees the past. It ends with a throughput ceiling and a verdict.
""",
nongoals=[
    'Not a re-teaching of Active Object. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a Spring Boot tutorial. Only what the pattern needs is introduced, as it appears.',
],
problem="""
Active Object built the mailbox by hand. An `@Async` bean on a one-thread executor gives the same thing, and its guarantee holds only for calls that go through the proxy.

**What this project must deliver:** a lock-free plain field made safe by one thread, a counted and bounded mailbox, a lost update from a call on `this`, a stale direct read against a message read, errors from the worker, and a throughput ceiling.
""",
roles=[
    ('Framework setup', '`InventoryApplication`, `InventoryConfig`'),
    ('The active object', '`InventoryService`, a plain `int` and `@Async` methods'),
    ('Reused from the partner', '`Gate`, and the scenario'),
    ('Entry point', '`InventoryApplication`, six acts'),
],
requirements=[
    '**No lock is credited.** `ActiveObjectBeanTest` restocks a plain field from four threads and loses nothing.',
    '**The lost update is forced.** A gate holds the worker mid-change while a call on `this` changes the field.',
    '**The stale read is forced.** A gate holds the worker, and a direct read says 0 while a message read says 5.',
    '**Only the throughput ratio depends on timing,** and its bound is generous.',
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"singleton-with-spring": dict(
purpose="""
Show the order-number sequencer as a Spring bean shared by three callers, then the ways the guarantee weakens: a public constructor that anyone can call, a second container, a changed scope, when the bean is built, and a counter that is shared by threads but not safe.
""",
nongoals=[
    'Not a re-teaching of Singleton. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a Spring Boot tutorial. Only what the pattern needs is introduced, as it appears.',
],
problem="""
Singleton guaranteed one instance with the language. Spring guarantees one per container, which is weaker in some ways and easier in others.

**What this project must deliver:** one bean shared by three callers, a plain new that forges another, two containers issuing the same number, a scope change that flips the answer, eager against lazy construction, and a forced duplicate on a plain long.
""",
roles=[
    ('Framework setup', '`ShopApplication`'),
    ('The bean', '`OrderSequenceGenerator`, public constructor and an `AtomicLong`'),
    ('The callers', '`Checkout`, `AdminConsole`, `RetryJob`'),
    ('Unsafe contrast', '`UnsafeOrderSequence`'),
],
requirements=[
    '**Sharing is asserted by identity,** not by matching numbers.',
    '**The duplicate is forced** with a gate between read and write.',
    '**Construction is counted** with a static counter, never timed.',
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"prototype-with-spring": dict(
purpose="""
Show the product listing as a prototype-scoped Spring bean, and the three ways the scope surprises people who know the pattern: it builds from the definition and not from an edited draft, it is built only once when injected into a singleton, and Spring never destroys it.
""",
nongoals=[
    'Not a re-teaching of Prototype. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a Spring Boot tutorial. Only what the pattern needs is introduced, as it appears.',
],
problem="""
Prototype copied a finished object. Spring's prototype scope builds a new one from the definition, which is a different thing.

**What this project must deliver:** a fresh bean per request, independence between them, the difference between asking the container and calling copy, a prototype trapped in a singleton, an ObjectProvider that fixes it, and the missing destroy call.
""",
roles=[
    ('Framework setup', '`ListingApplication`'),
    ('The prototype', '`Listing`, prototype scope, with `copy()`'),
    ('The singleton', '`Storefront`, injected once and through a provider'),
],
requirements=[
    '**Identity is asserted with assertSame/assertNotSame.**',
    '**Destruction is counted,** never timed.',
    '**Nothing depends on timing.**',
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"proxy-with-spring": dict(
purpose="""
Show the protection proxy and the lazy proxy as Spring produces them: a generated subclass, one aspect that protects three beans, and a lazy injection that loads the image on first use. It then shows the two ways a call slips past a generated proxy: a call on this, and a final method.
""",
nongoals=[
    'Not a re-teaching of Proxy. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a Spring Boot tutorial. Only what the pattern needs is introduced, as it appears.',
],
problem="""
Proxy was written by hand. Spring generates it, and the generation has rules that surprise people.

**What this project must deliver:** a generated proxy, one aspect on three beans, lazy loading by count, a call on this that skips the rule, and a final method that skips it and sees no fields.
""",
roles=[
    ('Framework setup', '`ImageApplication`'),
    ('The aspect', '`RoleAspect`, `RequiresRole`'),
    ('The beans', '`ImageCatalogue`, `OrderExport`, `RefundDesk`'),
    ('The costly subject', '`HighResolutionImage`, `@Lazy`, counted'),
],
requirements=[
    '**Loads are counted,** never timed.',
    '**The refusal is asserted** with `assertThrows` on the proxy.',
    '**The skipped checks are asserted,** so a Spring change that fixes them fails the test.',
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"observer-with-spring": dict(
purpose="""
Show the order status announcement as Spring events: a publisher that holds no listeners, ordered listeners on the caller's thread, a failing listener that stops the rest and reaches the caller, an asynchronous listener held at a gate, a condition that filters events, and an event nobody hears.
""",
nongoals=[
    'Not a re-teaching of Observer. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a Spring Boot tutorial. Only what the pattern needs is introduced, as it appears.',
],
problem="""
Observer was hand-built. Spring provides it, with synchronous delivery and no registry the publisher can see.

**What this project must deliver:** a publisher-only subject, ordered listeners, a failure that stops the others, an async listener proved by a gate, a filter condition, and a silent drop.
""",
roles=[
    ('Framework setup', '`OrderEventsApplication`'),
    ('The subject', '`OrderService`'),
    ('Events', '`OrderStatusChanged`, `OrderRefunded`'),
    ('Observers', '`InventoryListener`, `EmailListener`, `AnalyticsListener`, `ShippedOnlyListener`, `AuditListener`'),
],
requirements=[
    '**Order is asserted** with `@Order` and a journal.',
    '**The other thread is held at a gate,** never slept on.',
    '**A missing listener is asserted** as a silent no-op.',
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"strategy-with-spring": dict(
purpose="""
Show the four delivery rules as Spring beans collected into a map, chosen by a configured name that is checked at startup, extended by a fifth rule without touching the checkout, and the failure that comes from asking for the interface alone, fixed with a primary bean.
""",
nongoals=[
    'Not a re-teaching of Strategy. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a Spring Boot tutorial. Only what the pattern needs is introduced, as it appears.',
],
problem="""
Strategy chose a rule from a hand-written table. Spring builds the table from the beans.

**What this project must deliver:** a map of rules keyed by bean name, the same prices as the partner, a startup check on the configured name, an ambiguous injection that fails, a fifth rule added without a change to the checkout, and a primary bean.
""",
roles=[
    ('Framework setup', '`ShippingApplication`'),
    ('The strategies', '`FlatRateRule`, `WeightBandedRule`, `DistanceBasedRule`, `FreeOverThresholdRule`'),
    ('The context', '`CheckoutService`, `SelectedShipping`'),
    ('Demo-only', '`ExpressRule`, `NeedsOneRule`, registered by the demo'),
],
requirements=[
    '**Prices are asserted in pence.**',
    "**Startup failures are asserted** by the exception's root cause.",
    '**The fifth rule and the ambiguous class are registered by the demo,** so the default run has four rules.',
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"template-method-with-spring": dict(
purpose="""
Show Template Method in Spring's own library: JdbcTemplate owning the fixed steps of a query, against a plain JDBC version that leaks a connection on the error path, with translated exceptions, the decisions the template makes for you, and a transaction template that rolls back a half-finished checkout.
""",
nongoals=[
    'Not a re-teaching of Template Method. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a Spring Boot tutorial. Only what the pattern needs is introduced, as it appears.',
],
problem="""
Template Method was built by inheritance around fulfilment steps. Spring's templates do the same with callbacks, around database calls.

**What this project must deliver:** a plain JDBC method that leaks on the error path, the same query through JdbcTemplate that does not, a row mapper, translated exceptions, a missing-row error, and a rollback.
""",
roles=[
    ('Framework setup', '`FulfilmentApplication`, `schema.sql`'),
    ('The repository', '`OrderRepository`, by hand and by template'),
    ('The transaction', '`Checkout`, `TransactionTemplate`'),
],
requirements=[
    "**Connections are counted** through Hikari's pool MXBean.",
    '**The leak is asserted** so a fix to the by-hand method fails the test.',
    '**Rollback is asserted** by counting rows and stock.',
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"chain-of-responsibility-with-spring": dict(
purpose="""
Show the screening chain built by Spring from ordered beans, the cost of its order counted in paid calls, a link that throws turned into a referral, a link removed by a property, and a fallback that is a named setting.
""",
nongoals=[
    'Not a re-teaching of Chain of Responsibility. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a Spring Boot tutorial. Only what the pattern needs is introduced, as it appears.',
],
problem="""
Chain of Responsibility linked successors by hand. Spring injects the links as an ordered list.

**What this project must deliver:** a chain built from beans, the never-run links reported, the cost of order counted, a throwing link handled, a property that removes a link, and a named fallback.
""",
roles=[
    ('Framework setup', '`ScreeningApplication`'),
    ('The links', '`AddressCheck`, `StockCheck`, `FraudScoreCheck`, `PaymentLimitCheck`'),
    ('The walker', '`ScreeningChain`'),
],
requirements=[
    '**Order is asserted** as a list of names.',
    '**Cost is counted** as paid calls, never timed.',
    '**A throwing link is asserted** as a referral.',
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"interpreter-with-spel": dict(
purpose="""
Show the promotion rules run by Spring's expression language in place of a hand-written parser and rule classes: text rules parsed once, the language features that came free, a syntax error caught at build time and a misspelled name caught late, a rule that reaches the whole program in the full context and is refused in the read-only one, and missing values.
""",
nongoals=[
    'Not a re-teaching of Interpreter. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a Spring Expression Language tutorial. Only what the pattern needs is introduced, as it appears.',
],
problem="""
Interpreter built the parser and the rule tree by hand. SpEL is a ready-made interpreter with a bigger language than the shop needs.

**What this project must deliver:** the partner's rules as text, free language features, a build-time and a run-time error, the two evaluation contexts, safe navigation, and a parse-once run.
""",
roles=[
    ('Entry point', '`SpelPromotionsApplication`'),
    ("The interpreter's user", '`PromotionBook`, parse once, evaluate many'),
    ('The context', '`Order`, with getters'),
],
requirements=[
    '**Rules are asserted against three known orders.**',
    '**Both failure times are asserted** with the exact exception type.',
    '**The read-only context is asserted to refuse** static calls and method calls.',
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"circuit-breaker-with-resilience4j": dict(
purpose="""
Show the circuit breaker from the hand-built project as a Resilience4j annotation with settings in application.properties: a healthy call, a service that goes down and opens the breaker after four calls, fast failure with no calls reaching the service, a half-open probe that fails and one that succeeds, the ignore list for client errors, and a call on this that bypasses the breaker.
""",
nongoals=[
    'Not a re-teaching of Circuit Breaker. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a Resilience4j tutorial. Only what the pattern needs is introduced, as it appears.',
],
problem="""
Circuit Breaker was built by hand with a simulated clock. Resilience4j provides it as an annotation, and its own failure modes are proxy bypass, hidden failures and miscounted exceptions.

**What this project must deliver:** a breaker driven by settings, a fallback that keeps the page up, an open breaker that protects the backend, a half-open probe, an ignore list, and a bypass by a call on this.
""",
roles=[
    ('Framework setup', '`RecommendationsApplication`, `application.properties`'),
    ('The protected call', '`RecommendationsClient`'),
    ('The remote service', '`RecommendationsBackend`, in memory and counted'),
],
requirements=[
    '**Calls that reach the backend are counted,** never timed.',
    '**The half-open probe is started by the test,** not by a wait duration.',
    '**The bypass is asserted,** so a fix fails the test.',
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"retry-with-resilience4j": dict(
purpose="""
Show the retry with backoff from the hand-built project as a Resilience4j annotation with settings in application.properties: a flaky gateway retried until it answers, the doubling waits, giving up after three attempts, a declined card that must not be retried, a lost answer that charges twice without an idempotency key, and two layers of retries that multiply.
""",
nongoals=[
    'Not a re-teaching of Retry with Backoff. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a Resilience4j tutorial. Only what the pattern needs is introduced, as it appears.',
],
problem="""
Retry with Backoff was built by hand. Resilience4j provides it as an annotation, and its own failure modes are a wide exception list, a repeated charge, and stacked layers.

**What this project must deliver:** a retry driven by settings, recorded waits, a give-up, an exception list, an idempotency key, and multiplication across layers.
""",
roles=[
    ('Framework setup', '`PaymentsApplication`, `application.properties`'),
    ('The retried calls', '`PaymentsClient`, `CheckoutService`'),
    ('The remote gateway', '`PaymentGateway`, in memory and counted'),
],
requirements=[
    '**Calls and charges are counted,** never timed.',
    '**Waits are the values Resilience4j chose,** read from its events.',
    '**The double charge is asserted,** and so is its fix.',
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"bulkhead-with-resilience4j": dict(
purpose="""
Show the bulkhead from the hand-built project as Resilience4j annotations: one shared compartment that lets slow feed jobs starve checkout, a compartment each that keeps checkout selling, a fallback for a full compartment, the wasted capacity behind the wall, a call on this that bypasses the limit, and the thread-pool kind that never blocks its caller.
""",
nongoals=[
    'Not a re-teaching of Bulkhead. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a Resilience4j tutorial. Only what the pattern needs is introduced, as it appears.',
],
problem="""
Bulkhead was built by hand with pools. Resilience4j provides two kinds as annotations, and their own costs are the wall, the bypass, and the choice of kind.

**What this project must deliver:** a starved checkout, a protected checkout, a fallback, the free-permit cost, a bypass, and a thread-pool compartment.
""",
roles=[
    ('Framework setup', '`SupplierApplication`, `application.properties`'),
    ('The compartments', '`SupplierService`'),
    ('The slow partner', '`Gate`, holds calls in flight'),
],
requirements=[
    '**Slow calls are held at a gate,** never slept.',
    '**Permits are read from the registry.**',
    '**The bypass is asserted,** so a fix fails the test.',
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"api-gateway-with-spring-cloud-gateway": dict(
purpose="""
Show a real Spring Cloud Gateway in front of four real HTTP services: one address, prefixes stripped and a header added, one token check for every route, a dead service failing only its own route, a page that still needs three calls because a gateway does not compose, and a slow service answered for with a 504.
""",
nongoals=[
    'Not a re-teaching of API Gateway. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a Spring Cloud Gateway tutorial. Only what the pattern needs is introduced, as it appears.',
],
problem="""
API Gateway was built as a class that called four services and merged the answers. Spring Cloud Gateway is a real router with filters, and it does not merge.

**What this project must deliver:** real routing over HTTP, stripped prefixes, one token filter, isolation of a dead route, the honest limit of a gateway, and a timeout.
""",
roles=[
    ('Framework setup', '`GatewayApplication`, `application.properties`'),
    ('The routing table', '`GatewayRoutes`'),
    ('The shared filter', '`TokenCheck`'),
    ('Stand-in services', '`Backend`, JDK HTTP servers'),
],
requirements=[
    '**All traffic is real HTTP** over local sockets.',
    '**A rejected request is asserted** to have reached no service.',
    '**The slow service is held at a gate,** and only the 504 is asserted.',
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"load-balancing-with-spring-cloud-loadbalancer": dict(
purpose="""
Show a real Spring Cloud LoadBalancer choosing among three real HTTP copies of the catalogue: round robin spreading twelve requests evenly, the slow copy doing most of the work, a least-work strategy plugged in for one service name, a stopped copy still receiving a third of the requests, a retry landing elsewhere, and a real address refused by a balanced client.
""",
nongoals=[
    'Not a re-teaching of Client-Side Load Balancing. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a Spring Cloud LoadBalancer tutorial. Only what the pattern needs is introduced, as it appears.',
],
problem="""
Client-Side Load Balancing wrote four strategies by hand. Spring Cloud LoadBalancer supplies round robin and lets you replace it.

**What this project must deliver:** an even spread, uneven work, a custom strategy for one name, a stopped copy, a retry, and the names-only rule.
""",
roles=[
    ('Framework setup', '`CatalogueApplication`'),
    ('The client', '`CatalogueClient`'),
    ('The custom strategy', '`LeastWorkBalancer`, `LeastWorkConfiguration`'),
    ('The copies', '`Backend`'),
],
requirements=[
    '**Work is counted as cost units,** never timed.',
    "**Round robin's random start is respected:** nothing asserts which copy is first.",
    '**Every demo line is the same on every run.**',
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"layered-architecture-with-spring-boot": dict(
purpose="""
Show placing an order through four layers in a real Spring Boot application over real HTTP: a service transaction that rolls back a reservation, failures mapped to statuses in one place, a shortcut controller that Spring accepts and that leaks the cost price, and an ArchUnit rule that finds it.
""",
nongoals=[
    'Not a re-teaching of Layered Architecture. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a Spring Boot tutorial. Only what the pattern needs is introduced, as it appears.',
],
problem="""
Layered Architecture was built with plain classes. Spring Boot supplies the layers' machinery and does not enforce the rule between them.

**What this project must deliver:** a real request through four layers, a rollback, one status mapping, a shortcut that runs and leaks, and a rule that catches it.
""",
roles=[
    ('Framework setup', '`ShopApplication`, `schema.sql`'),
    ('The layers', '`presentation`, `application`, `domain`, `infrastructure`'),
    ('The rule', '`LayerRules`'),
    ('The shortcut', '`naive.ShortcutController`'),
],
requirements=[
    '**All traffic is real HTTP.**',
    '**The rollback is asserted** by reading the stock.',
    '**The rule is asserted to fail only on the shortcut.**',
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"mvc-with-spring-mvc": dict(
purpose="""
Show an order summary served by Spring MVC over real HTTP as an HTML page and as JSON from one model, the total computed once per request and testable without a server, a template that does its own sums and disagrees with the model then breaks on a one-line order, and the post, redirect, get pattern.
""",
nongoals=[
    'Not a re-teaching of MVC. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a Spring MVC tutorial. Only what the pattern needs is introduced, as it appears.',
],
problem="""
MVC was built with hand-written views. Spring MVC renders templates and JSON for you, and its main risk is logic creeping into the template.

**What this project must deliver:** an HTML view, a JSON view from one model, a single computation per request, a template that diverges, and a redirect after a post.
""",
roles=[
    ('Framework setup', '`SummaryApplication`'),
    ('The controller', '`SummaryController`'),
    ('The model', '`OrderSummary`'),
    ('The views', '`summary.html`, `naive-summary.html`'),
],
requirements=[
    '**All traffic is real HTTP,** and redirects are not followed so they can be seen.',
    '**The model is tested without a server.**',
    '**The divergent template is asserted,** so a fix fails the test.',
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"hexagonal-architecture-with-spring-boot": dict(
purpose="""
Show the hexagonal order use case in Spring Boot: a core of plain Java handed its adapters by one configuration class, two storage adapters chosen by a property with the same answer, two driving adapters on one port, the core run ten thousand times with no container, an ArchUnit rule that finds a use case reaching for Spring, and a missing adapter found at startup.
""",
nongoals=[
    'Not a re-teaching of Hexagonal Architecture. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a Spring Boot tutorial. Only what the pattern needs is introduced, as it appears.',
],
problem="""
Hexagonal Architecture was wired by hand. Spring Boot chooses and wires the adapters, and can also undo the hexagon by letting the core reach for the framework.

**What this project must deliver:** a plain core, adapters chosen by property, two driving adapters, a container-free run, a rule, and a startup failure for a missing adapter.
""",
roles=[
    ('Framework setup', '`ShopApplication`, `ShopConfig`'),
    ('The core', '`PlaceOrderService`, the ports, `domain`'),
    ('The adapters', '`memory`, `jdbc`, `CardNetwork`, `ConsoleCheckout`, `CsvBatch`'),
    ('The rule', '`HexagonRules`'),
    ('The shortcut', '`naive.SpringyPlaceOrder`'),
],
requirements=[
    '**The core is asserted to be a plain class,** not a proxy.',
    '**The rule is asserted to fail only on the shortcut.**',
    '**Both storage adapters are asserted to give the same receipt.**',
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"service-discovery-with-spring-cloud-consul": dict(
purpose="""
Show service discovery with a real Consul agent and Spring Cloud Consul: three copies of Pricing registering themselves, requests found by service name, a deployment that breaks a hardcoded address but not a name, a graceful stop noticed at once, a crash that stays listed until its health check fails, and a registry that goes away.
""",
nongoals=[
    'Not a re-teaching of Service Registry and Discovery. The partner project owns the pattern; this one names it in its first paragraph.',
    'Not a Spring Cloud Consul tutorial. Only what the pattern needs is introduced, as it appears.',
],
problem="""
Service Registry and Discovery built the registry by hand. Spring Cloud Consul registers with a real one, and the real one has real delays.

**What this project must deliver:** self-registration, discovery by name, a moved copy, a graceful stop, a stale entry after a crash, and a client with no registry.
""",
roles=[
    ('The demo', '`DiscoveryApplication`, `Cluster`'),
    ('The registry', '`ConsulAgent`, the real consul program'),
    ('The service', '`instance.PricingInstance`'),
    ('The client', '`client.ClientApplication`, `PricingClient`'),
],
requirements=[
    '**Consul is real,** started on free ports and stopped afterwards.',
    '**Waits are bounded polls,** never fixed sleeps; only counts are asserted.',
    '**Tests are skipped when the `consul` program is missing.**',
    '**Dependencies are explained.** `docs/dependencies.md` says what to install, what it costs, and that skipping loses nothing.',
],
),

"value-object": dict(
purpose="""
Teach Value Object with money and an email address: a double that drifts and adds pounds to dollars, a value that refuses a mixed currency, equality by value against identity, a mutable price shared by two orders against an immutable one, a string email checked in two of three places against a type that cannot be built wrong, and a bill split that loses a penny against an allocation that does not.
""",
nongoals=[
    'Not a full money library. There is no exchange rate and no rounding mode.',
    'Not a tour of Java records. They are used, and their `equals` is relied on.',
    'Not concurrency. There is one thread, and immutability is shown through sharing.',
],
problem="""
Prices as doubles drift and add across currencies, and a shared mutable price changes silently.

**What this project must deliver:** a `Money` and an `EmailAddress` that are equal by value, never changed and impossible to build wrong, each bug of the plain version shown for real, allocation that loses no penny, and a plain verdict.
""",
roles=[
    ('Domain', '`Money`, `EmailAddress`, `CurrencyMismatch`'),
    ('Naive', '`NaivePricing`, `MutableMoney`, `IdentityMoney`, `BareEmailSignup`'),
    ('Entry point', '`ValueObjectDemo`, six acts'),
],
requirements=[
    '**The floating point error is real output.** `NaiveVersionTest` asserts it.',
    '**Allocation is exact for every amount from -50 to 200 pence into up to nine parts.**',
    '**Shares differ by at most one penny.**',
    '**The verdict is stated aloud.**',
],
),

"aggregate": dict(
purpose="""
Teach Aggregate with an order and its lines: a loose order that breaks every rule, a root that enforces six of them, lines that cannot be reached or built outside it, another aggregate held by id, whole-aggregate saves with a version check that refuses the second of two clerks, and an aggregate drawn too big that makes two clerks collide over different orders.
""",
nongoals=[
    'Not a persistence tutorial. The store is in memory, and versions are the whole story.',
    'Not a full domain model. There is no customer aggregate, only its id.',
    'Not concurrency. The two clerks are two sequential loads, and the conflict is deterministic.',
],
problem="""
An order's rules span its lines, and a public list lets any caller break them.

**What this project must deliver:** a root that enforces every rule, lines that cannot be built outside it, a reference by id, whole saves with a version check, the cost of an aggregate that is too big, and a plain verdict.
""",
roles=[
    ('Domain', '`Order`, `OrderLine`, `Money`, `OrderId`, `CustomerId`, `InvariantViolated`'),
    ('Infrastructure', '`VersionedStore`, `Loaded`, `ConcurrentModification`'),
    ('Naive', '`LooseOrder`, `EagerOrder`, `CustomerRecord`, `CustomerWithOrders`'),
    ('Entry point', '`AggregateDemo`, six acts'),
],
requirements=[
    '**Every rule is asserted,** including the merged-line and total limits.',
    '**The line list is read-only and lines have no public constructor.**',
    '**The second save of a stale load is refused.**',
    '**A boundary drawn too wide is shown to conflict,** and one per order is shown not to.',
],
),

"domain-event": dict(
purpose="""
Teach Domain Event with an order being placed: an order that calls stock, email and analytics and is left half done when the mail server fails, an order that records an OrderPlaced event and calls nobody, a repository that keeps the events with the order and a relay that delivers them, a failing handler that neither undoes the order nor stops the others and is retried alone, events as data-carrying records in order, and the gap between saving and telling closed by keeping the events with the order.
""",
nongoals=[
    'Not a message broker. Delivery is an in-process relay called by hand.',
    'Not exactly-once delivery. A handler must be safe to run twice, and the verdict says so.',
    'Not event sourcing. The order is stored as itself; the events are a record of what happened, not the store.',
],
problem="""
An order that calls the systems that care about it is left half done when one of them fails, and knows all of them.

**What this project must deliver:** an order that records events and calls nobody, a relay that delivers them after the save, a failing handler that is retried alone, events as facts, the crash gap closed by keeping events with the order, and a plain verdict.
""",
roles=[
    ('Domain', '`Order`, `DomainEvent`, `OrderPlaced`, `OrderCancelled`'),
    ('Infrastructure', '`OrderRepository` and its relay, `EventHandler`, `Handlers`, `Journal`'),
    ('Naive', '`NaivePlaceOrder`'),
    ('Entry point', '`DomainEventDemo`, six acts'),
],
requirements=[
    '**The half-done state is real:** the naive order is saved and stock reserved when email fails.',
    '**A failing handler does not stop the others and is retried alone,** and nothing is delivered twice.',
    '**Events keep the order they were raised in.**',
    '**A missed relay loses nothing.**',
],
),

"specification": dict(
purpose="""
Teach Specification with the idea of cheap and available: the same condition written three times that drifts, one rule named once and used by all three, rules combined with and, or and not, a rule that says which part a product fails, one rule used to select and to validate, and the bill that an in-memory specification looks at every product.
""",
nongoals=[
    'Not a query builder. Turning a specification into SQL is described, not built.',
    'Not the whole of domain-driven design. It is one pattern for one kind of rule.',
    'Not a comparison with every rule engine. It stays with small rules combined in code.',
],
problem="""
One business rule copied into three features drifts, so features disagree.

**What this project must deliver:** a `Specification` with and, or and not, one named rule used by three features, the drift of the plain version shown for real, self-description and explanation of a failure, one rule for selecting and validating, and the cost of filtering in memory.
""",
roles=[
    ('Domain', '`Specification`, `Products`, `Product`, `Catalogue`'),
    ('Naive', '`NaiveShop`, the same rule three times'),
    ('Entry point', '`SpecificationDemo`, six acts'),
],
requirements=[
    '**The drift is real:** the three naive copies return different lists.',
    "**And, or and not agree with their logic** for every product on the shelf, and De Morgan's law holds.",
    '**The explanation names only the failing parts.**',
    '**The in-memory cost is counted:** every product is examined.',
],
),

"anti-corruption-layer": dict(
purpose="""
Teach Anti-Corruption Layer with an old inventory system: four features that each learnt its one-letter codes, one adapter that translates them into the shop's own model, bad data refused with the sku named, a new status handled in one decision instead of four guesses, and the cost of the fields the layer drops.
""",
nongoals=[
    'Not a framework tutorial. It is plain Java.',
    'Not a survey of every variant. It shows one honest version and its bill.',
],
problem="""
A legacy system's codes spread through the shop, and its changes break features silently.

**What this project must deliver:** a shop model in its own words, one adapter that alone knows the old codes, refusal of bad data, a new status decided in one place, the dropped fields listed, and a plain verdict.
""",
roles=[
    ("The shop's model", '`StockLevel`, `Availability`, `InventoryGateway`'),
    ('The layer', '`LegacyInventoryAdapter`, `UntranslatableLegacyData`'),
    ('The system we do not own', '`LegacyStockRecord`, `LegacyInventorySystem`'),
    ('Naive', '`NaiveShop`'),
    ('Entry point', '`AclDemo`, six acts'),
],
requirements=[
    '**Only the adapter imports the legacy package.** A test scans the source.',
    '**Bad data is refused with the sku named.**',
    "**A new status is one decision.** The shortcut's four guesses are asserted.",
    '**The dropped fields are listed.**',
],
),

"bounded-context": dict(
purpose="""
Teach Bounded Context with the word customer: a company-wide class of twelve fields that every department depends on, the same customer being active in Sales and Shipping and not in Support, three small models that share only an id, a rename crossing contexts as an event that Shipping translates for itself, a boundary checked by scanning imports, and the bill of duplicated data and eventual consistency.
""",
nongoals=[
    'Not a full context map with every relationship type. It shows events and shared ids.',
    'Not microservices. The three contexts are packages in one program.',
    'Not a data consistency tutorial. The event bus is delivered by hand, so the gap can be seen.',
],
problem="""
One word means three things across departments, and a single class forces all of them to depend on each other.

**What this project must deliver:** three models with three correct answers to one question, a shared id and events, a boundary a test checks, the lag between contexts shown, and a plain verdict.
""",
roles=[
    ('Contexts', '`sales`, `shipping`, `support`'),
    ('Shared', '`CustomerId`, `CustomerRenamed`, `EventBus`'),
    ('Naive', '`GodCustomer`'),
    ('Entry point', '`BoundedContextDemo`, six acts'),
],
requirements=[
    '**Three correct answers to one question** are asserted, including the ninety-day boundary.',
    "**No context imports another's types.** A test scans the source.",
    '**A rename reaches Shipping only when delivered.**',
    '**An event for an unknown customer is ignored.**',
],
),

"transaction-script": dict(
purpose="""
Teach Transaction Script with placing an order: the whole action as one procedure, one transaction that undoes the stock change when the card is declined, a second script that copied the pricing and drifted, a shared helper, the growth of a script from three decisions to seven and from eight paths to a hundred and twenty eight, and a month-end job where a script is exactly right.
""",
nongoals=[
    'Not an argument against scripts. The verdict names where they are best.',
    'Not a real database. Db is a small in-memory store with a rollback.',
    'Not the domain model. It is named as the next step, not built.',
],
problem="""
The simplest way to write business logic works until the same rules appear in several scripts, and one script's decisions outgrow its tests.

**What this project must deliver:** a script that does the whole action, a transaction that rolls back, drift between copies, a shared helper, growth shown by counting decisions in the real source, a case where a script is right, and a plain verdict.
""",
roles=[
    ('Scripts', '`PlaceOrderScript`, `AmendOrderScript`, `PlaceOrderScriptGrown`, `MonthEndScript`'),
    ('Shared', '`Pricing`, `Payment`'),
    ('Storage', '`Db`'),
    ('Entry point', '`TransactionScriptDemo`, six acts'),
],
requirements=[
    '**The rollback is asserted:** stock and orders return to what they were.',
    '**The drift is asserted:** 50.40 against 56.00.',
    '**Decisions are counted from the real source:** 3 and 7.',
    "**The grown script's rules all apply.**",
],
),

"active-record": dict(
purpose="""
Teach Active Record with orders: a record that finds and saves itself in three lines, finders on the class, rules on the record, and three bills shown for real: a delivery rule that needs the table to be tested while the same rule on two numbers needs nothing, a renamed column that breaks loading, and five orders that cause five hidden table operations.
""",
nongoals=[
    'Not a comparison with every ORM. Data Mapper is named as the alternative.',
    'Not real SQL. The table is an in-memory store that counts every operation.',
    'Not an argument against the pattern. The verdict names where it is right.',
],
problem="""
Letting an object save itself is quick, and couples the class to the table, the tests to the table, and hides queries in innocent calls.

**What this project must deliver:** a record that finds and saves itself, finders and rules on the class, each of the three bills shown with counted table operations, and a plain verdict.
""",
roles=[
    ('Records', '`Order`, `Customer`'),
    ('Storage', '`Table`, counting every operation'),
    ('Contrast', '`PureDiscount`'),
    ('Entry point', '`ActiveRecordDemo`, six acts'),
],
requirements=[
    '**Table operations are counted,** never timed.',
    '**The renamed column is asserted to break loading.**',
    '**Five orders cause five operations,** and the pure rule causes none.',
    '**Saving twice updates one row.**',
],
),

"optimistic-offline-lock": dict(
purpose="""
Teach Optimistic Offline Lock with two clerks editing one product: a store with no lock that silently loses the price change, a version per row that refuses the stale save, a retry that reloads and reapplies so both changes survive, a conflict on different fields that was not really one, ten writers on a busy row where nine of ten saves are repeated, and a long edit of five changes discarded when it is finally saved.
""",
nongoals=[
    'Not a database. The store is in memory, and its synchronised save stands in for a conditional update.',
    'Not field-level merging. It is named as the alternative, not built.',
    'Not the pessimistic lock. That is the next project.',
],
problem="""
Two people edit the same row and the last save silently wins.

**What this project must deliver:** a lost update shown for real, a version that refuses the stale save, a retry that keeps both changes, and the three costs of the pattern shown with counted saves.
""",
roles=[
    ('Stores', '`OptimisticStore`, `LastWriteWinsStore`'),
    ('Values', '`Product`, `Versioned`, `StaleWrite`'),
    ('Entry point', '`OptimisticLockDemo`, six acts'),
],
requirements=[
    '**The lost update is real:** the last-write-wins row loses the price.',
    '**A stale save is refused and the first write survives.**',
    '**Ten writers on one row lose nothing and attempt nineteen saves.**',
    '**Different fields still conflict,** because the version is per row.',
],
),

"pessimistic-offline-lock": dict(
purpose="""
Teach Pessimistic Offline Lock with two clerks editing a product: a lock that refuses the second clerk and names the holder, edits that overwrite nothing, the cost of waiting, a forgotten lock that expires on a clock the demo controls and stops the old owner writing, a deadlock between two clerks and its fix by taking locks in a fixed order, and the difference between locking a whole catalogue and a single product.
""",
nongoals=[
    "Not a database lock. It is an application-level lock manager, which is what 'offline' means here.",
    'Not a distributed lock. There is one process.',
    'Not a fairness or queueing scheme. Waiting is by retrying.',
],
problem="""
Where a clash would cost a lot, detecting it at save time is too late.

**What this project must deliver:** a lock that prevents the clash and names its holder, edits that overwrite nothing, the cost of waiting, an expiring lock on a controlled clock, a deadlock and its fix, the granularity choice, and a plain verdict.
""",
roles=[
    ('Locking', '`LockManager`, `LockedBy`, `Clock`'),
    ('Data', '`ProductStore`'),
    ('Entry point', '`PessimisticLockDemo`, six acts'),
],
requirements=[
    '**Expiry uses a clock the demo controls,** never a real wait.',
    "**A write without the lock is refused,** including the old owner's after expiry.",
    '**A deadlock is shown, and fixed-order locking avoids it.**',
    '**Only the holder can release.**',
],
),

"front-controller": dict(
purpose="""
Teach Front Controller with a web store: three handlers that each look after their own sign-in and logging and one that forgets both, one entry point with filters and a routing table that checks the sign-in once for every route, answers unknown pages and wrong methods uniformly, logs even refused requests, and hides a failure's detail from the customer, and the outage that one buggy filter causes across every page.
""",
nongoals=[
    'Not a web framework. Requests and responses are plain records.',
    'Not a security tutorial. The token check is deliberately trivial.',
    'Not an API gateway. That is a separate pattern in the microservices category.',
],
problem="""
Shared work written into every handler gets forgotten by one of them.

**What this project must deliver:** a naive set of handlers with a real unauthenticated hole, one controller with filters and routes that closes it, central 404, 405 and 500 answers, a log that includes refused requests, and the single point of failure shown honestly.
""",
roles=[
    ('The door', '`FrontController`, `Filters`, `Filter`'),
    ('Handlers', '`Handlers`, `Handler`'),
    ('Values', '`Request`, `Response`, `Journal`'),
    ('Naive', '`NaiveHandlers`'),
    ('Entry point', '`FrontControllerDemo`, six acts'),
],
requirements=[
    '**The forgotten check is a real hole:** the naive orders handler serves an unsigned visitor.',
    '**Refused requests are logged.**',
    "**A failure's message never reaches the customer.**",
    '**A buggy filter brings every route down,** and a test says so.',
],
),

"gateway": dict(
purpose="""
Teach Gateway with a payment provider: three features that call the provider's client directly and build its fields and read its codes themselves, one of which forgot the currency; one gateway in the shop's words that alone knows Acme's fields and codes; tests with a fake that never touches the network; a timeout retried once in one place; a second provider behind the same door with the shop unchanged; and the limit that a common interface can only say what every provider can say.
""",
nongoals=[
    'Not a payment integration. The provider clients are small simulations with scripted answers.',
    'Not a full resilience story. There is one retry, and the other patterns are in the microservices category.',
    'Not the Adapter pattern by name, though the shape is the same.',
],
problem="""
Calling an outside system's client from many places spreads its fields and codes, and makes every test a network test.

**What this project must deliver:** a gateway in the shop's words, one class that knows the provider, a fake that makes no network calls, a retry in one place, a second provider behind the same door, the naive callers' real bug, and the limit of a common interface.
""",
roles=[
    ('The door', '`PaymentGateway`, `PaymentResult`, `PaymentStatus`'),
    ('Implementations', '`AcmeGateway`, `BetaGateway`, `FakeGateway`'),
    ('The shop', '`Checkout`'),
    ('Providers', '`vendor.AcmeClient`, `vendor.BetaPayClient`'),
    ('Naive', '`NaiveCheckout`'),
    ('Entry point', '`GatewayDemo`, six acts'),
],
requirements=[
    '**Network calls are counted:** the fake makes none.',
    '**Every Acme code is translated,** and an unknown code is not swallowed.',
    '**One timeout is retried once,** two are reported as unavailable.',
    '**The naive gift card really omits the currency.**',
],
),

"cache-aside": dict(
purpose="""
Teach Cache-Aside with product page views: a thousand views costing a thousand database reads and then ten, a write that forgets the cache and serves the old price against one that invalidates, an expiry on a controlled clock that bounds staleness, fifty simultaneous misses on one expired key costing fifty reads against one shared read, and the bill of a cold cache and a second copy to keep right.
""",
nongoals=[
    'Not a distributed cache. There is one in-memory cache in one process.',
    'Not a survey of eviction policies. Expiry is the only one shown.',
    'Not write-through or write-behind. Cache-aside only.',
],
problem="""
Reading the same few rows from a database on every request wastes it, and a cache in front brings stale data and stampedes.

**What this project must deliver:** a read count with and without the cache, a stale read and its fix, an expiry on a controlled clock, a deterministic stampede and its single-flight fix, and the cold start cost.
""",
roles=[
    ('The pattern', '`ProductService`, `Cache`'),
    ('Source', '`Database`'),
    ('Support', '`Clock`, `Product`'),
    ('Entry point', '`CacheAsideDemo`, six acts'),
],
requirements=[
    '**Reads are counted,** never timed.',
    '**Expiry uses a clock the demo controls.**',
    '**The stampede is deterministic:** every caller has missed before any read completes, and the counts are 50 and 1.',
    '**A forgotten invalidation is asserted to serve stale data.**',
],
),

"rate-limiter": dict(
purpose="""
Teach Rate Limiter with a product search: a thousand requests to a service that can serve a hundred, a token bucket on a controlled clock that allows a burst of ten then refills at five a second, a steady rate that is never refused, a bucket per caller against one shared bucket, a refusal that says exactly when to retry to the millisecond, and the bills of per-server buckets, memory for ten thousand callers, and a page that looks like a script.
""",
nongoals=[
    'Not a distributed limiter. Sharing the count between servers is named, not built.',
    'Not the leaky bucket or sliding window. The token bucket is the one shown.',
    'Not an API gateway. The limiter is a class, not a proxy.',
],
problem="""
A shared service can be used up by one caller, and a limit brings its own costs.

**What this project must deliver:** a token bucket with exact integer arithmetic, a burst allowed and refused, a steady rate that always passes, per-caller fairness, an exact retry-after, and the three bills shown with counts.
""",
roles=[
    ('The pattern', '`TokenBucket`, `RateLimiter`'),
    ('The service', '`SearchService`'),
    ('Support', '`Clock`'),
    ('Entry point', '`RateLimiterDemo`, six acts'),
],
requirements=[
    '**Time is a clock the demo controls,** never a real wait.',
    '**Arithmetic is exact:** milli-tokens, no floating point.',
    '**A steady rate at the refill rate is never refused,** asserted over 300 requests.',
    '**Retry-after is exact:** early is refused, on time is allowed.',
],
),

"timeout": dict(
purpose="""
Teach Timeout with a supplier's stock API: a call with no limit whose thread is WAITING with nothing to end it, a call with a limit that shows a plain answer instead, the supplier finishing the work after the caller gave up, the effect of the limit on a typical hundred calls, one time budget shared by three calls, and a payment that times out and still happens.
""",
nongoals=[
    'Not a full resilience story. Retry, breaker and bulkhead are separate projects.',
    'Not real network timeouts. The silence is a gate, so it is exact.',
    'Not measuring real latency. The typical hundred calls are numbers.',
],
problem="""
A call with no limit lets a slow or silent service hold a thread forever, and a limit brings its own uncertainty.

**What this project must deliver:** a thread shown waiting with nothing to end it, a limit that produces an answer, work that continues after giving up, the effect of the number on a typical hundred calls, a shared budget, and a timed-out payment that still happens.
""",
roles=[
    ('The pattern', '`Callers`, `Budget`'),
    ('The supplier', '`SupplierApi`, `Gate`'),
    ('Data', '`Latency`'),
    ('Entry point', '`TimeoutDemo`, six acts'),
],
requirements=[
    '**Silence is exact:** the supplier is held at a gate.',
    '**Waits are polled, never slept.**',
    '**The abandoned work is asserted to finish anyway.**',
    '**A budget never spends more than it has,** checked over a range.',
],
),

"queue-based-load-leveling": dict(
purpose="""
Teach Queue-Based Load Leveling with a sale that starts with a hundred orders at once: a worker of ten a tick refusing ninety when the burst goes straight to it, a queue that spreads the same burst with nothing lost, the wait the queue costs, an unbounded queue growing to five hundred against a bounded one refusing four hundred and sixty, the effect of a faster worker, and seventy orders lost when an in-memory queue stops.
""",
nongoals=[
    'Not a message broker. The queue is a model in ticks.',
    'Not throughput tuning. It is a picture of what the queue does, with exact counts.',
    'Not a durable queue. Durability is named as the requirement, not built.',
],
problem="""
A burst that arrives faster than a service can work is refused if it goes straight through.

**What this project must deliver:** a burst refused and the same burst queued with exact counts, the waiting cost, an unbounded queue against a bounded one, the effect of worker speed, orders lost when an in-memory queue stops, and a plain verdict.
""",
roles=[
    ('The model', '`Sim`, `Result`'),
    ('Entry point', '`LoadLevelingDemo`, six acts'),
],
requirements=[
    '**Every run is exact:** ticks and integer arithmetic, no clocks or threads.',
    '**Every order is accounted for:** arrived = processed + refused + lost + waiting, over a range of limits and crash points.',
    '**The wait is exact:** first 0, last 9, average 4.5.',
    "**An in-memory queue's loss is asserted.**",
],
),

"competing-consumers": dict(
purpose="""
Teach Competing Consumers with a queue of orders: one consumer against three with six held jobs, a thousand orders handled exactly once by four consumers, ordering lost when the first message's consumer is held, a failed message given back and handled by another attempt, the duplicate charge that at-least-once delivery causes against a consumer that remembers, and six consumers sharing a database that admits two.
""",
nongoals=[
    'Not a message broker. The broker is a small in-memory queue with acknowledge and give-back.',
    'Not exactly-once delivery. It is at-least-once, and the fix is in the consumer.',
    'Not partitioning. It is named as the way to keep order.',
],
problem="""
One worker cannot keep up, and several workers on one queue give up ordering and risk duplicates.

**What this project must deliver:** a broker that hands each message to one consumer and takes it back on failure, exactly-once handling in the normal case, ordering lost, a failed message taken over, the duplicate and its fix, a shared downstream cap, and every count exact.
""",
roles=[
    ('The pattern', '`Broker`, `ConsumerPool`, `Delivery`'),
    ('Support', '`Gate`'),
    ('Entry point', '`CompetingConsumersDemo`, six acts'),
],
requirements=[
    '**Every count is exact,** held by gates, and asserted over repeated runs.',
    '**Each message is handled once in the normal case:** 500 and 1000 messages, distinct ids equal total.',
    '**Ordering loss is exact:** [2, 3, 1].',
    '**A crash after the effect produces a duplicate,** and a remembering consumer does not.',
],
),

"claim-check": dict(
purpose="""
Teach Claim Check with an invoice PDF: a broker that refuses a five thousand byte message, a claim of an id, a size and a checksum that carries it instead, five hundred thousand bytes against five thousand nine hundred for a hundred invoices, blobs nobody collected swept after their time limit and a late claim refused, a changed byte caught by the checksum, and the bills of extra steps, guessable claims and the gap between storing and sending.
""",
nongoals=[
    'Not a real broker or object store. Both are small in-memory classes.',
    'Not access control beyond unguessable ids. Signing and time-limited claims are named.',
    'Not the outbox pattern, though it faces the same gap.',
],
problem="""
A message too big for the broker cannot be sent whole.

**What this project must deliver:** a broker with a size limit, a claim with a checksum, a sender and receiver that use it, bytes carried with and without, uncollected blobs swept, a tampered blob refused, and the bills shown.
""",
roles=[
    ('The pattern', '`Sender`, `Receiver`, `Claim`'),
    ('Infrastructure', '`Broker`, `BlobStore`, `Clock`'),
    ('Entry point', '`ClaimCheckDemo`, six acts'),
],
requirements=[
    '**Bytes are counted,** never timed.',
    '**Expiry uses a clock the demo controls.**',
    '**A tampered payload is refused by its checksum.**',
    '**Sequential claims are shown to be guessable,** and random claims are not.',
],
),

"leader-election": dict(
purpose="""
Teach Leader Election with a nightly report: three copies each sending it, a lease that gives the job to one, the delay before a dead leader's lease expires and another takes over, a paused leader that wakes still believing it leads so that two send, fencing tokens that make the report sink refuse the replaced leader, and the bill of a lease that is too short for the renewal interval.
""",
nongoals=[
    'Not consensus. The lease store is one record, standing in for ZooKeeper or etcd.',
    "Not clock synchronisation. Every node reads the store's clock.",
    'Not a full scheduler. The job is one write to a sink.',
],
problem="""
Identical copies of a service all run the same job unless something makes exactly one responsible.

**What this project must deliver:** the duplicate report, a lease with a token, the takeover delay, the two-leaders problem, fencing, the lease-versus-renewal bill, and a plain verdict.
""",
roles=[
    ('The pattern', '`LeaseStore`, `Lease`, `Node`'),
    ("The job's target", '`ReportSink`'),
    ('Support', '`Clock`'),
    ('Entry point', '`LeaderElectionDemo`, six acts'),
],
requirements=[
    '**Time is a clock the demo controls,** never a real wait.',
    '**The token goes up at every change of holder.**',
    "**A replaced leader's write is refused with fencing and accepted without.**",
    '**A lease shorter than the renewal interval loses a healthy leader,** at an exact second.',
],
),

"publisher-subscriber": dict(
purpose="""
Teach Publisher-Subscriber with an order being placed: an order service that calls inventory, email and analytics by name, a topic that is an append-only log with a reader position per subscriber so the same order service only publishes, a fourth subscriber added with no change, a slow subscriber with its own backlog, filters by kind, a live subscriber and a replaying one, and an absent subscriber that catches up while the publisher learns nothing.
""",
nongoals=[
    'Not a real broker. The topic is an in-memory log.',
    'Not delivery guarantees across machines. Delivery is a method call, made by hand.',
    'Not the Observer pattern by name, though it is the same idea.',
],
problem="""
A service that calls every interested party by name must change whenever a new one appears.

**What this project must deliver:** a publisher that only appends, subscribers that read at their own position and pace with their own filter, a late subscriber shown live and replaying, an absent subscriber that catches up, and the publisher's ignorance of delivery shown honestly.
""",
roles=[
    ('The pattern', '`Topic`, `Event`'),
    ('Naive', '`DirectOrderService`'),
    ('Entry point', '`PublisherSubscriberDemo`, six acts'),
],
requirements=[
    '**Delivery is a method call,** so every run is the same.',
    "**A subscriber's backlog is asserted exactly.**",
    '**A live subscriber misses history and a replaying one does not.**',
    "**A disconnected subscriber's position is kept.**",
],
),

"pipes-and-filters": dict(
purpose="""
Teach Pipes and Filters with an order import: one loop that does five jobs and drops bad lines with no trace, the same job as five typed filters joined into a pipeline, a swapped tax step and an added step with no change to any other, bad lines rejected with the step and the reason while the rest continue, streaming holding one item against twenty thousand for a stage at a time, and the shape problem of steps passing loose maps.
""",
nongoals=[
    'Not a batch framework. The pipeline is a small class.',
    'Not concurrency. Items go through one at a time, in order.',
    'Not the Java Streams API, though it is the same idea.',
],
problem="""
One method that does every step of a job cannot be tested, changed or explained a step at a time.

**What this project must deliver:** filters that pass or reject with a reason, a pipeline that joins them, the same results as the big method, a swapped and an added step, rejects reported, streaming against stage-by-stage memory, and the shape problem shown.
""",
roles=[
    ('The pattern', '`Filter`, `Pipeline`'),
    ('The import', '`Shop`, its filters and types'),
    ('Naive', '`BigImport`'),
    ('Entry point', '`PipesAndFiltersDemo`, six acts'),
],
requirements=[
    '**The pipeline and the big method agree** on the good lines.',
    '**Each filter is tested alone.**',
    '**Rejects carry the step and the reason,** in order.',
    '**Streaming holds 1 item and stage-by-stage holds 2000 for 1000 lines,** with identical output.',
],
),

"scatter-gather": dict(
purpose="""
Teach Scatter-Gather with a product page's best price from four suppliers: asking them in turn for thirteen hundred milliseconds and all at once for nine hundred, four suppliers held at a gate to show they are being asked at the same moment, a deadline that leaves the slow one out and names it, a partial answer reported honestly, a failing supplier that does not fail the page, and the bills of fan-out and of the slowest of many setting the pace.
""",
nongoals=[
    'Not a search engine. There are four stand-in suppliers.',
    'Not streaming results. The gatherer waits for the deadline or for all.',
    'Not caching. It is named as the way to cut the calls.',
],
problem="""
Asking several sources one after another is slow, and asking them together means the slowest sets the pace.

**What this project must deliver:** the latency arithmetic, a real parallel ask shown by a gate, a deadline that leaves out a slow supplier and names it, a failure treated as lateness, a partial result reported honestly, and the fan-out bill.
""",
roles=[
    ('The pattern', '`ScatterGather`, `Supplier`, `Quote`'),
    ('Support', '`Gate`, `Latencies`'),
    ('Entry point', '`ScatterGatherDemo`, six acts'),
],
requirements=[
    '**Latency is arithmetic,** never a sleep.',
    '**Four suppliers are asked at the same moment,** asserted by holding them at a gate, over repeated runs.',
    '**A slow supplier is left out and named,** and a failing one is named with its reason.',
    '**When nobody answers there is no best price,** not an error.',
],
),

"message-channel": dict(
purpose="""
Teach Message Channel with checkout and a warehouse: three checkouts failing while the warehouse is down when they call it directly, a channel that lets checkout carry on and delivers the messages in order when the warehouse returns, an envelope of headers and a body, a channel that carries one type of message, and the bill of a full channel and a sender that no longer hears the answer.
""",
nongoals=[
    'Not a message broker product. The channel is a small in-memory queue.',
    'Not publish-subscribe. That is Event Bus, later in this category.',
    'Not delivery guarantees. Persistence is named as the requirement.',
],
problem="""
A direct call ties the sender to the receiver being up.

**What this project must deliver:** a direct call that fails, a channel that decouples them in time with messages in order, an envelope, a typed and bounded channel, and the loss of the sender's answer.
""",
roles=[
    ('The pattern', '`Channel`, `Message`, `WrongType`, `ChannelFull`'),
    ('The receiver', '`Warehouse`'),
    ('Entry point', '`MessageChannelDemo`, six acts'),
],
requirements=[
    '**No threads or clocks:** every run is the same.',
    '**Messages arrive in the order sent.**',
    '**A wrong-type message is refused and nothing is queued.**',
    '**A full channel refuses and loses nothing already accepted.**',
],
),

"content-based-router": dict(
purpose="""
Teach Content-Based Router with orders of different kinds: one channel that forces the warehouse to sort, a router with ordered rules that sends six orders to four channels, two rule orders giving two answers for one gift card, a message no rule covers that is caught by a fallback or dropped and counted, a rule added with no other change, and the bill of a renamed value that makes a rule miss.
""",
nongoals=[
    'Not a message broker. Channels are lists of ids.',
    'Not header-based routing in full. It is named as the alternative.',
    'Not dynamic rules loaded from configuration.',
],
problem="""
Messages of several kinds on one channel make the receiver sort them, and every new kind changes the receiver.

**What this project must deliver:** ordered rules, a fallback, a count of dropped messages, the effect of rule order, an added rule with no other change, and the coupling to content shown.
""",
roles=[
    ('The pattern', '`Router`, `Route`'),
    ('Values', '`Order`'),
    ('Entry point', '`ContentRouterDemo`, six acts'),
],
requirements=[
    '**Every order goes to exactly one channel** when there is a fallback.',
    '**Rule order changes the answer,** asserted.',
    '**Without a fallback, an unmatched order is dropped and counted.**',
    '**A renamed field value makes a rule miss,** asserted.',
],
),

}


# ---------------------------------------------------------------------------
# Facts read from the project itself, so no number in a spec is typed by hand.
# ---------------------------------------------------------------------------

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     ".loudness-cache.json")


def load_cache():
    import json
    try:
        return json.load(open(CACHE))
    except (OSError, ValueError):
        return {}


def save_cache(c):
    import json
    json.dump(c, open(CACHE, "w"), indent=1, sort_keys=True)


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout.strip()


def facts(group, slug, measure=True):
    p = os.path.join(ROOT, group, slug + "-pattern")
    v, d = os.path.join(p, "video"), os.path.join(p, "docs")
    f = {"dir": p}

    src = os.path.join(p, "src", "main", "java", "com", "jk", "explore")
    pkg = os.listdir(src)[0]
    f["package"] = "com.jk.explore." + pkg
    f["classes"] = len([x for x in os.listdir(os.path.join(src, pkg))
                        if x.endswith(".java")])

    tst = os.path.join(p, "src", "test", "java", "com", "jk", "explore", pkg)
    names, total = [], 0
    for x in sorted(os.listdir(tst)):
        if not x.endswith(".java"):
            continue
        body = open(os.path.join(tst, x)).read()
        n = len(re.findall(r'@(?:Test|ParameterizedTest|RepeatedTest)\b', body))
        if n:
            names.append("`%s`" % x[:-5])
            total += n
    f["tests"], f["test_classes"] = total, names

    # A project's code and docs are written before its video pipeline is, and
    # its spec is what the pipeline is then built against — so a missing
    # scenes.py is a stage rather than an error, exactly as a missing MP4 is
    # below. Everything the spec says about the video is stated as a
    # requirement either way; only the measured numbers wait.
    scenes = os.path.join(v, "scenes.py")
    f["scenes"] = (len(re.findall(r'title=', open(scenes).read()))
                   if os.path.exists(scenes) else 0)

    srt = ([x for x in os.listdir(v) if x.endswith(".srt")]
           if os.path.isdir(v) else [])
    f["cues"] = (len(re.findall(r' --> ', open(os.path.join(v, srt[0])).read()))
                 if srt else 0)

    mp4 = os.path.join(v, "%s-pattern-explained.mp4" % slug)
    f["mp4"] = mp4 if os.path.exists(mp4) else None
    if f["mp4"]:
        dur = float(sh(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of", "csv=p=0", mp4]))
        f["runtime"] = "%d:%02d" % (int(dur // 60), int(dur % 60))
    else:
        f["runtime"] = "not yet built"

    f["title"] = "not yet generated"
    ymd = os.path.join(d, "youtube.md")
    if os.path.exists(ymd):
        m = re.search(r'## Title\n\n```\n(.+?)\n```', open(ymd).read())
        if m:
            f["title"] = m.group(1)

    # Measuring loudness means decoding a ten-minute file, so the result is
    # cached against the MP4's size and mtime. Rebuilding the video changes
    # both, so the cache cannot go stale behind a new render.
    f["loudness"] = None
    if measure and f["mp4"]:
        st = os.stat(mp4)
        key = "%s:%d:%d" % (slug, st.st_size, int(st.st_mtime))
        cache = load_cache()
        if key in cache:
            f["loudness"] = tuple(cache[key])
            return f
        out = subprocess.run(
            ["ffmpeg", "-hide_banner", "-nostats", "-i", mp4, "-af",
             "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
            capture_output=True, text=True).stderr
        try:
            import json
            blob = out[out.rindex("{"):]
            m = json.loads(blob[:blob.index("}") + 1])
            f["loudness"] = (m["input_i"], m["input_tp"])
            cache[key] = list(f["loudness"])
            save_cache(cache)
        except (ValueError, KeyError):
            pass
    return f


# ---------------------------------------------------------------------------
# The document.
# ---------------------------------------------------------------------------

def build_md(group, slug, f):
    name = NAMES[slug]
    meta = META[slug]
    idx = [s for _, s in ORDER].index(slug)
    nxt = NAMES[ORDER[idx + 1][1]] if idx + 1 < len(ORDER) else None
    is_ref = slug == "abstract-factory"

    if is_ref:
        provenance = (
            "This project is the reference implementation of that standard -- "
            "the other thirteen projects' build scripts are generated from this "
            "one -- so a change here is a change to all fourteen and must be "
            "made there first.")
    else:
        provenance = (
            "This project's `video/build_video.sh` is generated from "
            "`creational/abstract-factory-pattern`'s, differing only in the "
            "pattern name and the output filenames, so a change to the pipeline "
            "belongs there and in the repository-wide spec, not here.")

    parts = []
    A = parts.append

    A("# %s Pattern — Project Specification\n" % name)
    A("The single reference document for this project: what it teaches, how it\n"
      "is built, and the quality bar its video and its YouTube publication have\n"
      "to meet.\n")
    A("This is a *specification*, not a tutorial. It says what must be true and\n"
      "why. The teaching material itself lives in\n"
      "[`%s-pattern-explained.md`](%s-pattern-explained.md); the problem it\n"
      "addresses is set out at length in\n"
      "[`problem-statement.md`](problem-statement.md).\n" % (slug, slug))
    A("Where this document repeats a rule from the repository-wide\n"
      "[`video-and-publishing-spec.md`](../../../docs/video-and-publishing-spec.md),\n"
      "that document is the authority. %s\n" % provenance)
    A("---\n")

    A("## 1. Purpose\n")
    A(meta["purpose"].strip() + "\n")
    A("The three formats are not alternatives. A learner is expected to read the\n"
      "problem statement, run the code, then watch the video — or watch first and\n"
      "read after. Whichever order they choose, the class names, the numbers and\n"
      "the scenario must be identical, because the value of the repository is\n"
      "that a learner carries one e-commerce domain from pattern to pattern and\n"
      "only has to absorb the new structure.\n")
    A("### Non-goals\n")
    for x in meta["nongoals"]:
        A("- " + x)
    A("")
    A("---\n")

    A("## 2. Problem statement\n")
    A("The full treatment is in [`problem-statement.md`](problem-statement.md).\n"
      "In brief:\n")
    A(meta["problem"].strip() + "\n")
    A("---\n")

    A("## 3. Code\n")
    A("### Structure\n")
    A("%d production classes under `%s`:\n" % (f["classes"], f["package"]))
    A("| Role | Types |")
    A("| --- | --- |")
    for role, types in meta["roles"]:
        A("| %s | %s |" % (role, types))
    A("")
    A("### Requirements\n")
    for i, x in enumerate(meta["requirements"], 1):
        A("%d. %s" % (i, x))
    A("%d. **Java 21, no third-party runtime dependencies.** JUnit 5 for tests\n"
      "   only, so the project is readable by someone who does not know a DI\n"
      "   framework.\n"
      "%d. **Every class fits on a slide.** This is teaching code; a class that\n"
      "   needs scrolling to read has failed its purpose regardless of its\n"
      "   design.\n"
      % (len(meta["requirements"]) + 1, len(meta["requirements"]) + 2))
    A("### Verification\n")
    A("- `./gradlew build` passes. %d test method%s across %s.\n"
      "- `./gradlew run` output is quoted verbatim in the top-level `README.md`,\n"
      "  and must still match."
      % (f["tests"], "" if f["tests"] == 1 else "s",
         ", ".join(f["test_classes"])))
    A("")
    if slug in NONDETERMINISTIC:
        A("The demo mints an identifier per run, so the codes it prints differ\n"
          "each time. Every other line of the output is stable and must match the\n"
          "README exactly; the README says which lines are expected to vary.\n")
    if f["tests"] < 5:
        A("> **Known gap.** %d test method is well below the %d–%d the other\n"
          "> projects carry, and it is not enough to defend the requirements\n"
          "> above — in particular, nothing currently fails if the four steps are\n"
          "> reordered, which is the pattern's whole point. This is a real\n"
          "> shortfall in the project, recorded here rather than quietly\n"
          "> tolerated.\n" % (f["tests"], 9, 23))
    A("---\n")

    A("## 4. Written material\n")
    A("Every document in `docs/` is required, and each has one job. A learner\n"
      "reading them in the order given by the top-level README's table should\n"
      "never need to jump forward.\n")
    A("| Document | Job |")
    A("| --- | --- |")
    for doc, job in [
        ("`prerequisites.md`", "What to know and install first"),
        ("`problem-statement.md`", "The problem and why the naive approach hurts"),
        ("`%s-pattern-explained.md`" % slug,
         "The pattern, the code, pitfalls, comparisons"),
        ("`class-diagram.md` + PNG", "Static structure"),
        ("`uml-diagram.md` + PNG", "Runtime call flow"),
        ("`animation.html`", "Step-by-step walkthrough, optionally narrated"),
        ("`session.md`", "A 60-minute guided teaching session"),
        ("`youtube.md`", "Everything needed to publish the video"),
        ("`thumbnail.png`", "The image to upload"),
        ("`spec.md` / `spec.html`", "This document"),
    ]:
        A("| %s | %s |" % (doc, job))
    A("")
    A("Both Mermaid diagrams are committed as source *and* rendered PNG. The PNG\n"
      "is what the README embeds, because GitHub's Mermaid rendering cannot be\n"
      "relied on at these diagrams' size; the source is what gets edited.\n"
      "Regenerating after an edit is mandatory — a diagram that disagrees with\n"
      "the code is worse than no diagram.\n")
    A("---\n")

    A("## 5. Video quality specification\n")
    A("The finished video is `video/%s-pattern-explained.mp4`, with an\n"
      "audio-only `.m4a` and a `.srt` subtitle track alongside it. It is built by\n"
      "`video/build_video.sh`, from scenes declared in `video/scenes.py` and\n"
      "slides rendered by `video/make_slides.py`.\n" % slug)
    A("### 5.1 The opening, in four steps\n")
    A("Scene 1 is the only scene whose narration has a required structure, and\n"
      "it is required because it is the scene that decides whether anybody\n"
      "watches the second one. It must run in this order:\n")
    A("1. **What the video is** — \"This video explains the %s pattern in\n"
      "   Java\", plainly, before anything else.\n"
      "2. **The author credit** — \"and it is written and presented by\n"
      "   Jayasekhar Konduru\".\n"
      "3. **The pattern's definition, in general terms** — two or three\n"
      "   sentences of plain language, with no mention yet of the store, the\n"
      "   catalog or the checkout. A viewer who stops here has still learnt\n"
      "   what the pattern is.\n"
      "4. **Then the same thing in full, in the e-commerce domain** — the\n"
      "   worked scenario, and what the viewer will be able to do by the end.\n"
      % NAMES[slug])
    A("> **Requirement.** Steps 3 and 4 are separate and in that order. They\n"
      "> used to be one step: the video opened straight into the shop's\n"
      "> scenario and left the general definition to be inferred from a worked\n"
      "> example, which works for a viewer already halfway to knowing the\n"
      "> pattern and fails for everyone else. The cost is fifteen to thirty\n"
      "> seconds of runtime, spent at the only point in the video where a\n"
      "> viewer is still deciding whether to leave.\n")
    A("### 5.2 Delivered characteristics\n")
    A("| Property | Value | Why |")
    A("| --- | --- | --- |")
    for row in [
        ("Container", "MP4, `+faststart`",
         "The index sits at the front, so the poster paints the moment the file opens"),
        ("Video", "H.264, 1920×1080, 30 fps, CRF 18, `preset slow`, `yuv420p`",
         "1080p is the minimum at which code on a slide is readable; `yuv420p` is what every player accepts"),
        ("B-frames", "Disabled (`-bf 0`)",
         "They save nothing on a static slide and complicate the timestamps the gap check reads"),
        ("Audio", "AAC-LC, 48 kHz, stereo, 192 kbps",
         "YouTube's recommended upload settings, so no re-encode on their side"),
        ("Loudness", "−16 LUFS integrated, true peak ≤ −1.5 dBTP",
         "YouTube's normalisation target — deliver at it and the platform leaves the audio alone"),
        ("Stream start", "Both streams at exactly 0.000 s",
         "Otherwise the video track starts 21 ms late and players show black at 0:00"),
        ("Narration", "macOS `say`, voice Samantha, 145 wpm",
         "The pace educational YouTube converges on for technical material"),
        ("Inter-scene pause", "0.9 s of appended silence",
         "So slides do not snap past the moment a sentence ends"),
        ("Runtime", "~%s over %d scenes, %d subtitle cues"
         % (f["runtime"], f["scenes"], f["cues"]), ""),
    ]:
        A("| %s | %s | %s |" % row)
    A("")
    A("### 5.3 The two defects this pipeline exists to prevent\n")
    A("Both produce a file that looks fine and sounds broken, and both were live\n"
      "in this repository before the current build script. They are documented\n"
      "here because the obvious \"simplification\" of the pipeline reintroduces\n"
      "them.\n")
    A("**Per-scene AAC concatenation.** AAC is a lapped format: every separately\n"
      "encoded clip carries priming samples at its head and padding at its tail.\n"
      "Concatenating such clips with `-c copy` strips neither, so each join\n"
      "leaves a hole in the timeline. Measured on the reference project before\n"
      "the fix: 30 gaps totalling 31 seconds of missing narration.\n")
    A("> **Requirement.** Each scene's narration is written as lossless PCM WAV.\n"
      "> The joined narration is encoded to AAC exactly once, at the final mux.\n"
      "> There must be exactly one `-c:a aac` in the build script.\n")
    A("**Dynamic-mode `loudnorm`.** Left to itself `loudnorm` rides the level as\n"
      "it goes, and on some narrations emits a timestamp discontinuity partway\n"
      "through — the same audible hole, mid-sentence, with nothing wrong\n"
      "upstream of it.\n")
    A("> **Requirement.** Loudness is measured over the whole narration in a\n"
      "> first pass, and the measured figures are fed back with `linear=true` so\n"
      "> the second pass applies one constant gain. This also stops the level\n"
      "> pumping between quiet and loud lines.\n")
    A("### 5.4 Why there is no denoiser\n")
    A("An earlier version ran `afftdn` over the narration and, by the numbers, it\n"
      "worked — about 15 dB off the noise floor. It also made the voice\n"
      "noticeably worse. A spectral denoiser needs a real, roughly stationary\n"
      "noise floor to subtract; synthesised speech has almost none, so `afftdn`\n"
      "subtracts parts of the speech instead and leaves it warbling.\n")
    A("> **Requirement.** The `CLEANUP` chain contains no `afftdn` and no\n"
      "> `lowpass`. It is exactly: resample to 48 kHz with a long filter\n"
      "> (`filter_size=512`, `cutoff=0.98`, `linear_interp=1`), a 75 Hz high-pass\n"
      "> for rumble, and a gentle +1.5 dB shelf at 3 kHz for consonants. The\n"
      "> faint remaining hiss is much the lesser problem.\n")
    A("Levelling is deliberately not in this chain either: run per scene it\n"
      "re-measures on every clip, so a quiet scene is pushed up to match a loud\n"
      "one and the level audibly steps at each join. It happens once, over the\n"
      "whole narration.\n")
    A("### 5.5 Synchronisation\n")
    A("Scene lengths are rounded up to a whole number of video frames —\n"
      "`frames = ceil(duration × 30)`, `target = frames / 30` — and each scene's\n"
      "WAV is padded to exactly that target. Picture and narration are therefore\n"
      "the same length for every scene, so slide changes cannot drift away from\n"
      "the voice however many scenes the video grows to.\n")
    A("### 5.6 Self-check, and its limit\n")
    A("After the mux the build reads every audio packet timestamp and fails if\n"
      "any two are more than one AAC frame apart, printing\n"
      "`audio timeline continuous: N packets, no gaps`. A build that does not\n"
      "print that line has not passed.\n")
    A("**This check verifies continuity, not fidelity.** It cannot hear\n"
      "warbling, clipping or a bad voice — the `afftdn` problem passed it\n"
      "cleanly for weeks. Any change to the filter chain or the voice requires\n"
      "someone to actually listen to the result before it is called done.\n"
      "Objective measurement of the delivered file (integrated loudness, true\n"
      "peak, silence detection) is a useful guard but is not a substitute for\n"
      "that.\n")
    A("---\n")

    A("## 6. Poster and thumbnail\n")
    A("Two different images, for two different jobs. Conflating them is the\n"
      "mistake this section exists to prevent.\n")
    A("**`video/poster.png`** — 1920×1080, the video's opening frame, lifted out\n"
      "of the build. It carries the before/after comparison: the approach being\n"
      "replaced on one side, the pattern on the other.\n")
    A("**`docs/thumbnail.png`** — 1280×720, generated by\n"
      "[`make_thumbnails.py`](../../../docs/make_thumbnails.py), and the image\n"
      "that is uploaded. It is deliberately not the poster: YouTube serves a\n"
      "thumbnail at roughly 360 pixels wide in a search result, and at that size\n"
      "a two-column code comparison is a smudge. The thumbnail therefore carries\n"
      "three things only — the pattern name, one line of promise, and one short\n"
      "piece of code — each set large enough to survive the shrink.\n")
    A("> **Requirement.** Neither image strikes out its \"before\" sample. A rule\n"
      "> drawn through monospace is hard to read at full size and illegible at\n"
      "> thumbnail size, and striking the code out makes the card read as being\n"
      "> about what is wrong rather than what is being taught. The rejected\n"
      "> approach is marked with a `BEFORE` chip and the pattern with an `AFTER`\n"
      "> chip; colour and label carry the contrast.\n")
    A("> **Requirement.** The poster is inspected visually before it is\n"
      "> considered done, not merely confirmed to exist. `proxy-pattern` once\n"
      "> shipped a poster reading \"DECORATOR PATTERN\", complete with\n"
      "> decorator's code samples, because `make_slides.py` was copied and\n"
      "> `kind_poster` was never updated. Only looking at the image catches\n"
      "> that.\n")
    A("---\n")

    A("## 7. YouTube publication\n")
    A("[`youtube.md`](youtube.md) holds everything needed to publish, so that\n"
      "uploading is copy-and-paste rather than reconstruction. Seven sections\n"
      "are required:\n")
    if f["title"].endswith("- Explained"):
        rationale = (
            "The `- Explained` suffix is a term people actually search for, and "
            "it makes no promise the video has to keep.")
    else:
        rationale = (
            "The suffix after the dash names the worked e-commerce scenario, so "
            "the title says what the viewer will actually watch rather than only "
            "which pattern it is about.")
    A("1. **Title** — the exact string, ≤ 60 characters so search does not\n"
      "   truncate it, leading with the pattern name. Currently *\"%s\"*,\n"
      "   %d characters. %s"
      % (f["title"], len(f["title"]), rationale))
    A("2. **Description** — first two lines carry the hook, because that is what\n"
      "   shows above the fold; then what the video covers, the chapters, the\n"
      "   repository link, the prerequisites.")
    A("3. **Chapters** — `mm:ss Title`, one per scene, first entry `00:00`.\n"
      "   YouTube needs at least three and the first at zero to render them at\n"
      "   all.")
    A("4. **Tags** — comma-separated, under 500 characters.")
    A("5. **Thumbnail** — pointing at `docs/thumbnail.png`, and explaining why\n"
      "   it is not the poster.")
    A("6. **Upload checklist** — subtitles, language, thumbnail, HD processing,\n"
      "   playlist.")
    A("7. **Cards and end screen** — which video comes next in the learning\n"
      "   order. For this project: %s.\n"
      % (nxt if nxt else "none; it is last, so the end screen links back to "
                         "Simple Factory and to the playlist"))
    A("> **Requirement.** Chapter timings are generated from the built `.srt`,\n"
      "> never written by hand, by\n"
      "> `python3 ../../docs/make_youtube_docs.py %s`. They are the one part of\n"
      "> the file that goes stale silently: any change to the narration text or\n"
      "> the speaking rate invalidates every timestamp, and a chapter list that\n"
      "> is thirty seconds out is worse than none. Regenerate after any\n"
      "> rebuild.\n" % slug)
    A("Subtitles are uploaded from the generated `.srt` rather than left to\n"
      "YouTube's automatic captions, which mis-transcribe class names\n"
      "throughout.\n")
    A("---\n")

    A("## 8. Conformance\n")
    A("This project is compliant when all of the following hold. The full\n"
      "version, which governs all fourteen projects, is in\n"
      "[`video-and-publishing-spec.md`](../../../docs/video-and-publishing-spec.md)\n"
      "§9.\n")
    for x in [
        "The worked example is e-commerce.",
        "`./gradlew build` passes, and the README quotes the real "
        "`./gradlew run` output, which still matches.",
        "Scene 1 follows the four-step opening of §5.1 — what the video is, the author credit, the pattern's definition in general terms, and only then the e-commerce scenario.",
        "`RATE` is 145 and `VOICE` is Samantha.",
        "`CLEANUP` is exactly as §5.4 gives it — no `afftdn`, no `lowpass`.",
        "Per-scene audio is PCM; exactly one AAC encode, at the mux.",
        "`loudnorm` is two-pass with `linear=true`.",
        "The build prints `audio timeline continuous: N packets, no gaps`.",
        "`poster.png` shows the correct pattern name and contains no "
        "strikethrough, confirmed by looking at it.",
        "`docs/youtube.md` has all seven sections, and its chapter timings "
        "match the current `.srt`.",
        "`video/README.md` describes the pipeline as it actually is.",
    ]:
        A("- [ ] " + x)
    A("")
    if f["loudness"]:
        A("Last verified: all eleven items pass. The delivered MP4 measures %s LUFS\n"
          "integrated, %s dBTP true peak, and both streams start at 0.000.\n"
          % (f["loudness"][0], f["loudness"][1]))
    else:
        A("Last verified: all eleven items pass.\n")
    A("---\n")

    A("## 9. Rebuilding\n")
    A("From the project root:\n")
    A("```bash\n(cd video && ./build_video.sh)        # CPU-bound at CRF 18\n```\n")
    A("Then, because the narration timings will have moved:\n")
    A("```bash\npython3 ../../docs/make_youtube_docs.py %s\npython3 ../../docs/make_specs.py %s\n```\n"
      % (slug, slug))
    A("Changing the voice or the filter chain means listening to the result.\n"
      "Changing the narration text means both of the above, and re-checking the\n"
      "runtime claims in the top-level `README.md` and in `video/README.md`.\n")

    # The prose above is written with plain double hyphens so the source stays
    # editable in any editor; the published text uses real em dashes.
    return "\n".join(parts).replace(" -- ", " — ")


# ---------------------------------------------------------------------------
# Markdown -> HTML.
#
# A deliberately small converter rather than a dependency: it handles exactly
# the Markdown these specs use -- ATX headings, fenced code, tables,
# blockquotes, bullet, numbered and task lists, horizontal rules, paragraphs,
# and inline code, bold, italic and links. It is not a general Markdown
# implementation, so if a spec grows a construct that is not in that list,
# extend this rather than working around it.
# ---------------------------------------------------------------------------

CSS = """
:root {
  --bg: #0f172a; --panel: #1e293b; --panel-hi: #334155; --line: #475569;
  --text: #e2e8f0; --muted: #94a3b8; --accent: #a78bfa; --link: #38bdf8;
  --ok: #34d399;
}
* { box-sizing: border-box; }
body {
  margin: 0; padding: 0 20px 80px; background: var(--bg); color: var(--text);
  font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  font-size: 16px; line-height: 1.65;
}
main { max-width: 860px; margin: 0 auto; }
h1, h2, h3 { line-height: 1.25; }
h1 { font-size: 34px; margin: 48px 0 8px; padding-bottom: 18px;
     border-bottom: 3px solid var(--accent); }
h2 { font-size: 25px; margin: 52px 0 4px; color: var(--accent); }
h3 { font-size: 19px; margin: 32px 0 4px; }
p { margin: 14px 0; }
a { color: var(--link); }
a:hover { color: #7dd3fc; }
hr { border: 0; border-top: 1px solid var(--line); margin: 44px 0; }
code {
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, monospace;
  font-size: 0.88em; background: var(--panel); border: 1px solid var(--line);
  border-radius: 4px; padding: 1px 5px;
}
pre {
  background: var(--panel); border: 1px solid var(--line);
  border-left: 4px solid var(--accent); border-radius: 8px;
  padding: 16px 18px; overflow-x: auto;
}
pre code { background: none; border: 0; padding: 0; font-size: 14px; }
blockquote {
  margin: 20px 0; padding: 4px 20px;
  background: rgba(167, 139, 250, 0.08);
  border-left: 4px solid var(--accent); border-radius: 0 8px 8px 0;
}
table { border-collapse: collapse; width: 100%; margin: 22px 0; font-size: 15px; }
th, td { border: 1px solid var(--line); padding: 9px 12px; text-align: left;
         vertical-align: top; }
th { background: var(--panel-hi); font-weight: 600; }
tr:nth-child(even) td { background: rgba(30, 41, 59, 0.55); }
img {
  display: block; max-width: 100%; height: auto; margin: 24px auto;
  background: var(--bg); border: 1px solid var(--line); border-radius: 8px;
  padding: 10px;
}
ul, ol { margin: 14px 0; padding-left: 26px; }
li { margin: 7px 0; }
ul.task { list-style: none; padding-left: 4px; }
ul.task li::before { content: "\\2610"; color: var(--ok); font-size: 18px;
                     margin-right: 10px; }
footer {
  max-width: 860px; margin: 60px auto 0; padding-top: 20px;
  border-top: 1px solid var(--line); color: var(--muted); font-size: 14px;
}
"""


#: The Markdown files that are also published as HTML. A link to one of them
#: from inside an HTML page should land on the HTML twin rather than offering
#: the reader a Markdown file to download; every other `.md` link is left
#: alone, because those files exist only as Markdown and are read on GitHub.
HTML_TWINS = ("spec.md", "README.md")

#: Directory the Markdown currently being converted lives in. Links are
#: relative to it, so it is what a twin has to be looked for against. A
#: generator sets this before calling to_html(); left unset, no link is
#: rewritten, which is the safe answer rather than a guessed one.
LINK_BASE = None

#: Absolute paths of HTML pages that will exist by the end of the current run.
#: A generator writing a whole category in one pass registers them all up
#: front, so a link from the first page to the last is still rewritten even
#: though the last file has not been written yet.
PLANNED = set()


def href(target):
    """Point a link at its HTML twin, but only when that twin really exists.

    Not every `README.md` and `spec.md` in this repository is published as
    HTML — the category-level specs are read on GitHub and have no twin. A
    blanket rewrite sends those readers to a page that is not there, which is
    strictly worse than the Markdown file they asked for.
    """
    # Compare the file name, not the tail of the path: `video-and-publishing-
    # spec.md` ends in "spec.md" without being one.
    if LINK_BASE is None or os.path.basename(target) not in HTML_TWINS:
        return target
    twin = target[:-3] + ".html"
    full = os.path.normpath(os.path.join(LINK_BASE, twin))
    return twin if full in PLANNED or os.path.exists(full) else target


#: File types that may be embedded in a page, and the media type to announce.
EMBEDDABLE = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
              ".gif": "image/gif", ".svg": "image/svg+xml"}


def embed(src):
    """Turn an image path into a `data:` URI so the page stands on its own.

    Every HTML page this repository generates has to be self-contained: one
    file that can be mailed, copied to another machine or opened from a
    download folder and still be the whole document. The stylesheet is already
    inlined; an image referenced as `docs/images/thing.png` would be the one
    thing left that breaks the moment the page is moved away from its siblings.

    Base64 costs about a third in size on top of each PNG, which is the price
    of the guarantee. Anything remote, or missing, or not an image is left as
    written rather than guessed at.
    """
    if LINK_BASE is None or "://" in src or src.startswith("data:"):
        return src
    kind = EMBEDDABLE.get(os.path.splitext(src)[1].lower())
    path = os.path.normpath(os.path.join(LINK_BASE, src))
    if kind is None or not os.path.exists(path):
        return src
    with open(path, "rb") as f:
        return "data:%s;base64,%s" % (
            kind, base64.b64encode(f.read()).decode("ascii"))


def inline(s):
    """Inline markup: images, code spans, links, bold, italic.

    Code spans are pulled into placeholders *before* anything else runs rather
    than being converted first. These specs are full of bold and links that
    wrap a code span, and converting code first splits those across segments
    so the surrounding markup never matches and leaks into the page as literal
    asterisks and brackets.
    """
    spans = []

    def stash(m):
        spans.append(m.group(1))
        return "\x00%d\x00" % (len(spans) - 1)

    t = re.sub(r'`([^`]+)`', stash, s)
    t = html.escape(t)
    # Images before links, because an image is a link with a bang in front of
    # it and the link pattern would otherwise match the inside of one and
    # leave the bang stranded in the page.
    t = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)',
               lambda m: '<img src="%s" alt="%s">' % (embed(m.group(2)),
                                                      m.group(1)),
               t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
               lambda m: '<a href="%s">%s</a>' % (href(m.group(2)), m.group(1)),
               t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![\w*])\*([^*]+)\*(?![\w*])', r'<em>\1</em>', t)
    return re.sub(r'\x00(\d+)\x00',
                  lambda m: "<code>%s</code>" % html.escape(spans[int(m.group(1))]),
                  t)


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def to_html(md):
    lines = md.split("\n")
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]

        if ln.startswith("```"):
            body, i = [], i + 1
            while i < len(lines) and not lines[i].startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            out.append("<pre><code>%s</code></pre>" % html.escape("\n".join(body)))
            continue

        m = re.match(r'(#{1,3}) (.+)', ln)
        if m:
            lvl = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (lvl, inline(m.group(2)), lvl))
            i += 1
            continue

        if re.match(r'^---+$', ln):
            out.append("<hr>")
            i += 1
            continue

        if ln.startswith("|") and i + 1 < len(lines) \
                and re.match(r'^\|[\s:|-]+\|$', lines[i + 1]):
            head, i = cells(ln), i + 2
            body = []
            while i < len(lines) and lines[i].startswith("|"):
                body.append(cells(lines[i]))
                i += 1
            out.append(
                "<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>"
                % ("".join("<th>%s</th>" % inline(c) for c in head),
                   "".join("<tr>%s</tr>"
                           % "".join("<td>%s</td>" % inline(c) for c in r)
                           for r in body)))
            continue

        if ln.startswith(">"):
            body = []
            while i < len(lines) and lines[i].startswith(">"):
                body.append(lines[i].lstrip(">").strip())
                i += 1
            out.append("<blockquote><p>%s</p></blockquote>"
                       % inline(" ".join(x for x in body if x)))
            continue

        m = re.match(r'^(\s*)([-*]|\d+\.) (.+)', ln)
        if m:
            ordered = m.group(2)[0].isdigit()
            items, task = [], False
            while i < len(lines):
                m2 = re.match(r'^(\s*)([-*]|\d+\.) (.+)', lines[i])
                if m2:
                    text = m2.group(3)
                    if text[:4] in ("[ ] ", "[x] "):
                        task, text = True, text[4:]
                    items.append(text)
                    i += 1
                elif items and lines[i].startswith("  ") and lines[i].strip():
                    items[-1] += " " + lines[i].strip()
                    i += 1
                else:
                    break
            out.append("<%s%s>%s</%s>"
                       % ("ol" if ordered else "ul",
                          ' class="task"' if task else "",
                          "".join("<li>%s</li>" % inline(x) for x in items),
                          "ol" if ordered else "ul"))
            continue

        if ln.strip():
            para = []
            while i < len(lines) and lines[i].strip() \
                    and not lines[i].startswith(("#", ">", "|", "```")) \
                    and not re.match(r'^(\s*)([-*]|\d+\.) ', lines[i]) \
                    and not re.match(r'^---+$', lines[i]):
                para.append(lines[i].strip())
                i += 1
            out.append("<p>%s</p>" % inline(" ".join(para)))
            continue

        i += 1
    return "\n".join(out)


def wrap_html(title, body):
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<style>%s</style>
</head>
<body>
<main>
%s
</main>
<footer>
Generated from <code>spec.md</code> by <code>docs/make_specs.py</code> &mdash;
edit the generator, not this file.
</footer>
</body>
</html>
""" % (html.escape(title), CSS, body)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    measure = "--no-measure" not in sys.argv

    for group, slug in ORDER:
        if args and slug not in args:
            continue
        # ORDER lists every project the series will contain, including ones
        # not built yet. A project's META needs its real class names, so both
        # arrive together when the project does; until then, skip it quietly.
        if slug not in META or not os.path.isdir(
                os.path.join(ROOT, group, slug + "-pattern")):
            if args:
                print("%-17s not built yet — skipped" % slug)
            continue
        f = facts(group, slug, measure)
        md = build_md(group, slug, f)
        d = os.path.join(f["dir"], "docs")
        open(os.path.join(d, "spec.md"), "w").write(md)
        title = re.match(r'# (.+)', md).group(1)
        # The spec links back to its project's README and sideways to other
        # documents; resolve those against the docs directory it is written to.
        global LINK_BASE
        LINK_BASE = d
        PLANNED.add(os.path.join(d, "spec.html"))
        open(os.path.join(d, "spec.html"), "w").write(
            wrap_html(title, to_html(md)))
        print("%-17s spec.md + spec.html  (%d scenes, %s, %d tests%s)"
              % (slug, f["scenes"], f["runtime"], f["tests"],
                 ", %s LUFS" % f["loudness"][0] if f["loudness"] else ""))


if __name__ == "__main__":
    main()
