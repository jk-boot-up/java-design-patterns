# Dependencies

This project uses JPA with Hibernate through Spring Boot, which the plain Java
version of Single Table Inheritance does not. Skipping it loses none of the
pattern: the plain version teaches all of it with nothing installed.

## What JPA and Hibernate is

JPA, Jakarta Persistence, is the Java standard for storing objects in tables with annotations. @Entity marks a class as stored. @Inheritance chooses how a class hierarchy maps to tables: SINGLE_TABLE, JOINED or TABLE_PER_CLASS. @DiscriminatorColumn names the type column, and @DiscriminatorValue gives each class its value. Hibernate is the JPA implementation that creates the tables and writes the SQL; a statement inspector sees every statement before it is sent.

## What Spring Boot and H2 is

Spring Boot starts Hibernate and a database from a few properties. H2 is a small database that can run entirely in memory.

## Why this project uses them

The plain version writes the SQL by hand. This version shows how most Java
code gets single table inheritance, from one annotation, and what the SQL
behind it looks like.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| Spring Boot (data-jpa starter, H2) | 4.1.1 |

## What it costs

- Annotations whose effect on the schema must be checked.
- SQL that is written for you, and must be looked at to understand.
