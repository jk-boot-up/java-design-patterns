"""The catalogue of design patterns this course means to cover.

Each category lists (slug, display name). A pattern counts as covered when
`gradle-java/<category>/<slug>-pattern/` exists; `PLANNED` marks the ones
being built next (docs/new-patterns-plan.md). make_index.py turns this into
docs/design-patterns-catalog.md at the repository root, so the covered and
pending lists are never edited by hand.
"""

CATEGORIES = [
    ("creational", "Creational", "How objects are made", [
        ("simple-factory", "Simple Factory"), ("static-factory", "Static Factory Method"),
        ("factory-method", "Factory Method"), ("abstract-factory", "Abstract Factory"),
        ("builder", "Builder"), ("prototype", "Prototype"), ("singleton", "Singleton"),
    ]),
    ("structural", "Structural", "How objects are put together", [
        ("adapter", "Adapter"), ("bridge", "Bridge"), ("composite", "Composite"),
        ("decorator", "Decorator"), ("facade", "Facade"), ("flyweight", "Flyweight"),
        ("proxy", "Proxy"),
    ]),
    ("behavioural", "Behavioural", "How objects share the work", [
        ("strategy", "Strategy"), ("observer", "Observer"), ("command", "Command"),
        ("template-method", "Template Method"), ("state", "State"),
        ("chain-of-responsibility", "Chain of Responsibility"), ("iterator", "Iterator"),
        ("mediator", "Mediator"), ("memento", "Memento"), ("visitor", "Visitor"),
        ("interpreter", "Interpreter"), ("table-driven-state-machine", "Table-Driven State Machine"),
        ("blackboard", "Blackboard"), ("servant", "Servant"), ("acyclic-visitor", "Acyclic Visitor"),
    ]),
    ("foundational-design-patterns", "Foundational", "Everyday idioms under the bigger patterns", [
        ("callback", "Callback"), ("delegation", "Delegation"),
        ("dependency-injection", "Dependency Injection"), ("execute-around", "Execute Around"),
        ("fluent-interface", "Fluent Interface"), ("multiton", "Multiton"),
        ("null-object", "Null Object"), ("object-pool", "Object Pool"), ("registry", "Registry"),
        ("service-locator", "Service Locator"), ("type-object", "Type Object"),
        ("immutable-object", "Immutable Object"), ("extension-object", "Extension Object"),
        ("role-object", "Role Object"), ("private-class-data", "Private Class Data"),
        ("marker-interface", "Marker Interface"), ("memoization", "Memoization"),
    ]),
    ("enterprise-design-patterns", "Enterprise Application", "Organising business logic and data access", [
        ("transaction-script", "Transaction Script"), ("service-layer", "Service Layer"),
        ("repository", "Repository"), ("data-mapper", "Data Mapper"),
        ("active-record", "Active Record"), ("unit-of-work", "Unit of Work"),
        ("identity-map", "Identity Map"), ("lazy-load", "Lazy Load"), ("dto", "Data Transfer Object"),
        ("gateway", "Gateway"), ("front-controller", "Front Controller"),
        ("optimistic-offline-lock", "Optimistic Offline Lock"),
        ("pessimistic-offline-lock", "Pessimistic Offline Lock"), ("money", "Money"),
        ("special-case", "Special Case"), ("plugin", "Plugin"), ("service-stub", "Service Stub"),
        ("query-object", "Query Object"), ("table-data-gateway", "Table Data Gateway"),
        ("single-table-inheritance", "Single Table Inheritance"),
        ("page-controller", "Page Controller"), ("remote-facade", "Remote Facade"),
    ]),
    ("domain-driven-design-patterns", "Domain-Driven Design", "Modelling the business itself", [
        ("value-object", "Value Object"), ("aggregate", "Aggregate"),
        ("domain-event", "Domain Event"), ("specification", "Specification"),
        ("bounded-context", "Bounded Context"), ("anti-corruption-layer", "Anti-Corruption Layer"),
        ("entity", "Entity"), ("domain-service", "Domain Service"),
        ("context-map", "Context Map and Shared Kernel"),
    ]),
    ("concurrency-design-patterns", "Concurrency", "Several things at once, safely", [
        ("producer-consumer", "Producer-Consumer"), ("thread-pool", "Thread Pool"),
        ("future-promise", "Future / Promise"), ("read-write-lock", "Read-Write Lock"),
        ("active-object", "Active Object"), ("monitor-object", "Monitor Object"),
        ("balking", "Balking"), ("double-checked-locking", "Double-Checked Locking"),
        ("guarded-suspension", "Guarded Suspension"), ("thread-local-storage", "Thread-Local Storage"),
        ("fork-join", "Fork-Join"), ("actor", "Actor"), ("two-phase-termination", "Two-Phase Termination"),
        ("reactor", "Reactor"), ("proactor", "Proactor"), ("half-sync-half-async", "Half-Sync/Half-Async"),
        ("leader-followers", "Leader/Followers"), ("copy-on-write", "Copy-on-Write"),
        ("compare-and-swap", "Lock-Free Compare-and-Swap"), ("scheduler", "Scheduler"),
    ]),
    ("architectural-design-patterns", "Architectural", "The shape of a whole application", [
        ("layered-architecture", "Layered Architecture"), ("mvc", "Model-View-Controller"),
        ("mvp-and-mvvm", "MVP and MVVM"), ("hexagonal-architecture", "Hexagonal Architecture"),
        ("onion-architecture", "Onion Architecture"), ("clean-architecture", "Clean Architecture"),
        ("pipe-and-filter-architecture", "Pipe-and-Filter Architecture"), ("microkernel", "Microkernel"),
        ("event-driven-architecture", "Event-Driven Architecture"), ("serverless", "Serverless"),
        ("modular-monolith", "Modular Monolith"), ("micro-frontends", "Micro-Frontends"),
        ("broker", "Broker"), ("space-based", "Space-Based Architecture"),
        ("cell-based", "Cell-Based Architecture"),
    ]),
    ("messaging-integration-patterns", "Messaging and Integration", "Systems that talk by messages", [
        ("message-channel", "Message Channel"), ("content-based-router", "Content-Based Router"),
        ("splitter-aggregator", "Splitter and Aggregator"), ("dead-letter-channel", "Dead Letter Channel"),
        ("event-bus", "Event Bus"), ("content-enricher", "Content Enricher"),
        ("message-translator", "Message Translator / Normalizer"), ("message-filter", "Message Filter"),
        ("recipient-list", "Recipient List"), ("wire-tap", "Wire Tap"), ("resequencer", "Resequencer"),
        ("request-reply", "Request-Reply with Correlation Identifier"),
        ("process-manager", "Process Manager"), ("routing-slip", "Routing Slip"),
        ("polling-consumer", "Polling Consumer"), ("guaranteed-delivery", "Guaranteed Delivery"),
    ]),
    ("micro-services-design-patterns", "Microservices", "Many small services that stay reliable", [
        ("api-gateway", "API Gateway"), ("api-composition", "API Composition"),
        ("service-discovery", "Service Discovery"), ("load-balancing", "Load Balancing"),
        ("circuit-breaker", "Circuit Breaker"), ("retry", "Retry with Backoff"),
        ("bulkhead", "Bulkhead"), ("timeout", "Timeout"), ("rate-limiter", "Rate Limiter"),
        ("saga", "Saga"), ("cqrs", "CQRS"), ("database-per-service", "Database per Service"),
        ("transactional-outbox", "Transactional Outbox"), ("idempotent-consumer", "Idempotent Consumer"),
        ("cache-aside", "Cache-Aside"), ("queue-based-load-leveling", "Queue-Based Load Leveling"),
        ("competing-consumers", "Competing Consumers"), ("claim-check", "Claim Check"),
        ("leader-election", "Leader Election"), ("publisher-subscriber", "Publisher-Subscriber"),
        ("pipes-and-filters", "Pipes and Filters"), ("scatter-gather", "Scatter-Gather"),
        ("materialized-view", "Materialized View"), ("async-request-reply", "Asynchronous Request-Reply"),
        ("health-endpoint-monitoring", "Health Endpoint Monitoring"), ("write-behind-cache", "Write-Behind Cache"),
        ("write-through-cache", "Write-Through Cache"), ("sharding", "Sharding"), ("valet-key", "Valet Key"),
        ("priority-queue", "Priority Queue"), ("backpressure", "Backpressure"),
        ("hedged-requests", "Hedged Requests"), ("gateway-offloading", "Gateway Offloading"),
        ("event-carried-state-transfer", "Event-Carried State Transfer"),
    ]),
    ("platform-design-patterns", "Platform", "Shipping, running and operating software", [
        ("externalised-configuration", "Externalised Configuration"), ("feature-toggle", "Feature Toggle"),
        ("blue-green-and-canary", "Blue-Green and Canary"), ("strangler-fig", "Strangler Fig"),
        ("sidecar", "Sidecar"), ("service-mesh", "Service Mesh"),
        ("distributed-tracing", "Distributed Tracing"), ("consumer-driven-contract", "Consumer-Driven Contract"),
        ("backends-for-frontends", "Backends for Frontends"), ("event-sourcing", "Event Sourcing"),
    ]),
    ("testing-design-patterns", "Testing", "Making code easy to test and tests easy to read", [
        ("test-double", "Test Double (dummy, stub, spy, mock, fake)"),
        ("object-mother", "Object Mother / Test Data Builder"), ("page-object", "Page Object"),
        ("contract-stub", "Contract Stub"),
    ]),
    ("security-design-patterns", "Security", "Who may do what, and how you know", [
        ("authorization-policy", "Authorization Policy (RBAC / ABAC)"),
        ("token-authentication", "Token-Based Authentication (JWT)"), ("secure-gateway", "Secure Gateway"),
        ("secrets-manager", "Secrets Manager"), ("input-validation", "Input Validation Pipeline"),
    ]),
    ("functional-design-patterns", "Functional", "Functional style in modern Java", [
        ("railway-oriented", "Railway-Oriented Programming (Optional / Either)"),
        ("higher-order-functions", "Higher-Order Functions"), ("currying", "Currying"),
        ("lenses", "Lenses for Immutable Updates"),
    ]),
]

#: Being built now, in this order (docs/new-patterns-plan.md).
PLANNED = [
    "money", "test-double", "content-enricher", "materialized-view", "async-request-reply",
    "health-endpoint-monitoring", "write-behind-cache", "immutable-object",
    "table-driven-state-machine", "modular-monolith",
]
