# Data Mapper, Explained

## The pattern in one sentence

A mapper class moves data between a domain object and its database rows,
so the object never knows it is stored.

## Active Record first, fairly

`ActiveRecordCustomer` is one class, one table, and `save()` reads like
what it does. For a small application that is simple and correct. Nothing
here says otherwise.

## Why it stops being enough

The class knows table and column names, so a schema change is a change to
the domain object. It holds a database, so a domain rule needs a database
to test. And one class per table cannot describe a customer stored across
`customers` and `addresses`, or a `customers` table that also feeds a
smaller summary object.

## The pattern

`CustomerMapper` reads and writes both tables and builds a `Customer`.
`Customer` has fields and behaviour and nothing else. The demo prints its
fields and methods to prove it.

```
FOUR. The pattern — the mapper knows the rows; the customer does not.
  Customer's fields: address email id loyaltyPoints name
  no table, no column, no SQL, no database.
```

One `find` costs one select per table, and the demo prints them:

```
    SELECT customers id=1
    SELECT addresses id=1
```

## The bill

**A second class per entity.** Every domain object gets a mapper beside it.

**The mapping is hand-written and easy to get subtly wrong.** A mapper
that forgets the postcode succeeds on every call. The postcode is simply
never stored.

```
FIVE. The bill — a hand-written mapping can lose a field silently.
  saved postcode:  LS1 4AB
  loaded postcode: null
```

**Loading a graph means deciding how far to go.** That is the Lazy Load
project's problem.

**An indirection to understand.** You must know the mapper exists before
you can debug a wrong value.

## Where you have already met this

A JPA entity is the domain object, and the `EntityManager` is the mapper.
Hibernate writes the mapping code that act five shows can go wrong. If you
have ever fixed a mapping annotation because a field did not come back,
you have met act five.

## When this is too much

For a simple application with one class per table and a schema that
rarely changes, Active Record is simpler and is the right answer.
