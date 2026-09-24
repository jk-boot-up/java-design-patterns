# Dependencies

This project uses PostgreSQL, MongoDB, a driver for each, and Testcontainers, which the hand-built project does not. This page says what they are, why they are here, and what they cost. It comes before the first line of database code on purpose.

**Skipping this project loses none of the pattern.** The plain-Java Database per Service project in this course teaches the pattern itself in plain Java, with nothing installed.

## What PostgreSQL is

PostgreSQL, usually called Postgres, is a relational database: a separate program that keeps data in tables. Think of a spreadsheet with fixed column headings, where every row must fill in the same columns. It is asked questions in SQL, a language for asking a database questions. Three of its abilities matter here.

It can **join**: answer one question from two tables at once, by matching a value in one with a value in the other. It keeps **foreign keys**: a rule, written into the database, that a value in one table must exist in another, so it refuses a change that would break the rule. And it runs **transactions**: a group of changes that are kept together or undone together, where undoing them is called a **rollback**.

One Postgres server can hold several separate databases. This project uses two on one server: `shop`, the shared database before the split, and `orders`, the Orders service's own. Postgres will not join across two of them, even on the same server.

## What MongoDB is

MongoDB is a document database. Think of a filing drawer of filled-in forms, where each form can have its own set of boxes. Each form is a **document**: a record of named fields and their values. A drawer of them is a **collection**. There are no tables and no fixed columns, so the kettle's document can have a wattage and the mug's a capacity, and nothing has to change first.

It is asked questions with query documents rather than SQL. A **find** asks for the documents that match. An **aggregation** is a list of steps each document passes through, and one of those steps, **`$lookup`**, is MongoDB's join: for each document, attach the matching documents from another collection in the same database. If that other collection does not exist, MongoDB treats it as empty and attaches nothing, without an error. That behaviour is the headline of this project.

## What the drivers are

A driver is the library a Java program uses to talk to one kind of database over the network. The PostgreSQL JDBC driver, 42.7.13, speaks Postgres's protocol through Java's standard database interface, JDBC. The MongoDB Java driver, 5.12.0, in its synchronous flavour, speaks MongoDB's. Each service in this project has exactly one of them. The Orders service has no MongoDB driver in its hands, and the Catalog service has no Postgres connection. That is the pattern.

## What Testcontainers is

Testcontainers is a Java library that starts a container from inside your program and stops it again when you are done. It is here so that the demo owns both databases' lifetimes: `./gradlew run` brings them up, uses them, stops MongoDB on purpose in the sixth act, and takes both away. Each is reached on a random free port chosen each run. In the 2.x line each database has its own module, `testcontainers-postgresql` and `testcontainers-mongodb`.

## Why this project uses them

Because the thing the plain-Java twin could only describe — two services on two different databases, with no join between them — needs two real engines to be true. Inside one Java program both "databases" were maps, and the join was forbidden by an exception written for the purpose. Here the join cannot be written at all, the foreign key cannot reach across, the rollback stops at the edge of its engine, and one engine can be down while the other is up.

## What to install

Only a JDK, version 21, and a container runtime. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Docker, or a Docker-compatible runtime | running; 24 or later |
| PostgreSQL image | `postgres:18.6-alpine` |
| MongoDB image | `mongo:8.3.11-noble` |
| `org.postgresql:postgresql` | 42.7.13 |
| `org.mongodb:mongodb-driver-sync` | 5.12.0 |
| `org.testcontainers:testcontainers-postgresql` | 2.0.5 |
| `org.testcontainers:testcontainers-mongodb` | 2.0.5 |
| `org.slf4j:slf4j-simple` | 2.0.17 |

Every one of these is the newest generally available release; none is held back.

## What it costs

The first run pulls both images: about 300 MB for Postgres and 830 MB for MongoDB once unpacked. MongoDB has no Alpine image, which is why it is the larger. After that a run takes about twelve seconds, most of it the two databases starting. Testcontainers also runs a small helper container that removes anything left behind if the demo is killed part way through; it exits on its own a few seconds after the demo does.

In a real shop the larger cost is not disk. It is two engines to back up, upgrade, watch and learn, where there was one; two query languages in the team's heads; and every page that used to be one join now two questions and some code.

## Where this pattern lives in a real system

In each service's configuration, which holds the address and password of its own database and no other. In the database accounts, where the Orders service's login simply cannot see the Catalog's data. In the code that assembles a page from two services and decides what to show when one of them does not answer. And in the agreements between teams that replace the foreign key.
