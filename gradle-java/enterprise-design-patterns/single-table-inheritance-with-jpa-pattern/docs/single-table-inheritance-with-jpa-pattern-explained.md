# Single Table Inheritance with JPA, Explained

## The pattern in one sentence

With JPA, single table inheritance is @Inheritance(SINGLE_TABLE): one table, a
type column, and Hibernate building the right class for each row.

## The 5 acts

### 1. A table per class

First, JPA's table-per-class strategy: books, electronics and food each get a
table. Asking for everything under £10 returns breakfast tea and the desk
lamp, but Hibernate's SQL is a single query that unions three tables
together, and a fourth product class makes the union bigger.

### 2. One table

Now the products use `@Inheritance(SINGLE_TABLE)`. The same question returns
the same two products, and Hibernate's SQL is one plain select from the
product table.

### 3. Each row as its own class

Loading every product gives back a Book, two Electronics and a Food, each
with its own detail: the ISBN, the warranty card, the best-before date.
Hibernate chose each class from the type column, which holds BOOK,
ELECTRONICS and FOOD.

### 4. A new type

A gift card is a new kind of product: one class, GiftCard, with one field.
The product table gains one column, value_pence, and GIFT-1 loads back as a
GiftCard, ready to be activated for £50 on dispatch.

### 5. The bill

Fifteen of the twenty type-specific cells are empty. The shop wants every
book to have an ISBN, but the database refuses to make isbn NOT NULL,
because the kettle, lamp, tea and gift card rows have none. So a book with no
ISBN is saved. Putting `@Column(nullable = false)` on the field is worse: it
stopped every kettle and tea from being saved at all. The rule must live in
Java, for example with Bean Validation.

## The verdict

Use SINGLE_TABLE when types share most columns and queries span all of them.
Check the SQL Hibernate writes, keep subclass rules in Java, and move to
JOINED when empty cells start to dominate.

## How to recognise this in code you did not write

- `@Inheritance(strategy = InheritanceType.SINGLE_TABLE)`.
- `@DiscriminatorColumn` and `@DiscriminatorValue`.
- A table with a `dtype` or `type` column and many nullable columns.

## Where you have already met this

- `@Inheritance(strategy = InheritanceType.SINGLE_TABLE)` in JPA entities.
- Ruby on Rails' single table inheritance with a type column.
- Hibernate's default inheritance mapping, which is single table.
