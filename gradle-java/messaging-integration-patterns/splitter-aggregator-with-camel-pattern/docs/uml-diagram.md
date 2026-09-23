# Splitter and Aggregator with Camel Pattern — UML Sequence Diagrams

Four sequences. The deadline comes first, because it is the one thing this project exists to show.

## 1. The Deadline Fires

The aggregator holds two of three shipments. Nothing else will ever arrive. The background checker, which has been looking at the clock every hundred milliseconds, finds that six hundred have passed and ends the wait.

![The deadline fires](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as Camel aggregate
    participant T as deadline checker
    participant O as the customer
    A-->>A: holding 2 of 3 for ORD-4473
    T->>A: 100 ms, not yet
    T->>A: 600 ms have passed
    A->>O: 2 of 3 shipments, missing Glasgow, completed by timeout
```

</details>

## 2. The Split Stamps Every Piece

One order in, three messages out. Camel numbers them itself and copies the order's headers onto each one, so the order number travels without anybody arranging it.

![The split stamps every piece](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout route
    participant S as Camel split
    participant W as warehouse step
    C->>S: one order, 3 lines, order number ORD-4471
    S->>W: piece 1 of 3, stamped ORD-4471, to Leeds
    S->>W: piece 2 of 3, stamped ORD-4471, to Reading
    S->>W: piece 3 of 3, stamped ORD-4471, to Glasgow
    Note over S,W: Camel numbers the pieces from zero and the demo adds one so a person can read them
```

</details>

## 3. Jumbled Arrivals, Ordered Answer

The warehouses answer third, first, second. The aggregator files each under the place it says it is, so the answer comes out in the customer's line order and completes by size.

![Jumbled arrivals, ordered answer](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant W as warehouses
    participant A as Camel aggregate
    participant O as the customer
    W->>A: shipment 3, Glasgow
    A-->>A: 1 of 3, keep waiting
    W->>A: shipment 1, Leeds
    A-->>A: 2 of 3, keep waiting
    W->>A: shipment 2, Reading
    A->>O: 3 of 3 in line order, total GBP 283.42, completed by size
```

</details>

## 4. A Repeated Message Counts As Progress

Camel's completion by size counts messages, not distinct pieces. Two copies of the Reading shipment plus one from Leeds makes three messages, so the order is declared finished with one of its lines never picked.

![A repeated message counts as progress](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant W as warehouses
    participant F as the fold you wrote
    participant A as Camel aggregate
    W->>A: shipment 1, Leeds
    A->>F: fold it in
    W->>A: shipment 2, Reading
    A->>F: fold it in
    W->>A: shipment 2 again, Reading
    A->>F: fold it in
    F-->>A: duplicate noticed, kept the first, total stays GBP 265.97
    A-->>A: 3 messages seen, 3 expected, completed by size at 2 of 3 lines
```

</details>
