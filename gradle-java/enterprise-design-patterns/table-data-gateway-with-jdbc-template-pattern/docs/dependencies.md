# Dependencies

This project uses Spring's JDBC support, which the plain Java version of Table
Data Gateway does not. Skipping it loses none of the pattern: the plain
version teaches all of it with nothing installed.

## What Spring JDBC is

JdbcTemplate runs SQL for you: it borrows a connection, runs the statement, reads the results and always returns the connection. NamedParameterJdbcTemplate lets SQL use named parameters such as :sku. A row mapper turns each result row into an object; DataClassRowMapper fills a record by matching column names. Spring translates database errors into its DataAccessException family, such as BadSqlGrammarException and DuplicateKeyException.

## What HikariCP and H2 is

HikariCP is the connection pool Spring Boot uses: a fixed set of open database connections that code borrows and returns. H2 is a small database, here running entirely in memory, created from schema.sql at start.

## Why this project uses them

The plain version writes the plumbing by hand. This version shows what most
Spring code uses, and the leaks and error codes it takes off your hands.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| Spring Boot (jdbc starter, H2) | 4.1.1 |

## What it costs

- A framework to start, even for a few queries.
