# Modular Monolith, Explained

## The pattern in one sentence

A modular monolith is one program split into modules that each own their data
and rules and are reached only through small front doors, with the walls
between them checked on every build.

## The 5 acts

### 1. Every table open

In the `mud` package, every table is a public static map. `MudCheckout` takes
stock by writing to `Tables.STOCK` itself. The catalogue has a rule that stock
never goes below zero, but checkout never asks the catalogue. There is one
kettle; two orders each take one, stock becomes -1, and two customers have paid
for one kettle.

### 2. Modules with front doors

Now the shop is three modules. Catalogue owns stock, payments owns its ledger,
and orders is handed only their front doors, `CatalogApi` and `PaymentsApi`.
Orders must ask the catalogue to reserve a kettle. The first order is placed and
charged; the second is refused, "only 0 kettle left", and never charged. The
catalogue's rule holds because it is the only code that can change stock.

### 3. Boundaries checked

Java cannot stop orders importing `payments.internal.PaymentsModule`: the class
is public, because payments' own front door needs to create it. So
`BoundaryCheck` reads every source file's imports. The real project has zero
violations. When someone adds that import to `OrdersModule`, the check reports
"OrdersModule.java imports payments.internal", and a test fails the build.

### 4. Moving a module out

Payments grows, and the team wants to deploy it on its own. Because orders only
ever used `PaymentsApi`, a `RemotePayments` class that answers the same front
door over the network can be plugged in instead. Order three is placed with one
network call to payments, and not a single line of the orders module changes.

### 5. The bill

It is still one program. Three modules share one build and one deployment, so a
payments fix redeploys the catalogue too. They share one process, so a crash in
any module stops all three, and they can only be scaled together. And the
boundaries last only as long as the check runs on every build.

## The verdict

Start most new systems as a modular monolith. Split by business area, give
each module a front door, keep its data private, and fail the build on any
shortcut. Move a module out into its own service only when it truly needs its
own deployment, scaling or team.

## How to recognise this in code you did not write

- Top-level packages named after business areas, each with `api` and `internal` parts.
- `module-info.java`, ArchUnit or Spring Modulith tests.
- A rule that each module has its own tables or schema.
- Architecture documents describing "components" inside one deployable.

## Where you have already met this

- Java's own module system (`module-info.java`), with `exports` naming the public packages.
- ArchUnit tests that fail the build when one package uses another it should not.
- Spring Modulith, which checks module boundaries in Spring Boot applications.
- Shopify's and GitHub's large monoliths, split into internal components.
