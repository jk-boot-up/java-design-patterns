# Extension Object, Explained

## The pattern in one sentence

An extension object lets code attach extra roles to individual objects and
lets clients ask for a role by type, so a core class stays small while new
abilities keep arriving.

## The 5 acts

### 1. One class, every field

`FatProduct` has a field for everything: download link and limit, warranty,
gift wrap, age limit. A mug uses three of its eight fields and leaves five
empty. Selling subscriptions would mean a ninth field, added to the one class
that every part of the shop depends on.

### 2. A small core, with roles

`Product` now holds only a code, a name and a price. Extra roles are attached
to individual products with `with`: the e-book gets a `Download` role, the
kettle a `Warranty`. The mug gets nothing. The product class knows nothing
about downloads or warranties.

### 3. Asking for a role

After payment, `Checkout` asks each product: do you have a `Download` role? A
`Warranty`? The e-book answers with a download link, which is emailed with its
limit of three downloads. The kettle's two-year warranty is registered. The mug
answers "no" to both, so nothing extra happens.

### 4. A new role

The subscriptions team writes its own `Subscription` record and attaches it to
the coffee beans. Checkout schedules a delivery every four weeks. `Product`
did not change; the team owns its own role.

### 5. The bill

Nothing checks that a product has the roles it should. A second e-book is
added without its `Download` role. It compiles and sells; after payment there
are zero actions, and the customer receives nothing. And reading `Product` no
longer tells anyone what a product can do.

## The verdict

Use it when abilities belong to some objects and not others, keep arriving,
and are owned by different teams. Check at startup that objects have the roles
they must, and keep a list of the roles that exist so developers can find them.

## How to recognise this in code you did not write

- Methods like `getExtension(Class)`, `getAdapter(Class)` or `unwrap(Class)`.
- A map from a type to an object inside a core class.
- Client code that does `.extension(X.class).ifPresent(...)`.

## Where you have already met this

- Eclipse's `IAdaptable.getAdapter(Class)`, which asks an object for another role.
- `Optional`-returning lookups such as `unwrap(Class)` in JDBC and JPA.
- Entity-component systems in games, where an entity is a bag of components.
- Product attribute tables in shop platforms, where each product has only the attributes it needs.
