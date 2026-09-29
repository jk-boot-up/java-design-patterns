# Message Translator / Normalizer, Explained

## The pattern in one sentence

A message translator converts one format into another; a normalizer
recognises each incoming format and picks the translator, so everything
arrives in one canonical shape.

## The 5 acts

### 1. The warehouse reads every format

`Warehouse.pickOld` recognises and parses each of the three formats inside
the warehouse. It picks a kettle, two mugs and a teapot. When marketplace C
starts sending XML, the warehouse fails: "warehouse cannot read this order".
Every new format means changing the warehouse.

### 2. Translators

Each format gets its own small translator that produces an `OrderMessage`:
order ID, product code, quantity and price in pence. The web form, the CSV and
the JSON all come out in exactly the same shape.

### 3. The normalizer

`Normalizer` holds a list of rules: a message starting with "order=" is the
web form, one matching "A-" and commas is marketplace A, one starting with a
brace is marketplace B. It picks the translator, and the warehouse only ever
receives `OrderMessage`.

### 4. A new marketplace

Marketplace C is added with one translator for its XML and one rule
recognising it. Its order, C-5, one kettle, reaches the warehouse as an
ordinary `OrderMessage`. The warehouse was not changed.

### 5. The bill

Marketplace B's order carries a gift note, "Happy birthday, Mum". The
canonical order has no field for it, so after translation it is gone. Every
field someone needs must be added to the canonical order and to every
translator.

## The verdict

Use a normalizer at the edge whenever several senders use different formats.
Keep one small translator per format, define the canonical message carefully,
and check what each translation drops.

## How to recognise this in code you did not write

- Mappers or transformers named after an external system: `AmazonOrderMapper`.
- A canonical `Order` or `Event` type used everywhere inside.
- A router that picks a parser by content type or message shape.

## Where you have already met this

- Apache Camel's data formats and `unmarshal`, and Spring Integration transformers.
- Canonical data models in enterprise integration.
- Adapters in payment and shipping integrations that map each provider's API to one internal model.
