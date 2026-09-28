# Rollout Report

Progress of bringing every project into line with [`AUDIO-VIDEO-SPEC.md`](AUDIO-VIDEO-SPEC.md). Updated automatically by `tools/videokit/videokit.sh rollout`; last update 2026-09-28 22:06.

| Stage | Done | Queued | Failed | Pending | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| Narration rewritten (simple, audio-first, third-person credit) | 170 | 0 | 0 | 0 | 170 |
| Video + audio rebuilt with the sample 03 voice | 114 | 56 | 0 | 0 | 170 |
| Animation narration + step play/pause, self-contained | 119 | 0 | 0 | 51 | 170 |
| Version `amy-slow` (video + audio + animation, main build kept) | 170 | 0 | 0 | 0 | 170 |

**114 of 170 projects complete, 56 remaining.**


## architectural-design-patterns

| Project | Script | Video | Animation | Note |
| --- | :---: | :---: | :---: | --- |
| clean-architecture | ✅ | ✅ | ✅ | 10:18 runtime |
| clean-architecture-with-spring | ✅ | ✅ | ✅ | 7:54 runtime |
| event-driven-architecture | ✅ | ✅ | ✅ | 5:36 runtime |
| event-driven-architecture-with-kafka | ✅ | ✅ | ✅ | 6:46 runtime |
| hexagonal-architecture | ✅ | ✅ | ✅ | 9:07 runtime |
| hexagonal-architecture-with-spring-boot | ✅ | ✅ | ✅ | 5:49 runtime |
| layered-architecture | ✅ | ✅ | ✅ | 10:53 runtime |
| layered-architecture-with-spring-boot | ✅ | ✅ | ✅ | 6:08 runtime |
| microkernel | ✅ | ✅ | ✅ | 5:37 runtime |
| mvc | ✅ | ✅ | ✅ |  |
| mvc-with-spring-mvc | ✅ | ✅ | ✅ | 5:36 runtime |
| mvp-and-mvvm | ✅ | ✅ | ✅ | 5:57 runtime |
| onion-architecture | ✅ | ✅ | ✅ | 5:58 runtime |
| pipe-and-filter-architecture | ✅ | ✅ | ✅ | 5:50 runtime |
| serverless | ✅ | ✅ | ✅ | 5:48 runtime |
| serverless-with-localstack | ✅ | ✅ | ✅ | 6:26 runtime |

## behavioural

| Project | Script | Video | Animation | Note |
| --- | :---: | :---: | :---: | --- |
| chain-of-responsibility | ✅ | ✅ | ✅ | 11:39 runtime |
| chain-of-responsibility-with-spring | ✅ | ✅ | ✅ | 5:40 runtime |
| command | ✅ | ✅ | ✅ | 11:24 runtime |
| interpreter | ✅ | ✅ | ✅ | 10:36 runtime |
| interpreter-with-spel | ✅ | ✅ | ✅ | 6:12 runtime |
| iterator | ✅ | ✅ | ✅ | 9:31 runtime |
| mediator | ✅ | ✅ | ✅ | 10:10 runtime |
| memento | ✅ | ✅ | ✅ | 10:00 runtime |
| observer | ✅ | ✅ | ✅ | 10:20 runtime |
| observer-with-spring | ✅ | ✅ | ✅ | 5:53 runtime |
| state | ✅ | ✅ | ✅ | 10:44 runtime |
| strategy | ✅ | ✅ | ✅ | 9:14 runtime |
| strategy-with-spring | ✅ | ✅ | ✅ | 5:22 runtime |
| template-method | ✅ | ✅ | ✅ | 11:15 runtime |
| template-method-with-spring | ✅ | ✅ | ✅ | 6:23 runtime |
| visitor | ✅ | ✅ | ✅ | 12:13 runtime |

## concurrency-design-patterns

| Project | Script | Video | Animation | Note |
| --- | :---: | :---: | :---: | --- |
| active-object | ✅ | ✅ | ✅ | 7:01 runtime |
| active-object-with-spring | ✅ | ✅ | ✅ | 6:23 runtime |
| actor | ✅ | ✅ | ✅ | 5:39 runtime |
| balking | ✅ | ✅ | ✅ | 5:23 runtime |
| double-checked-locking | ✅ | ✅ | ✅ | 5:48 runtime |
| fork-join | ✅ | ✅ | ✅ | 5:48 runtime |
| future-promise | ✅ | ✅ | ✅ | 7:20 runtime |
| future-promise-with-spring | ✅ | ✅ | ✅ |  |
| guarded-suspension | ✅ | ✅ | ✅ | 5:31 runtime |
| monitor-object | ✅ | ✅ | ✅ | 7:04 runtime |
| producer-consumer | ✅ | ✅ | ✅ | 8:00 runtime |
| read-write-lock | ✅ | ✅ | ✅ | 6:54 runtime |
| thread-local-storage | ✅ | ✅ | ✅ | 5:49 runtime |
| thread-pool | ✅ | ✅ | ✅ | 7:28 runtime |
| thread-pool-with-spring | ✅ | ✅ | ✅ | 6:02 runtime |
| two-phase-termination | ✅ | ✅ | ✅ | 5:38 runtime |

## creational

| Project | Script | Video | Animation | Note |
| --- | :---: | :---: | :---: | --- |
| abstract-factory | ✅ | ✅ | ✅ | 9:47 runtime |
| builder | ✅ | ✅ | ✅ | 10:05 runtime |
| factory-method | ✅ | ✅ | ✅ | 8:20 runtime |
| prototype | ✅ | ✅ | ✅ | 9:06 runtime |
| prototype-with-spring | ✅ | ✅ | ✅ | 5:08 runtime |
| simple-factory | ✅ | ✅ | ✅ | 8:11 runtime |
| singleton | ✅ | ✅ | ✅ | 7:43 runtime |
| singleton-with-spring | ✅ | ✅ | ✅ | 5:43 runtime |
| static-factory | ✅ | ✅ | ✅ | 10:46 runtime |

## domain-driven-design-patterns

| Project | Script | Video | Animation | Note |
| --- | :---: | :---: | :---: | --- |
| aggregate | ✅ | ✅ | ✅ | 5:40 runtime |
| anti-corruption-layer | ✅ | ✅ | ✅ | 5:42 runtime |
| bounded-context | ✅ | ✅ | ✅ | 5:27 runtime |
| domain-event | ✅ | ✅ | ✅ | 5:48 runtime |
| specification | ✅ | ✅ | ✅ | 5:34 runtime |
| value-object | ✅ | ✅ | ✅ | 5:45 runtime |

## enterprise-design-patterns

| Project | Script | Video | Animation | Note |
| --- | :---: | :---: | :---: | --- |
| active-record | ✅ | ✅ | ✅ | 5:15 runtime |
| data-mapper | ✅ | ✅ | ✅ | 6:25 runtime |
| dto | ✅ | ✅ | ✅ | 6:19 runtime |
| front-controller | ✅ | ✅ | ✅ | 5:37 runtime |
| gateway | ✅ | ✅ | ✅ | 5:37 runtime |
| identity-map | ✅ | ✅ | ✅ | 6:14 runtime |
| identity-map-with-jpa | ✅ | ✅ | ✅ | 6:28 runtime |
| lazy-load | ✅ | ✅ | ✅ | 6:01 runtime |
| lazy-load-with-hibernate | ✅ | ✅ | ✅ | 6:31 runtime |
| optimistic-offline-lock | ✅ | ✅ | ✅ | 5:29 runtime |
| pessimistic-offline-lock | ✅ | ✅ | ✅ | 5:31 runtime |
| repository | ✅ | ✅ | ✅ | 6:10 runtime |
| repository-with-spring-data | ✅ | ✅ | ✅ | 6:19 runtime |
| service-layer | ✅ | ✅ | ✅ | 6:00 runtime |
| transaction-script | ✅ | ✅ | ✅ | 5:23 runtime |
| unit-of-work | ✅ | ✅ | ✅ | 6:16 runtime |
| unit-of-work-with-spring | ✅ | ✅ | ✅ | 6:21 runtime |

## foundational-design-patterns

| Project | Script | Video | Animation | Note |
| --- | :---: | :---: | :---: | --- |
| callback | ✅ | ✅ | ✅ | 4:55 runtime |
| delegation | ✅ | ✅ | ✅ | 5:05 runtime |
| dependency-injection | ✅ | ✅ | ✅ | 6:53 runtime |
| dependency-injection-with-spring | ✅ | ✅ | ✅ | 5:47 runtime |
| execute-around | ✅ | ✅ | ✅ | 5:13 runtime |
| fluent-interface | ✅ | ✅ | ✅ | 5:27 runtime |
| multiton | ✅ | ✅ | ✅ | 5:04 runtime |
| null-object | ✅ | ✅ | ✅ | 6:00 runtime |
| object-pool | ✅ | ✅ | ✅ | 6:19 runtime |
| object-pool-with-hikaricp | ✅ | ✅ | ✅ | 5:53 runtime |
| registry | ✅ | ✅ | ✅ | 5:42 runtime |
| registry-with-spring | ✅ | ✅ | ✅ | 5:49 runtime |
| service-locator | ✅ | ✅ | ✅ | 5:40 runtime |
| service-locator-with-consul | ✅ | ✅ | ✅ | 6:33 runtime |
| type-object | ✅ | ✅ | ✅ | 5:30 runtime |

## messaging-integration-patterns

| Project | Script | Video | Animation | Note |
| --- | :---: | :---: | :---: | --- |
| content-based-router | ✅ | ✅ | ✅ | 5:46 runtime |
| content-based-router-with-camel | ✅ | ✅ | ✅ | 10:20 runtime |
| dead-letter-channel | ✅ | ✅ | ✅ | 5:28 runtime |
| dead-letter-channel-with-rabbitmq | ✅ | ✅ | ✅ | 8:15 runtime |
| event-bus | ✅ | ✅ | ✅ | 5:28 runtime |
| event-bus-with-nats | ✅ | ✅ | ✅ | 8:39 runtime |
| message-channel | ✅ | ✅ | ✅ | 5:07 runtime |
| message-channel-with-rabbitmq | ✅ | ✅ | ✅ | 10:06 runtime |
| splitter-aggregator | ✅ | ✅ | ✅ | 5:17 runtime |
| splitter-aggregator-with-camel | ✅ | ✅ | ✅ | 8:17 runtime |

## micro-services-design-patterns

| Project | Script | Video | Animation | Note |
| --- | :---: | :---: | :---: | --- |
| api-composition | ✅ | ✅ | ✅ | 13:00 runtime |
| api-gateway | ✅ | ✅ | ✅ |  |
| api-gateway-with-spring-cloud-gateway | ✅ | ✅ | ✅ | 7:17 runtime |
| bulkhead | ✅ | ✅ | ✅ | 13:25 runtime |
| bulkhead-with-resilience4j | ✅ | ✅ | ✅ | 6:22 runtime |
| cache-aside | ✅ | ✅ | ✅ | 6:03 runtime |
| cache-aside-with-redis | ✅ | ✅ | ✅ | 10:56 runtime |
| circuit-breaker | ✅ | ✅ | ✅ | 14:26 runtime |
| circuit-breaker-with-resilience4j | ✅ | ✅ | ✅ | 6:14 runtime |
| claim-check | ✅ | 🕒 | ✅ |  |
| claim-check-with-s3 | ✅ | 🕒 | ✅ |  |
| competing-consumers | ✅ | 🕒 | ✅ |  |
| competing-consumers-with-rabbitmq | ✅ | 🕒 | ✅ |  |
| cqrs | ✅ | 🕒 | ✅ |  |
| database-per-service | ✅ | 🕒 | ⏳ |  |
| database-per-service-with-containers | ✅ | 🕒 | ⏳ |  |
| idempotent-consumer | ✅ | 🕒 | ⏳ |  |
| idempotent-consumer-with-kafka | ✅ | 🕒 | ⏳ |  |
| leader-election | ✅ | 🕒 | ⏳ |  |
| leader-election-with-kubernetes | ✅ | 🕒 | ⏳ |  |
| load-balancing | ✅ | 🕒 | ⏳ |  |
| load-balancing-with-spring-cloud-loadbalancer | ✅ | 🕒 | ⏳ |  |
| pipes-and-filters | ✅ | 🕒 | ⏳ |  |
| publisher-subscriber | ✅ | 🕒 | ⏳ |  |
| publisher-subscriber-with-redis | ✅ | 🕒 | ⏳ |  |
| queue-based-load-leveling | ✅ | 🕒 | ⏳ |  |
| queue-based-load-leveling-with-sqs | ✅ | 🕒 | ⏳ |  |
| rate-limiter | ✅ | 🕒 | ⏳ |  |
| rate-limiter-with-redis | ✅ | 🕒 | ⏳ |  |
| retry | ✅ | 🕒 | ⏳ |  |
| retry-with-resilience4j | ✅ | 🕒 | ⏳ |  |
| saga | ✅ | 🕒 | ⏳ |  |
| scatter-gather | ✅ | 🕒 | ⏳ |  |
| service-discovery | ✅ | 🕒 | ⏳ |  |
| service-discovery-with-spring-cloud-consul | ✅ | 🕒 | ⏳ |  |
| timeout | ✅ | 🕒 | ⏳ |  |
| transactional-outbox | ✅ | 🕒 | ⏳ |  |
| transactional-outbox-with-debezium | ✅ | 🕒 | ⏳ |  |

## platform-design-patterns

| Project | Script | Video | Animation | Note |
| --- | :---: | :---: | :---: | --- |
| backends-for-frontends | ✅ | 🕒 | ⏳ |  |
| blue-green-and-canary | ✅ | 🕒 | ⏳ |  |
| blue-green-and-canary-with-kubernetes | ✅ | 🕒 | ⏳ |  |
| consumer-driven-contract | ✅ | 🕒 | ⏳ |  |
| consumer-driven-contract-with-pact | ✅ | 🕒 | ⏳ |  |
| distributed-tracing | ✅ | 🕒 | ⏳ |  |
| event-sourcing | ✅ | 🕒 | ⏳ |  |
| event-sourcing-with-eventstoredb | ✅ | 🕒 | ⏳ |  |
| externalised-configuration | ✅ | 🕒 | ⏳ |  |
| externalised-configuration-with-spring-cloud-config | ✅ | 🕒 | ⏳ |  |
| feature-toggle | ✅ | 🕒 | ⏳ |  |
| feature-toggle-with-flagd | ✅ | 🕒 | ⏳ |  |
| service-mesh | ✅ | 🕒 | ⏳ |  |
| service-mesh-with-envoy | ✅ | 🕒 | ⏳ |  |
| sidecar | ✅ | 🕒 | ⏳ |  |
| sidecar-java-proxy | ✅ | 🕒 | ⏳ |  |
| sidecar-on-kubernetes | ✅ | 🕒 | ⏳ |  |
| strangler-fig | ✅ | 🕒 | ⏳ |  |
| strangler-fig-with-nginx | ✅ | 🕒 | ⏳ |  |

## structural

| Project | Script | Video | Animation | Note |
| --- | :---: | :---: | :---: | --- |
| adapter | ✅ | 🕒 | ⏳ |  |
| bridge | ✅ | 🕒 | ⏳ |  |
| composite | ✅ | 🕒 | ⏳ |  |
| decorator | ✅ | 🕒 | ⏳ |  |
| facade | ✅ | 🕒 | ⏳ |  |
| flyweight | ✅ | 🕒 | ⏳ |  |
| proxy | ✅ | 🕒 | ⏳ |  |
| proxy-with-spring | ✅ | 🕒 | ⏳ |  |
