# Problem Statement

## The scenario

Sales takes orders, shipping prints labels, and the catalogue supplies prices.
Sales and shipping both need addresses and amounts of money.

## The naive version

Each context keeps its own Address, and a converter copies between them. A
flat number added in sales is dropped on the way to shipping.

## What this project must deliver

- The converter shown losing the flat.
- A two-class shared kernel used by both contexts.
- A context map written as code.
- An import check that the code matches the map.
- Every printed result asserted by a test.
