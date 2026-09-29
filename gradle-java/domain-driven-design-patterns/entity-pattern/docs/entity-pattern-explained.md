# Entity, Explained

## The pattern in one sentence

An entity is an object defined by an identity that never changes, compared by
that identity alone, so it stays the same thing while its details change.

## The 5 acts

### 1. Defined by values

`CustomerRecord` is a record, compared by all its fields. When Priya changes
her email, the new record is not equal to the old one. Her orders, stored
under the old record, cannot be found with the new one, and a set of
customers now contains two Priyas.

### 2. Defined by identity

`Customer` has a `CustomerId`, set when the account is opened. Its `equals`
and `hashCode` use only the ID. Priya changes her email and is still `C-17`:
her orders are found, and the mailing list holds one customer.

### 3. Look-alikes are different

A father and son are both called Tom Reed and share a family email. As
records they are equal, so the shop would merge their orders. As entities
they are `C-42` and `C-43`: different customers, however alike they look.

### 4. A life story

An entity is followed through time. Priya's history shows the account opened
with her old email, then two changes. She has earned 80 points. Through all
of it, her ID stayed `C-17`.

### 5. The bill

Equal is not the same as up to date. A copy of Priya made for a cache and the
live customer are equal, because they share `C-17`, even though the copy still
has her work email and the live one her final email. And every entity needs an
ID that is unique and never reused.

## The verdict

Model things the business follows individually through time as entities:
customers, orders, parcels. Give each a never-changing ID, compare by it, and
keep everything else in value objects.

## How to recognise this in code you did not write

- A final `id` field and `equals` that compares only it.
- `@Entity` and `@Id` in JPA code.
- Methods that change details (`changeEmail`) but never the ID.

## Where you have already met this

- JPA `@Entity` classes with an `@Id` field.
- Database primary keys.
- `equals` and `hashCode` written over an ID field only.
