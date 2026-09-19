# Data Mapper Pattern — UML Sequence Diagrams

Four sequences: Active Record saving, the mapper inserting, the mapper
finding, and a careless mapper.

## 1. Active Record Saves Itself

![Active Record saves itself](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Caller
    participant R as ActiveRecordCustomer
    participant T as customers table
    Caller->>R: save()
    R->>T: insert id=1
```

</details>

## 2. The Mapper Inserts

![The mapper inserts](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Caller
    participant M as CustomerMapper
    participant T1 as customers table
    participant T2 as addresses table
    Caller->>M: insert(customer)
    M->>T1: insert id=1
    M->>T2: insert id=1
```

</details>

## 3. The Mapper Finds

![The mapper finds](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Caller
    participant M as CustomerMapper
    participant T1 as customers table
    participant T2 as addresses table
    Caller->>M: find(1)
    M->>T1: select id=1
    M->>T2: select id=1
    M-->>Caller: Customer
```

</details>

## 4. A Careless Mapper

![A careless mapper](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Caller
    participant M as CarelessCustomerMapper
    participant T2 as addresses table
    Caller->>M: insert(customer with postcode LS1 4AB)
    M->>T2: insert street, city (no postcode)
    Caller->>M: find(1)
    M-->>Caller: postcode is null, no error
```

</details>
