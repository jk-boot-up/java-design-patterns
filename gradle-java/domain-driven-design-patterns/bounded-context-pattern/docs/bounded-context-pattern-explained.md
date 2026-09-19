# Bounded Context, Explained

## The pattern in one sentence

A bounded context is a boundary inside which one word has one meaning and one model, with explicit links to the other contexts around it.

## The six acts

### One Customer For Everyone

One Customer class has twelve fields, and each department uses only a handful. Every department depends on all twelve, so any department's change is every department's change.

```
  fields in the company-wide Customer class: 12.
  each context uses a handful of them, and every one depends on the whole class, so one context's change is every context's change.
```

### The Same Word, Three Meanings

Is Ada active? Sales says yes, she bought in the last ninety days. Shipping says yes, a parcel is on its way. Support says no, no open ticket. Each is right in its own context.

```
  is Ada an active customer?
    Sales, bought in the last 90 days:  true.
    Shipping, a parcel on its way:      true.
    Support, an open ticket:            false.
  one class cannot answer all three. each answer is right, in its own context.
```

### A Model For Each Context

Sales has a buyer, Shipping a recipient and Support a contact, each with four fields. None knows the others' types. They share only the customer id.

```
  Sales:    Buyer with 4 fields: credit limit, last purchase.
  Shipping: Recipient with 4 fields: address, parcels in transit.
  Support:  Contact with 4 fields: phone, open tickets.
  none of them knows the others' types. they share one thing, the CustomerId.
```

### The Contexts Talk By Events

Sales renames Ada and publishes a fact. Until it is delivered, Shipping still has the old name. After delivery, Shipping updates its own recipient. It never saw a buyer.

```
  Sales renames Ada. Sales says: Ada King. Shipping says: Ada Lovelace. events waiting: 1.
  after the event is delivered, Shipping says: Ada King.
  Shipping translated a Sales fact into a change to its own Recipient. it never saw a Buyer.
```

### The Boundary Can Be Checked

A test scans the source and finds no import of one context's types by another. Shipping can change its own model freely.

```
  imports of one context's types by another: 0.
  Shipping can add a field to Recipient and nothing in Sales or Support needs to change.
```

### The Bill

Ada's name is stored three times. Between a rename and its delivery, two contexts disagree. And every context needs its own translator for every event it cares about.

```
  Ada's name is now stored three times: Sales, Shipping, Support.
  between the rename and the delivery, two contexts disagreed about her name. that gap is called eventual consistency.
  and every context needs its own translator for every event it cares about.
```

## The verdict

Draw a bounded context wherever the same word starts to mean different things, or where different teams own the model. Give each its own model, share only ids and events, translate at the border, and accept that copies lag. Do not split a small system that one team understands.

## How to recognise this in code you did not write

- The same word, such as Customer or Product, defined by separate classes in separate packages.
- Services or modules that each have their own database and their own idea of a customer.
- Events carrying an id and a few plain values, not whole objects.
- A context map, or a diagram of who is upstream of whom.

## Where you have already met this

Every large system split by department, and every microservice that owns its own data and its own vocabulary.

## When this is too much

In a small system that one team understands, one model is simpler, and translation is pure cost. A boundary earns its place where meanings really diverge.
