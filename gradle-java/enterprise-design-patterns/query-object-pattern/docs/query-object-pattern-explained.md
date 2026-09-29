# Query Object, Explained

## The pattern in one sentence

A query object holds a search as a set of criteria that can write themselves
as safe SQL with placeholders and can also run over data in memory.

## The 5 acts

### 1. SQL glued from strings

`StringSql.build` appends each filter to a string. With a category and a price
it works. Without a category it produces `WHERE  AND price_pence <= 3000`,
which the database rejects. And the name filter pastes the customer's text
into the SQL, so the apostrophe in "O'Brien" ends the string early: the first
step of a SQL injection attack.

### 2. A query object

`ProductQuery` is built by adding criteria: `category("kitchen")`,
`maxPrice(3000)`, `inStock()`. It writes SQL with a question mark for every
value, and keeps the values separately: `[kitchen, 3000]`. Leaving out the
category simply leaves out that criterion, and the SQL is still correct.

### 3. The same query in memory

Each criterion can also test a product in Java, so `runOn` runs the same query
over a plain list. It finds the steel kettle, the tea towel and O'Brien's mug.
The glass teapot is out of stock and the desk lamp is not kitchen, so both are
left out. Tests can check a query's meaning without a database.

### 4. Safe and reusable

The saved "cheap kitchen" query is extended with `nameContains("O'Brien")`.
The apostrophe travels as a value, `%O'Brien%`, never as SQL, and one product
is found. Adding a criterion returns a new query, so the saved one still has
its original two values and can be reused for other searches.

### 5. The bill

A query object is a small query language of your own. It has only the
criteria you wrote: no OR, no joins, no sorting until someone adds them. And
each criterion says the same thing twice, once as SQL and once as Java, and
the two must agree.

## The verdict

Use query objects when searches are built from optional filters, saved,
combined or run in several places. Always use placeholders for values, test
criteria in memory, and reach for JPA Criteria, Specifications or jOOQ rather
than growing your own into a full language.

## How to recognise this in code you did not write

- `Criteria`, `Specification` or `Predicate` objects combined with `and`.
- SQL with `?` placeholders built from a list of conditions.
- Saved searches or filter objects passed to a repository.

## Where you have already met this

- JPA's Criteria API and Hibernate's `Criteria`.
- Spring Data `Specification` and QueryDSL.
- jOOQ, which builds type-safe SQL from Java objects.
- Saved searches and filters in online shops.
