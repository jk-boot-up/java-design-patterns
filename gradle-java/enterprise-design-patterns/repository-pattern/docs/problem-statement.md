# Problem Statement

## The scenario

Find customers in London who have ordered in the last month.

## The naive version: SQL in the service

The query is written where it is needed. For one query in one place, that is
fine. Here the same question is asked from three services.

```
ONE. SQL in the service — the same question, asked three ways.
  marketing: [Ada, Grace]
  support:   [Ada, Grace, Ken]
  reports:   [Ada, Grace]
  three answers to one question. support is off by one day.
```

Then the schema changes. The column `city` becomes `town`, and every string
in the codebase that names it has to be found by hand.

```
TWO. A schema change — every string that names a column.
  marketing: []
  support:   []
  reports:   []
  nothing threw. every list is empty.
```

## What this project must deliver

An interface that looks like a collection of customers, which the service uses
without knowing a database exists. It must show swapping the store with no
change to the caller, and admit the costs.
