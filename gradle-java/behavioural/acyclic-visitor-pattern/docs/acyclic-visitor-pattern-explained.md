# Acyclic Visitor, Explained

## The pattern in one sentence

An acyclic visitor gives each type its own one-method visitor interface and an
empty root, so each visitor handles only the types it chooses and new types
change nothing existing.

## The 5 acts

### 1. The classic visitor

`ClassicVisitor` has one method per product type: book, food, electronics.
The VAT visitor works out £6.00 on a book, some tea and a £30 kettle. The
customs visitor only cares about electronics but must still write two empty
methods. When the gift card type arrives, `ClassicVisitor` has no method for
it: the interface and every visitor would have to change.

### 2. The acyclic visitor

`ProductVisitor` is now empty: it names no product type. Each type has its
own one-method interface: `BookVisitor`, `FoodVisitor`, `ElectronicsVisitor`.
Each product's `accept` checks whether the visitor wears its interface, and
only then visits. The VAT visitor implements the three it handles, and the
basket's VAT is still £6.00. The cycle is gone.

### 3. A new product type

The gift card type comes with its own `GiftCardVisitor` interface and a new
`GiftCardActivation` visitor. The VAT visitor does not wear the gift card
interface, so it skips `GIFT-1` and the VAT stays £6.00. The activation
visitor handles `GIFT-1`. The VAT and customs classes were not touched.

### 4. A visitor for one type

Customs forms are only needed for electronics, so `Customs` implements only
`ElectronicsVisitor`. Across the four products it handles one, the kettle,
and produces one form: 1200 grams. It has no empty methods at all.

### 5. The bill

The compiler no longer checks that a visitor handles everything. A VAT
visitor that forgot `FoodVisitor` compiles happily; at run time the tea is
simply skipped (`accept` returns false) and nobody is told. And there is one
extra interface for every product type.

## The verdict

Use it when new types keep arriving and most operations only care about a few
of them. Log or test the skipped cases, because the compiler no longer checks
them. When the type list is fixed, prefer the classic Visitor or a sealed
interface with `switch`.

## How to recognise this in code you did not write

- An empty marker interface that many small visitor interfaces extend.
- `accept` methods that start with `if (visitor instanceof ...)`.
- Visitors that implement a handful of one-method interfaces.

## Where you have already met this

- Robert C. Martin's description of Acyclic Visitor in "Pattern Languages of Program Design 3".
- Plug-in systems where each plug-in says which file types or events it can handle.
- Event listeners that implement only the listener interfaces for the events they care about.
