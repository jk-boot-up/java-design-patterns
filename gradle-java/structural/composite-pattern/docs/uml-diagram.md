# Composite Pattern — UML Sequence Diagram

Shows the runtime interaction: `CatalogDemo` calls `totalPrice()` once, on
the root `Category`, and the recursion into nested categories and leaf
products happens entirely inside the tree — no caller-side `instanceof`,
no caller-side loop past the first call.

![Composite pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    actor Client as CatalogDemo
    participant Electronics as Category (Electronics)
    participant Phone as Product (Phone)
    participant Accessories as Category (Accessories)
    participant Case as Product (Case)
    participant Cables as Category (Cables)
    participant Cable as Product (USB-C Cable)

    Client->>Electronics: totalPrice()
    activate Electronics
    Electronics->>Phone: totalPrice()
    Phone-->>Electronics: 599.99
    Electronics->>Accessories: totalPrice()
    activate Accessories
    Accessories->>Case: totalPrice()
    Case-->>Accessories: 19.99
    Accessories->>Cables: totalPrice()
    activate Cables
    Cables->>Cable: totalPrice()
    Cable-->>Cables: 9.99
    Cables-->>Accessories: 9.99
    deactivate Cables
    Accessories-->>Electronics: 29.98 + 9.99 = 59.97 (Charger omitted for space)
    deactivate Accessories
    Electronics-->>Client: 599.99 + 59.97 = 659.96
    deactivate Electronics

    Note over Client,Cable: One call from the client. Every level below recurses through the same totalPrice() method.
```

</details>

## Notes

- The client makes exactly **one** call, `electronics.totalPrice()`. Every
  arrow below that is the tree talking to itself — `Category` asking each
  of its children the identical question it was just asked.
- `Product.totalPrice()` never sends any further messages — it is the base
  case of the recursion, answering with its own stored price.
- `Category.totalPrice()` is the recursive case: it waits for every child's
  answer (whether that child is a `Product` or another `Category`) and
  sums them before returning to whoever asked it.
- Nesting one more `Category` (as `Cables` is nested inside `Accessories`)
  adds one more layer to this diagram, but requires no new code — the same
  `totalPrice()` method just gets called one more time.
