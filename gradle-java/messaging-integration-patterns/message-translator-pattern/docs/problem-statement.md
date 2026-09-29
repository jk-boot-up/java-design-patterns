# Problem Statement

## The scenario

Orders arrive from the web form (key-value), marketplace A (CSV), marketplace
B (JSON) and, later, marketplace C (XML).

## The naive version

`Warehouse.pickOld` parses every format itself, so each new format means
changing the warehouse, and XML is refused.

## What this project must deliver

- The warehouse shown parsing every format and failing on XML.
- One translator per format producing a canonical OrderMessage.
- A normalizer that recognises and routes each format.
- A new marketplace added with one translator and one rule.
- The lost gift note shown.
- Every printed result asserted by a test.
