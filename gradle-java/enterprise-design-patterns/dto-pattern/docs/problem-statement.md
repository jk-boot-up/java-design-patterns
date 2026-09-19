# Problem Statement

## The scenario

A REST endpoint returns a customer.

## The naive version: return the domain object

Whatever the domain object holds goes out. This project's small JSON writer
walks every field, exactly as a real serialiser does.

```
ONE. A REST endpoint returns the domain object.
  contains the password hash: true
  order history in it: true, history loaded 1 time, just to serialise
  size: 5297 characters, for a customer's name and city.
```

The password hash is in it. The whole order history is in it, because
serialisation touched the lazy collection. It is enormous. And the keys are
the names of private fields.

```
TWO. The field name the client depends on is a private field.
  a developer renames the private field name to fullName.
  the client reads the key "name": null
```

## What this project must deliver

A separate object for the boundary, and an honest account of its cost.
