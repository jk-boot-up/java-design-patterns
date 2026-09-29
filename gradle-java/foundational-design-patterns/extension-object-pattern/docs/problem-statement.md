# Problem Statement

## The scenario

The store sells e-books, electricals, mugs and, soon, subscriptions. Each
needs different extra information and actions after payment.

## The naive version

`FatProduct` has a field for every feature. A mug leaves five of eight empty,
and every new feature is another field in the class the whole shop depends on.

## What this project must deliver

- The fat class shown: 8 fields, 5 empty for a mug.
- A 3-field core product with roles attached per object.
- Checkout acting on the roles it finds and ignoring the rest.
- A new role added with no change to the product class.
- The cost shown: a missing role that compiles and delivers nothing.
- Every printed result asserted by a test.
