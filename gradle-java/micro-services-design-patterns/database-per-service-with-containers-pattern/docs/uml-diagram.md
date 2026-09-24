# Database per Service with Containers Pattern — UML Sequence Diagrams

Four sequences. The join tried from both sides comes first, because it is the one thing the hand-built twin could only describe.

## 1. The Join, Tried Anyway

From the Orders side, Postgres refuses the old join, and refuses even a reach into another database on the same server. From the Catalog side, MongoDB runs its own join into a collection it does not have, and answers with empty lists and no error.

![The join, tried anyway](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant O as Orders service
    participant PG as Postgres orders db
    participant C as Catalog service
    participant M as MongoDB catalog db
    O->>PG: SELECT ... FROM orders JOIN products
    PG->>O: ERROR 42P01, relation products does not exist
    O->>PG: SELECT ... FROM shop.public.products
    PG->>O: ERROR 0A000, cross-database references are not implemented
    C->>M: aggregate products, $lookup from orders
    Note over M: no collection called orders here, treated as empty
    M->>C: SKU-KETTLE with 0 orders, SKU-MUG with 0 orders
    Note over C: no error. the answer is simply wrong
```

</details>

## 2. The Rename, Before And After

In the shared database the Catalog team's rename breaks the Orders team's query. After the split the same kind of rename touches only the Catalog's own documents and code.

![The rename, before and after](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant CT as Catalog team
    participant S as Postgres shop db
    participant P as order history page
    participant M as MongoDB catalog db
    CT->>S: RENAME COLUMN product_name TO title
    P->>S: the join, naming p.product_name
    S->>P: ERROR 42703, column does not exist
    Note over CT,P: after the split
    CT->>M: rename name to title in every document
    M->>CT: 2 documents changed
    P->>M: via the Catalog service, names for 2 skus
    M->>P: the same 2 names. page unchanged
```

</details>

## 3. No Foreign Key Between Two Engines

Postgres refused this delete when both tables were in one database. Across two engines nothing can.

![No foreign key between two engines](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as Catalog service
    participant M as MongoDB
    participant PG as Postgres
    participant P as order history page
    C->>M: delete SKU-KETTLE
    M->>C: 1 document deleted
    Note over PG: still 1 order naming SKU-KETTLE, and no way to know
    P->>PG: orders for cust-7
    P->>M: names for SKU-KETTLE and SKU-MUG
    M->>P: only the mug
    Note over P: ord-101 shows no longer in the catalogue
```

</details>

## 4. A Rollback Stops At The Edge Of Its Engine

The order and the stock change are two writes to two engines. Undoing one does not undo the other.

![A rollback stops at the edge of its engine](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant O as Orders service
    participant PG as Postgres
    participant C as Catalog service
    participant M as MongoDB
    O->>PG: begin, insert ord-103, SKU-MUG x2
    C->>M: stock of SKU-MUG minus 2
    M->>C: kept at once, 38
    Note over O: payment declined
    O->>PG: rollback
    Note over PG: ord-103 gone, 2 orders for cust-7
    Note over M: stock still 38, was 40
```

</details>
