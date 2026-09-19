# DTO, Explained

## The pattern in one sentence

A separate object shaped for the boundary, so the domain object never leaves.

## How it works

`CustomerDto` is a Java `record`: flat, immutable, with exactly the three
fields this client needs. `CustomerMapper.toDto` copies them across.

```
THREE. The pattern — a DTO shaped for the boundary.
  domain object: 5297 characters
  DTO:           46 characters
  DTO payload:   {"id":7,"name":"Ada Lovelace","city":"London"}
  order history loaded by the DTO: 0 times.
```

The password hash cannot leak, because the DTO has no field for it. The order
history is never touched. The client's keys are now a contract, not an accident
of a private field's name.

## A DTO is not a domain model

The project shows one of each. `CustomerDto` is a record with no behaviour.
`Customer` enforces a rule: it refuses an email with no `@`. The DTO would carry
a bad email without complaint, because it is data, not a model. Conflating the
two is how anemic domains start.

## The bill

**Mapping code, everywhere.** Every DTO needs a method that copies fields
across by hand. It is tedious, and a new field on the domain object silently
does not reach a DTO that was not updated.

**Near-duplicate classes that drift.** DTOs multiply.

```
FIVE. The bill — mapping code, everywhere.
    CustomerDto: [id, name, city]
    CustomerSummaryDto: [id, name]
    CustomerListItemDto: [id, name, city, loyaltyPoints]
    CustomerDetailDto: [id, name, email, city, loyaltyPoints, orderCount]
  Customer has 7 fields. four DTOs carry 15 between them.
```

Until the mapping layer is larger than the domain it protects.

**The mapping decides what loads.** `toDetail` asks for the order count, and
that touches the lazy history. The DTO can hide it, but only if the mapping does.

## Where you have already met this

A Java record returned from a Spring controller is a DTO, and Jackson writes
its JSON. This is Backends for Frontends at the level of one object rather than
one deployment. MapStruct generates the mapping code, and it is worth taking
once you have felt the tedium by hand.

## When this is too much

For an internal call between two classes in one module, a DTO is a needless
copy. It earns its place at a boundary you do not control: a REST API, a
message, a file.
