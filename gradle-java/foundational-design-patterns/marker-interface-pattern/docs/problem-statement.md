# Problem Statement

## The scenario

Products need different care in transit: cold, padded, or nothing special.

## The naive version

`TaggedProduct` stores care instructions as free text. A capital letter or a
typo means the packer misses the tag, and dairy goes out warm.

## What this project must deliver

- Tags shown failing on case and spelling.
- Empty marker interfaces and a packer that reads them.
- A method that only accepts perishable items, checked by the compiler.
- A mark inherited by a subclass.
- The limits shown: no values, no removal.
- Every printed result asserted by a test.
