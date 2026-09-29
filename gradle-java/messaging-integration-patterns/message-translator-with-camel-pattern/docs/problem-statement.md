# Problem Statement

## The scenario

Orders arrive as key-value text, CSV, JSON and, later, XML; the warehouse
needs one canonical order.

## The naive version

Parsing every format inside the warehouse ties it to every marketplace, and
hand-written parsers must be written and tested for each.

## What this project must deliver

- A type check that refuses raw formats at the warehouse route.
- Translator routes using Camel's CSV and JSON data formats.
- A normalizer route using `toD` to pick the translator.
- A new XML translator added as one route.
- The costs named honestly.
- Every printed result asserted by a test.
