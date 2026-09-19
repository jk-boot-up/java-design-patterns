#!/usr/bin/env python3
"""Generate `docs/youtube.md` for every pattern project.

The file it writes is the one described in section 8 of
`video-and-publishing-spec.md`: everything needed to publish a video, in
copy-and-paste form, so that uploading is not an exercise in reconstructing
the title and the chapter list from memory.

Chapter timings are derived, not stored. Each project's `.srt` is the
authoritative timing record — it was generated from the *encoded* scene
clips, so it already accounts for frame alignment. This script re-splits
each scene's narration exactly the way `make_subtitles.py` did, counts how
many cues each scene produced, and reads the start timestamp of the first
cue of each scene out of the SRT. That means a chapter list can never drift
from the video as long as the SRT was regenerated with it, and it means this
script can be re-run at any time without a build.

Usage:
    python3 docs/make_youtube_docs.py            # all projects
    python3 docs/make_youtube_docs.py proxy      # one project
"""

import importlib.util
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_URL = "https://github.com/jk-boot-up/java-design-patterns"

# The learning order used by the written docs. It is deliberately NOT used
# for the end screen: publishing order is not build order, so no video
# names its successor.
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
    # Spring, and each version is a project of its own.
    ("architectural-design-patterns", "layered-architecture"),
    ("architectural-design-patterns", "mvc"),
    ("architectural-design-patterns", "hexagonal-architecture"),
    ("architectural-design-patterns", "clean-architecture"),
    ("architectural-design-patterns", "clean-architecture-with-spring"),
    # The concurrency category. A dependency order: the queue, what consumes
    # it, how a caller gets an answer back, the two ways shared state is
    # protected, and the capstone that assembles all four.
    ("concurrency-design-patterns", "producer-consumer"),
    ("concurrency-design-patterns", "thread-pool"),
    ("concurrency-design-patterns", "future-promise"),
    ("concurrency-design-patterns", "read-write-lock"),
    ("concurrency-design-patterns", "monitor-object"),
    ("concurrency-design-patterns", "active-object"),
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
    ("foundational-design-patterns", "null-object"),
    ("foundational-design-patterns", "object-pool"),
    ("foundational-design-patterns", "registry"),
    ("foundational-design-patterns", "service-locator"),
    ("foundational-design-patterns", "dependency-injection"),
    ("foundational-design-patterns", "dependency-injection-with-spring"),
    ("foundational-design-patterns", "registry-with-spring"),
    ("foundational-design-patterns", "object-pool-with-hikaricp"),
    ("foundational-design-patterns", "service-locator-with-consul"),
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
    ("architectural-design-patterns", "layered-architecture-with-spring-boot"),
    ("architectural-design-patterns", "mvc-with-spring-mvc"),
    ("architectural-design-patterns", "hexagonal-architecture-with-spring-boot"),
]

# Per-project title and tag material. The title is what gets pasted into
# YouTube verbatim and is kept under 60 characters so search results do not
# truncate it; it leads with the pattern name because that is what people
# type into the search box.
META = {
    "simple-factory": {
        "title": "Simple Factory Pattern in Java - Payment Methods",
        "tags": ["simple factory pattern", "factory pattern java", "payment methods"],
    },
    "static-factory": {
        "title": "Static Factory Methods in Java - Named Constructors",
        "tags": ["static factory method", "named constructor java", "effective java"],
    },
    "factory-method": {
        "title": "Factory Method Pattern in Java - Delivery Tiers",
        "tags": ["factory method pattern", "template method", "shipping"],
    },
    "abstract-factory": {
        "title": "Abstract Factory in Java - A Regional Checkout",
        "tags": ["abstract factory pattern", "product family", "localisation"],
    },
    "builder": {
        "title": "Builder Pattern in Java - Building a Purchase Order",
        "tags": ["builder pattern", "fluent api java", "telescoping constructor"],
    },
    "prototype": {
        "title": "Prototype Pattern in Java - Cloning Product Listings",
        "tags": ["prototype pattern", "deep copy java", "clone"],
    },
    "singleton": {
        "title": "Singleton Pattern in Java - Order Number Sequencer",
        "tags": ["singleton pattern", "enum singleton", "thread safe singleton"],
    },
    "adapter": {
        "title": "Adapter Pattern in Java - Wrapping a Shipping SDK",
        "tags": ["adapter pattern", "wrapper class java", "third party sdk"],
    },
    "bridge": {
        "title": "Bridge Pattern in Java - Notifications and Channels",
        "tags": ["bridge pattern", "class explosion", "composition over inheritance"],
    },
    "composite": {
        "title": "Composite Pattern in Java - Nested Category Trees",
        "tags": ["composite pattern", "tree structure java", "recursion"],
    },
    "decorator": {
        "title": "Decorator Pattern in Java - Gift Wrap and Insurance",
        "tags": ["decorator pattern", "wrapper java", "open closed principle"],
    },
    "facade": {
        "title": "Facade Pattern in Java - One Call to Place an Order",
        "tags": ["facade pattern", "subsystem java", "api design"],
    },
    "flyweight": {
        "title": "Flyweight Pattern in Java - Sharing Badge Styles",
        "tags": ["flyweight pattern", "memory optimisation java", "object pooling"],
    },
    "proxy": {
        "title": "Proxy Pattern in Java - Lazy and Guarded Images",
        "tags": ["proxy pattern", "virtual proxy", "protection proxy", "lazy loading"],
    },
    "strategy": {
        "title": "Strategy Pattern in Java - Shipping Rules",
        "tags": ["strategy pattern", "interchangeable algorithms", "shipping calculation"],
    },
    "observer": {
        "title": "Observer Pattern in Java - Order Status Events",
        "tags": ["observer pattern", "event driven java", "publish subscribe"],
    },
    "command": {
        "title": "Command Pattern in Java - Undoable Cart Edits",
        "tags": ["command pattern", "undo redo java", "shopping cart"],
    },
    "template-method": {
        "title": "Template Method Pattern in Java - Fulfilment Steps",
        "tags": ["template method pattern", "workflow java", "inheritance hooks"],
    },
    "state": {
        "title": "State Pattern in Java - The Order Lifecycle",
        "tags": ["state pattern", "state machine java", "order lifecycle"],
    },
    "chain-of-responsibility": {
        "title": "Chain of Responsibility in Java - Checkout Screening",
        "tags": ["chain of responsibility", "handler chain java", "validation pipeline"],
    },
    "iterator": {
        "title": "Iterator Pattern in Java - Paging the Catalog",
        "tags": ["iterator pattern", "iterable java", "lazy pagination"],
    },
    "mediator": {
        "title": "Mediator Pattern in Java - The Checkout Page",
        "tags": ["mediator pattern", "decoupling components", "checkout ui"],
    },
    "memento": {
        "title": "Memento Pattern in Java - Restoring a Saved Cart",
        "tags": ["memento pattern", "snapshot undo java", "encapsulation"],
    },
    "visitor": {
        "title": "Visitor Pattern in Java - Catalog Reports",
        "tags": ["visitor pattern", "double dispatch java", "tree traversal"],
    },
    "interpreter": {
        "title": "Interpreter Pattern in Java - Promotion Rules",
        "tags": ["interpreter pattern", "expression tree java", "rules engine"],
    },
    "api-gateway": {
        "title": "API Gateway in Java - One Front Door for the Store",
        "tags": ["api gateway pattern", "microservices java", "backend for frontend"],
    },
    "service-discovery": {
        "title": "Service Discovery in Java - Finding a Live Instance",
        "tags": ["service discovery", "service registry", "microservices java"],
    },
    "load-balancing": {
        "title": "Client-Side Load Balancing in Java - Catalog Reads",
        "tags": ["load balancing", "round robin java", "microservices java"],
    },
    "retry": {
        "title": "Retry with Backoff in Java - A Flaky Payment Gateway",
        "tags": ["retry pattern", "exponential backoff java", "resilience"],
    },
    "circuit-breaker": {
        "title": "Circuit Breaker in Java - When a Service Stops",
        "tags": ["circuit breaker pattern", "resilience4j", "fault tolerance java"],
    },
    "bulkhead": {
        "title": "Bulkhead Pattern in Java - Isolating a Slow Job",
        "tags": ["bulkhead pattern", "thread pool isolation", "resilience java"],
    },
    "database-per-service": {
        "title": "Database per Service in Java - Losing the Join",
        "tags": ["database per service", "microservices data", "bounded context"],
    },
    "api-composition": {
        "title": "API Composition in Java - The Order Details Page",
        "tags": ["api composition", "microservices query", "parallel fanout java"],
    },
    "cqrs": {
        "title": "CQRS in Java - Order History Without the Joins",
        "tags": ["cqrs pattern", "read model java", "event driven"],
    },
    "saga": {
        "title": "Saga Pattern in Java - Placing an Order, Safely",
        "tags": ["saga pattern", "compensating transaction", "distributed transaction"],
    },
    "transactional-outbox": {
        "title": "Transactional Outbox in Java - Never Lose an Event",
        "tags": ["transactional outbox", "dual write problem", "event publishing"],
    },
    "idempotent-consumer": {
        "title": "Idempotent Consumer in Java - The Duplicate Message",
        "tags": ["idempotent consumer", "exactly once java", "message deduplication"],
    },
    "externalised-configuration": {
        "title": "Externalised Configuration in Java - No Deploy Needed",
        "tags": ["externalised configuration", "feature flags java", "twelve factor app"],
    },
    "distributed-tracing": {
        "title": "Distributed Tracing in Java - Which Service Is Slow?",
        "tags": ["distributed tracing", "observability java", "trace id propagation"],
    },
    "backends-for-frontends": {
        "title": "Backends for Frontends in Java - One Shape Won't Fit",
        "tags": ["backends for frontends", "bff pattern", "api design java"],
    },
    "sidecar": {
        "title": "Sidecar Pattern in Java - Retry Code Moves Out",
        "tags": ["sidecar pattern", "service mesh java", "nginx proxy"],
    },
    "sidecar-java-proxy": {
        "title": "Sidecar in Java - Swapping the Proxy, Not the Service",
        "tags": ["sidecar pattern", "java proxy server", "polyglot microservices"],
    },
    "sidecar-on-kubernetes": {
        "title": "Sidecar on Kubernetes - Two Containers, One Pod",
        "tags": ["kubernetes sidecar", "kubernetes pod", "kind cluster"],
    },
    "event-sourcing": {
        "title": "Event Sourcing in Java - Why Is This Balance 140?",
        "tags": ["event sourcing", "append only log java", "loyalty points"],
    },
    "strangler-fig": {
        "title": "Strangler Fig in Java - Replacing Legacy Safely",
        "tags": ["strangler fig pattern", "legacy migration", "incremental rewrite"],
    },
    "layered-architecture": {
        "title": "Layered Architecture in Java - The One Call That Ruins It",
        "tags": ["layered architecture", "n tier architecture", "archunit"],
    },
    "mvc": {
        "title": "MVC in Java - The View That Knew Too Much",
        "tags": ["mvc pattern", "model view controller", "mvp and mvvm"],
    },
    "hexagonal-architecture": {
        "title": "Hexagonal Architecture in Java - Ports and Adapters",
        "tags": ["hexagonal architecture", "ports and adapters", "archunit"],
    },
    "clean-architecture": {
        "title": "Clean Architecture in Java - Which Way Does It Point?",
        "tags": ["clean architecture", "dependency inversion", "dependency rule"],
    },
    "clean-architecture-with-spring": {
        "title": "Clean Architecture with Spring - Who Wires the Graph?",
        "tags": ["clean architecture spring", "spring boot 4", "dependency injection"],
    },
    "producer-consumer": {
        "title": "Producer-Consumer in Java - The Bounded Queue",
        "tags": ["producer consumer pattern", "java concurrency", "blockingqueue"],
    },
    "thread-pool": {
        "title": "Thread Pool in Java - A Thread Per Order, Until It Isn't",
        "tags": ["thread pool pattern", "java executor", "virtual threads"],
    },
    "future-promise": {
        "title": "Future and Promise in Java - The Answer You Don't Have Yet",
        "tags": ["future promise pattern", "completablefuture", "java async"],
    },
    "read-write-lock": {
        "title": "Read-Write Lock in Java - A Thousand Readers, One Writer",
        "tags": ["read write lock", "java concurrency", "reentrantreadwritelock"],
    },
    "monitor-object": {
        "title": "Monitor Object in Java - The Object That Guards Itself",
        "tags": ["monitor object pattern", "java synchronized", "wait notify"],
    },
    "active-object": {
        "title": "Active Object in Java - A Call That Returns Before It's Done",
        "tags": ["active object pattern", "java concurrency", "actor model"],
    },
    "data-mapper": {
        "title": "Data Mapper in Java - The Object That Is Not A Row",
        "tags": ["data mapper pattern", "active record", "java persistence"],
    },
    "identity-map": {
        "title": "Identity Map in Java - One Row, One Object",
        "tags": ["identity map pattern", "java persistence", "object identity"],
    },
    "unit-of-work": {
        "title": "Unit of Work in Java - All Of The Order Or None",
        "tags": ["unit of work pattern", "java transactions", "persistence"],
    },
    "lazy-load": {
        "title": "Lazy Load in Java - One Order, Twenty-One Queries",
        "tags": ["lazy load pattern", "n+1 query problem", "java persistence"],
    },
    "repository": {
        "title": "Repository in Java - Query The Collection, Not The Table",
        "tags": ["repository pattern", "java repository", "domain driven design"],
    },
    "service-layer": {
        "title": "Service Layer in Java - Where Does Placing An Order Live?",
        "tags": ["service layer pattern", "java service layer", "anemic domain model"],
    },
    "dto": {
        "title": "DTO in Java - The Object That Crosses The Boundary",
        "tags": ["dto pattern", "data transfer object", "java rest"],
    },
    "identity-map-with-jpa": {
        "title": "Identity Map with JPA - Why == Is True",
        "tags": ["identity map jpa", "persistence context", "hibernate"],
    },
    "unit-of-work-with-spring": {
        "title": "Unit of Work with Spring - The Flush You Did Not Write",
        "tags": ["transactional spring", "unit of work spring", "spring boot 4"],
    },
    "lazy-load-with-hibernate": {
        "title": "LazyInitializationException Explained in Hibernate",
        "tags": ["lazyinitializationexception", "hibernate lazy loading", "n+1"],
    },
    "repository-with-spring-data": {
        "title": "Spring Data Repository - An Interface With No Implementation",
        "tags": ["spring data jpa", "jparepository", "repository pattern spring"],
    },
    "null-object": {
        "title": "Null Object in Java - The Discount That Is Not There",
        "tags": ["null object pattern", "java optional", "nullpointerexception"],
    },
    "object-pool": {
        "title": "Object Pool in Java - When Pooling Makes It Slower",
        "tags": ["object pool pattern", "connection pool", "java performance"],
    },
    "registry": {
        "title": "Registry in Java - A Global Variable With Better Manners",
        "tags": ["registry pattern", "global state", "java singleton"],
    },
    "service-locator": {
        "title": "Service Locator in Java - Why It Is Called An Anti-Pattern",
        "tags": ["service locator pattern", "anti-pattern", "serviceloader"],
    },
    "dependency-injection": {
        "title": "Dependency Injection in Java - Without Spring, First",
        "tags": ["dependency injection", "constructor injection", "java di"],
    },
    "dependency-injection-with-spring": {
        "title": "Dependency Injection with Spring - Recognise The Wiring",
        "tags": ["spring dependency injection", "spring boot", "constructor injection"],
    },
    "registry-with-spring": {
        "title": "Spring's Registry - The Context And Its Shared State",
        "tags": ["spring applicationcontext", "beanfactory", "spring test context caching"],
    },
    "object-pool-with-hikaricp": {
        "title": "Object Pool with HikariCP - The Mature Answer",
        "tags": ["hikaricp", "connection pool", "java database"],
    },
    "service-locator-with-consul": {
        "title": "Service Locator with Consul - Real Service Discovery",
        "tags": ["consul service discovery", "service locator", "microservices"],
    },
    "thread-pool-with-spring": {
        "title": "Thread Pool with Spring - The Executor Behind @Async",
        "tags": ["spring async", "threadpooltaskexecutor", "java thread pool"],
    },
    "future-promise-with-spring": {
        "title": "Future and Promise with Spring - What @Async Loses",
        "tags": ["spring completablefuture", "async exception", "spring async"],
    },
    "active-object-with-spring": {
        "title": "Active Object with Spring - One Thread, One Mailbox",
        "tags": ["active object spring", "actor model java", "spring async"],
    },
    "singleton-with-spring": {
        "title": "Singleton with Spring - One Per Container, Not Per JVM",
        "tags": ["spring singleton scope", "spring beans", "singleton pattern"],
    },
    "prototype-with-spring": {
        "title": "Prototype with Spring - The Prototype That Is Not New",
        "tags": ["spring prototype scope", "objectprovider", "prototype pattern"],
    },
    "proxy-with-spring": {
        "title": "Proxy with Spring - The Call That Skips The Proxy",
        "tags": ["spring aop", "spring proxy", "cglib proxy"],
    },
    "observer-with-spring": {
        "title": "Observer with Spring - Events, And Who Runs Them",
        "tags": ["spring events", "eventlistener", "observer pattern"],
    },
    "strategy-with-spring": {
        "title": "Strategy with Spring - Let The Container Hold Them",
        "tags": ["spring strategy pattern", "dependency injection", "strategy pattern"],
    },
    "template-method-with-spring": {
        "title": "Template Method with Spring - Inside JdbcTemplate",
        "tags": ["jdbctemplate", "template method pattern", "spring jdbc"],
    },
    "chain-of-responsibility-with-spring": {
        "title": "Chain of Responsibility with Spring - Filters In Order",
        "tags": ["spring filter chain", "oncepertequestfilter", "chain of responsibility"],
    },
    "interpreter-with-spel": {
        "title": "Interpreter with SpEL - Expressions You Did Not Write",
        "tags": ["spring expression language", "spel", "interpreter pattern"],
    },
    "circuit-breaker-with-resilience4j": {
        "title": "Circuit Breaker with Resilience4j - Real Defaults",
        "tags": ["resilience4j circuit breaker", "spring boot resilience", "circuit breaker"],
    },
    "retry-with-resilience4j": {
        "title": "Retry with Resilience4j - Backoff, Jitter And Order",
        "tags": ["resilience4j retry", "exponential backoff", "spring retry"],
    },
    "bulkhead-with-resilience4j": {
        "title": "Bulkhead with Resilience4j - Two Kinds Of Wall",
        "tags": ["resilience4j bulkhead", "spring boot", "bulkhead pattern"],
    },
    "api-gateway-with-spring-cloud-gateway": {
        "title": "API Gateway with Spring Cloud Gateway - Real Routes",
        "tags": ["spring cloud gateway", "api gateway", "reactive gateway"],
    },
    "load-balancing-with-spring-cloud-loadbalancer": {
        "title": "Load Balancing with Spring Cloud LoadBalancer",
        "tags": ["spring cloud loadbalancer", "client side load balancing", "load balancer"],
    },
    "service-discovery-with-spring-cloud-consul": {
        "title": "Service Discovery with Spring Cloud Consul",
        "tags": ["spring cloud consul", "service discovery", "consul health checks"],
    },
    "value-object": {
        "title": "Value Object",
        "tags": ['value object', 'ddd value object', 'java record', 'immutable object'],
    },
    "aggregate": {
        "title": "Aggregate",
        "tags": ['aggregate', 'ddd aggregate', 'aggregate root', 'domain driven design'],
    },
    "domain-event": {
        "title": "Domain Event",
        "tags": ['domain event', 'ddd domain event', 'event driven', 'domain driven design'],
    },
    "layered-architecture-with-spring-boot": {
        "title": "Layered Architecture with Spring Boot - Layers That Hold",
        "tags": ["spring boot layered architecture", "layered architecture", "archunit"],
    },
    "mvc-with-spring-mvc": {
        "title": "MVC with Spring MVC - What The Framework Adds",
        "tags": ["spring mvc", "model view controller", "thymeleaf"],
    },
    "hexagonal-architecture-with-spring-boot": {
        "title": "Hexagonal Architecture with Spring Boot",
        "tags": ["hexagonal architecture", "ports and adapters", "spring boot"],
    },
}

COMMON_TAGS = [
    "design patterns", "java design patterns", "gang of four", "java 21",
    "software design", "clean code", "object oriented design",
    "java tutorial", "ecommerce", "programming tutorial",
]


def load_scenes(video_dir):
    """Import a project's scenes.py without letting the 14 shadow each other."""
    path = os.path.join(video_dir, "scenes.py")
    spec = importlib.util.spec_from_file_location("scenes_" + video_dir, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.SCENES


def load_subtitle_splitter(video_dir):
    """Reuse the project's own cue splitter, so the counts match its SRT."""
    path = os.path.join(video_dir, "make_subtitles.py")
    src = open(path).read()
    ns = {"__name__": "not_main"}
    sys.path.insert(0, video_dir)
    try:
        exec(compile(src, path, "exec"), ns)
    finally:
        sys.path.pop(0)
    return ns["split_cues"]


def _clock(h, mi, s, ms):
    return h * 3600 + mi * 60 + s + ms / 1000.0


def srt_times(srt_path):
    """Every cue as a (start, end) pair, in order, in seconds."""
    times = []
    pat = (r"(\d\d):(\d\d):(\d\d),(\d\d\d) --> "
           r"(\d\d):(\d\d):(\d\d),(\d\d\d)")
    for line in open(srt_path):
        m = re.match(pat, line.strip())
        if m:
            g = [int(x) for x in m.groups()]
            times.append((_clock(*g[:4]), _clock(*g[4:])))
    return times


def srt_starts(srt_path):
    return [t[0] for t in srt_times(srt_path)]


def mmss(seconds):
    total = int(seconds)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return "%d:%02d:%02d" % (h, m, s) if h else "%02d:%02d" % (m, s)


def chapters(video_dir, slug):
    """`mm:ss Title` per scene, first entry forced to 00:00."""
    scenes = load_scenes(video_dir)
    split_cues = load_subtitle_splitter(video_dir)
    starts = srt_starts(os.path.join(video_dir, slug + "-pattern-explained.srt"))

    lines, cursor = [], 0
    for i, scene in enumerate(scenes):
        if cursor >= len(starts):
            break
        t = 0.0 if i == 0 else starts[cursor]
        # The opening scene is the title card. Its slide title is the name of
        # the pattern, which repeats later when the pattern itself is defined;
        # two identically named chapters are no help to anyone skimming the
        # list, so the first one says what it actually is.
        name = "Introduction" if i == 0 else scene["title"]
        lines.append("%s %s" % (mmss(t), name))
        cursor += len(split_cues(scene["narration"]))
    return lines


def suggested_description(video_dir):
    """Lift the blockquote the project's video/README.md already carries."""
    readme = open(os.path.join(video_dir, "README.md")).read()
    m = re.search(r"Suggested description:\n\n((?:> .*\n)+)", readme)
    if not m:
        return None
    body = " ".join(l[2:].strip() for l in m.group(1).strip().splitlines())
    return re.sub(r"\s+", " ", body).strip()


def runtime(video_dir, slug):
    """The end of the last caption -- the last cue's *start* would undercount
    the final scene by the length of its closing sentence."""
    times = srt_times(os.path.join(video_dir, slug + "-pattern-explained.srt"))
    return mmss(times[-1][1]) if times else "?"


def next_video(slug):
    slugs = [s for _, s in ORDER]
    i = slugs.index(slug)
    return slugs[i + 1] if i + 1 < len(slugs) else None


def write_doc(group, slug):
    project = os.path.join(ROOT, group, slug + "-pattern")
    video_dir = os.path.join(project, "video")
    meta = META[slug]
    title = meta["title"]
    assert len(title) <= 60, "%s title is %d chars" % (slug, len(title))

    chaps = chapters(video_dir, slug)
    desc = suggested_description(video_dir)
    tags = meta["tags"] + COMMON_TAGS
    tag_line = ", ".join(tags)
    assert len(tag_line) < 500, "%s tags are %d chars" % (slug, len(tag_line))

    # `.title()` is right for "load balancing" and wrong for "api" and
    # "cqrs", which are read out letter by letter and are written that way
    # everywhere else in the repository.
    ACRONYMS = {"api": "API", "cqrs": "CQRS"}
    pretty = " ".join(ACRONYMS.get(w, w.title()) for w in slug.split("-"))
    rel = os.path.join(group, slug + "-pattern")

    out = ["# YouTube — %s Pattern\n" % pretty]
    out.append(
        "Everything needed to publish `video/%s-pattern-explained.mp4`. "
        "Copy the fields straight out of this file.\n" % slug
    )
    out.append("Chapter timings are generated from the video's `.srt`. "
               "Re-run `python3 docs/make_youtube_docs.py %s` after any "
               "change to the narration, or they will be wrong.\n" % slug)

    out.append("## Title\n")
    out.append("```\n%s\n```\n" % title)
    out.append("%d characters — under the 60 YouTube shows before "
               "truncating in search results.\n" % len(title))

    out.append("## Description\n")
    out.append("The first two lines are what a viewer sees above the fold, "
               "so they carry the hook rather than the boilerplate.\n")
    out.append("```")
    if desc:
        out.append(desc + "\n")
    out.append("CHAPTERS")
    out.extend(chaps)
    out.append("")
    out.append("SOURCE CODE, WRITTEN NOTES AND AN INTERACTIVE ANIMATION")
    out.append("%s/tree/main/gradle-java/%s" % (REPO_URL, rel))
    out.append("")
    out.append("WHAT YOU NEED FIRST")
    out.append("Java 21 and a working knowledge of classes and interfaces. "
               "No prior design-pattern knowledge is assumed. The full "
               "prerequisites are in docs/prerequisites.md in the "
               "repository.")
    out.append("```\n")

    out.append("## Chapters\n")
    out.append("YouTube renders these as chapters only if there are at least "
               "three and the first is at `00:00`.\n")
    out.append("```")
    out.extend(chaps)
    out.append("```\n")

    out.append("## Tags\n")
    out.append("```\n%s\n```\n" % tag_line)
    out.append("%d characters, under YouTube's 500 limit.\n" % len(tag_line))

    out.append("## Thumbnail\n")
    out.append("![Thumbnail](thumbnail.png)\n")
    out.append("**Upload `docs/thumbnail.png`** — 1280×720, the size YouTube "
               "recommends, generated by `docs/make_thumbnails.py`. It is "
               "deliberately not the same image as the video's opening "
               "frame: a thumbnail is judged at about 360 pixels wide in a "
               "search result, so this one carries only the pattern name, "
               "one line of promise and one short piece of code, each set "
               "large enough to survive the shrink.\n")
    out.append("`video/poster.png` is the 1920×1080 opening frame, produced "
               "by the video build. It stays in the repository as the title "
               "card; it is not what gets uploaded.\n")
    out.append("YouTube will not pick the thumbnail up on its own — upload "
               "it under **Details → Thumbnail → Upload file**. A custom "
               "thumbnail requires a verified channel.\n")

    out.append("## Upload checklist\n")
    out.append("- [ ] Upload `video/%s-pattern-explained.mp4` "
               "(1080p, H.264, 30 fps, AAC 48 kHz — already YouTube's "
               "recommended settings, no re-encode needed)" % slug)
    out.append("- [ ] Set the video language to **English** first, or the "
               "subtitle option may not appear")
    out.append("- [ ] Add subtitles: *Video elements → Add subtitles → "
               "Upload file → With timing* → `video/%s-pattern-explained.srt`"
               % slug)
    out.append("- [ ] Upload `docs/thumbnail.png` as the thumbnail — do not "
               "let YouTube auto-pick a frame")
    out.append("- [ ] Paste the title, description and tags from above")
    out.append("- [ ] Add to the **Java Design Patterns** playlist, in "
               "learning order")
    out.append("- [ ] Wait for 1080p processing before sharing the link — "
               "code slides are unreadable at 360p\n")

    out.append("## Cards and end screen\n")
    # Deliberately not naming a successor. Publishing order is not the build
    # order, so the end screen is set at upload time to whatever actually went
    # up next; unlike the video itself, it can be changed afterwards.
    out.append("End screen links to whichever pattern video goes up next — "
               "set it at upload time rather than assuming an order.\n")
    out.append("Add a card partway through pointing at the playlist, so a "
               "viewer who arrives at this pattern from search can find the "
               "rest of the series.\n")

    out.append("## Runtime\n")
    out.append("Approximately %s, narrated at 145 words per minute.\n"
               % runtime(video_dir, slug))

    path = os.path.join(project, "docs", "youtube.md")
    open(path, "w").write("\n".join(out))
    print("wrote %s  (%d chapters)" % (
        os.path.relpath(path, ROOT), len(chaps)))


def main():
    wanted = sys.argv[1:]
    for group, slug in ORDER:
        if wanted and slug not in wanted:
            continue
        # ORDER lists the whole series, including projects not built yet.
        if not os.path.isdir(os.path.join(ROOT, group, slug + "-pattern")):
            if wanted:
                print("%s: not built yet - skipped" % slug)
            continue
        write_doc(group, slug)


if __name__ == "__main__":
    main()
