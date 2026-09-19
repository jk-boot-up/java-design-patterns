# Proxy with Spring Pattern — Class Diagram

The aspect is the protection proxy. The beans only carry the annotation.

![Proxy with Spring Pattern — Class Diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class RoleAspect {
        <<@Aspect>>
        +check(call, required) Object
    }
    class RequiresRole {
        <<annotation>>
    }
    class ImageCatalogue {
        <<@Service>>
        +render(sku) String
        +renderThroughThis(sku) String
        +renderFinal(sku) String
    }
    class OrderExport
    class RefundDesk
    RoleAspect ..> RequiresRole : selects methods
    ImageCatalogue ..> RequiresRole
    OrderExport ..> RequiresRole
    RefundDesk ..> RequiresRole
```

</details>
