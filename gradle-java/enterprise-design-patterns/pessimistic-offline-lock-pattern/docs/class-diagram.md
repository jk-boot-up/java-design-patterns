# Pessimistic Offline Lock Pattern — Class Diagram

A lock manager decides who may edit. The store refuses writes from anyone else.

![Pessimistic Offline Lock Pattern — Class Diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class LockManager {
        +acquire(resource, owner, ttl)
        +holds(resource, owner) boolean
        +release(resource, owner)
    }
    class ProductStore {
        +read(sku) Product
        +write(sku, owner, product)
    }
    class Clock {
        +now() long
        +advance(duration)
    }
    class LockedBy {
        +holder() String
    }
    ProductStore --> LockManager
    LockManager --> Clock
    LockManager ..> LockedBy : throws
```

</details>
