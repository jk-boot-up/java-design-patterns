# Multiton Pattern — Class Diagram

A class that keeps one instance for each region.

![Multiton Pattern — Class Diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class Warehouse {
        -region String
        -stock int
        -INSTANCES Map
        -Warehouse(region)
        +of(region)$ Warehouse
        +reserve(quantity)
        +stock() int
    }
```

</details>
