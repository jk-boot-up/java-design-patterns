# Database per Service with Containers Pattern — Data Flow Diagram

One order history page, from two engines. Two questions, one assembly step, and two different reasons a product name can be missing — each of which the page must turn into something to show.

![Database per Service with Containers Pattern — Data Flow Diagram](images/data-flow-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TD
    In(["the page is asked for cust-7's order history"])
    Ask1["ask Orders: one SQL query to Postgres"]
    Rows["2 orders: ord-101 SKU-KETTLE x1, ord-102 SKU-MUG x4"]
    Skus["collect the skus: SKU-KETTLE, SKU-MUG"]
    Ask2{"ask Catalog: one find to MongoDB for both skus"}
    Names["names for the skus MongoDB still has"]
    Down["no answer within 3 seconds"]
    Each{"for each order: is there a name for its sku?"}
    Show(["show the product name"])
    Gone(["show: no longer in the catalogue"])
    Unreach(["show: catalog unreachable"])
    In --> Ask1 --> Rows --> Skus --> Ask2
    Ask2 -- "answered" --> Names --> Each
    Ask2 -- "MongoDB stopped" --> Down --> Unreach
    Each -- yes --> Show
    Each -- "no, the product was deleted" --> Gone
```

</details>
