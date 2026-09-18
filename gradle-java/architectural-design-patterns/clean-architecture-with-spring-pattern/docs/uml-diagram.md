# Clean Architecture with Spring — UML Sequence Diagrams

Two sequences: the container succeeding, and the container failing on the
identical mistake that would not compile in the hand-wired project.

## 1. The Container Wires The Whole Graph

![Clean Architecture with Spring sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant App as Application.main
    participant Ctx as ApplicationContext «AppConfig»
    participant UC as PlaceOrderInteractor

    App->>Ctx: SpringApplication.run(...)
    Ctx->>Ctx: resolve all seven @Bean methods
    Ctx->>UC: new PlaceOrderInteractor(products, orders, payments, notifications)
    Ctx-->>App: context ready, all beans available
```

</details>

## 2. The Container Fails — At Startup, Not At Compile Time

![The container failing at startup](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant App as Application «act five»
    participant Ctx as ApplicationContext «BrokenAppConfig»

    Note over Ctx: BrokenAppConfig has no @Bean for NotificationGateway.<br/>javac has already accepted this file.
    App->>Ctx: new AnnotationConfigApplicationContext(BrokenAppConfig.class)
    Ctx->>Ctx: resolve placeOrderInputBoundary's 4th parameter
    Note over Ctx: no bean of type NotificationGateway exists
    Ctx-->>App: throws UnsatisfiedDependencyException
```

</details>

Compare sequence two with deleting the equivalent argument from
`clean-architecture-pattern`'s hand-wired `new PlaceOrderInteractor(...)`
call: that failure happens in your editor, at the moment you try to save
the file, and never reaches a running process at all.
