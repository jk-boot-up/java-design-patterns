# Problem Statement

## The scenario

An order is loaded, and its customer is loaded with it. Separately, the
caller loads the same customer by id. It is one row in the database.

## The naive version: a new object every load

Every load builds a new object. Correct for a single caller. With two
callers, there are two objects that both claim to be customer 7.

```
ONE. Two loads, two objects.
  same object (==): false
  3 selects: the order, its customer, and the same customer again.
```

Change the address on one, change the email on the other, and save both.
Each save writes the whole row, so the second save overwrites the first.

```
TWO. The lost change.
  stored address: 12 Mill Lane, Leeds
  stored email:   ada@newmail.example
  the address change silently disappeared: last writer wins.
```

Overriding `equals()` looks like a fix and is not one. The two objects are
equal, and still separately changeable.

## What this project must deliver

One object per row per session, so that asking twice gives the same object.
It must also admit what that costs: the map is a cache and can be stale,
it holds references, and its scope is a decision with consequences.
