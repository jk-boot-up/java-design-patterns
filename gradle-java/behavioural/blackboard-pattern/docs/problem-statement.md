# Problem Statement

## The scenario

Before accepting an order, the store runs six fraud checks: card country, IP
country, whether they match, orders in the last hour, order value, and a slow
device check.

## The naive version

`FraudCheckAll` runs every check in a hand-written order, every time. It spends
902 milliseconds on an order whose answer was clear after 102, and every new
check means editing it.

## What this project must deliver

- The fixed method shown spending 902 ms, 800 of them unneeded.
- Checks as independent knowledge sources that declare what they need and add.
- A controller that runs the cheapest ready check and stops at the rejection line.
- A new check added without changing any other code.
- Every printed result asserted by a test.
