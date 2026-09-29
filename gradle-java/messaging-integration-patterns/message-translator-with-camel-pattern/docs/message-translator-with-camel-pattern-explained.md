# Message Translator with Apache Camel, Explained

## The pattern in one sentence

With Camel, each translator is a route, each format is read by a data format,
and a normalizer route sends each message to the right translator by name.

## The 5 acts

### 1. Straight to the warehouse

The warehouse route begins by converting its message to the canonical
`OrderMessage`. When a marketplace's raw JSON is sent straight to it, Camel
refuses: there is no type converter from a String to an OrderMessage. The
framework stops a foreign format at the door, instead of letting the
warehouse guess.

### 2. A translator route per format

Each format gets its own translator route. The web form is split into
key-value pairs. The CSV route uses Camel's CSV data format, and the JSON
route uses Camel's Jackson data format. Each ends by building the canonical
order: two mugs for A-77, one teapot for B-9, one kettle for W-1.

### 3. The normalizer

Now every order goes to one inbox. The normalizer route looks at the first
character of the text, sets a format header, and uses Camel's `toD`, a
dynamic "send to", to reach `direct:translate-` plus that format. CSV, JSON
and web-form orders all come out as canonical picks. Five routes are running:
the normalizer, three translators and the warehouse.

### 4. A new format, a new route

Marketplace C sends XML. The normalizer recognises it and sends it to
`direct:translate-xml`, but no route listens there yet, and Camel says so:
no consumers available. Adding one route, which reads the XML with XPath,
while the others keep running, makes it work: one kettle for C-5. The
normalizer and the warehouse routes were not changed.

### 5. The bill

Camel did not solve the canonical model's weakness: marketplace B's gift
note still does not survive, because the canonical order has no room for it.
And the program now carries more than twenty library files, against none for
the plain version, plus Camel's route language to learn.

## The verdict

Use Camel for translation when there are many formats and transports and
translators arrive over time. For a handful of stable formats, the plain Java
version is simpler.

## How to recognise this in code you did not write

- `from(...).unmarshal().json(...)` and `.unmarshal().csv()`.
- `toD("direct:translate-${header.format}")`.
- `convertBodyTo(SomeCanonical.class)` at the start of a route.

## Where you have already met this

- Apache Camel routes in Spring Boot or Quarkus applications.
- Spring Integration's transformers and MuleSoft's DataWeave, the same idea in other tools.
- The book Enterprise Integration Patterns, whose names Camel uses directly.
