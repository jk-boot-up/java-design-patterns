# Problem Statement

## The scenario

Many small tests check the shipping rules, and each needs an order with a
customer, a country, lines and options.

## The naive version

Building every order by hand makes tests long, hides what matters, and breaks
every test when a constructor changes.

## What this project must deliver

- A hand-built order and what it costs.
- An Object Mother of named orders.
- The mother's explosion of combinations.
- A Test Data Builder with defaults and one method per detail.
- The hidden-default trap and its fix.
- A real test class written with the builder.
