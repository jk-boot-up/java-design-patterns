# Problem Statement

## Read the partner first

This project assumes [Feature Toggle](../feature-toggle-pattern), which put gift wrap behind a table of switches read at run time, and showed it deployed dark, switched on for some customers, turned off by a kill switch, and safe when the table cannot be read. Nothing here is lost by skipping flagd and OpenFeature, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: gift wrap in the checkout, with a bug nobody has found yet.

## What is new

**flagd**, the OpenFeature flag daemon, in a Docker container, reading its flags from a file it watches, and answering over HTTP.

```
  gift wrap goes live by deploying it: 1 deploy. it has a bug, so taking it away is another: 2 deploys.
  each deploy ships every other change waiting in the branch too.
```

## The failure this project exists to show

Every flag check is now a network call to another process. The flags file is another thing to keep right. And a settled flag stays in the file until someone removes it.
