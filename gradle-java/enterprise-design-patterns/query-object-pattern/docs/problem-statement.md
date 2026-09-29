# Problem Statement

## The scenario

Customers filter products by category, maximum price and part of the name,
any of which may be left empty.

## The naive version

`StringSql` glues SQL together from strings: an empty category gives `WHERE
AND`, and the customer's text is pasted into the SQL.

## What this project must deliver

- Broken SQL and an unescaped apostrophe shown.
- Criteria that produce placeholders and a separate list of values.
- The same query run over a list in memory.
- A saved query extended without being changed.
- Every printed result asserted by a test.
