# Session Guide — Table Data Gateway with JdbcTemplate Pattern

## Learning Objectives

By the end of the session you can:

- Write a table data gateway with NamedParameterJdbcTemplate.
- Map rows to records with DataClassRowMapper.
- Explain why JdbcTemplate cannot leak connections.
- Catch Spring's translated exceptions.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Hand-written JDBC that leaks | 7 min |
| 0:17 | Act 2: A gateway on JdbcTemplate | 7 min |
| 0:24 | Act 3: Errors that mean something | 7 min |
| 0:31 | Act 4: Stock in one statement | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run`. Compare act one's failed third page with act two's four
requests. Open `ProductGateway`: every method is one call. Open
`ScatteredJdbc`: the missing close.

## Exercises

1. Add a method for products low on stock, and discuss where "low" belongs.
2. Use SimpleJdbcInsert for the insert.
3. Point the gateway at PostgreSQL and check the same exceptions come back.
