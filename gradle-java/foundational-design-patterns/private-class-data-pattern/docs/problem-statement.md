# Problem Statement

## The scenario

Invoices are printed, sometimes with a staff discount shown.

## The naive version

`LooseInvoice` subtracts the discount from its own stored total before
printing, so every print takes the discount again: £100, then £90, then £81.

## What this project must deliver

- The drifting total shown: £90.00, then £81.00.
- Figures held in a private record with final fields and no setters.
- Repeated prints showing the same figure while the total stays at £100.00.
- An ordinary counter kept beside the protected data.
- Every printed result asserted by a test.
