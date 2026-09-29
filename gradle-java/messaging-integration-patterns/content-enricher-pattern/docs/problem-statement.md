# Problem Statement

## The scenario

Checkout sends an "order placed" message with an order number, the items and a
customer identifier. The warehouse needs an address and the email service needs
a name, so each of them calls the customer service for every order.

## The naive version

Each receiver looks the customer up itself (`Receivers.packThin`,
`Receivers.emailThin`). It is simple, but the lookups multiply with every new
receiver, and every receiver stops working when the customer service is down.

## What this project must deliver

- The thin message printed, showing what it lacks.
- The lookup count without an enricher (6 for 3 orders and 2 receivers) and with one (2, with a cache).
- Receivers that keep working while the customer service is down, because the message carries the details.
- A problem list for orders whose customer cannot be found.
- The costs shown: a stale copy after the customer moves, and bigger messages.
- Every printed number asserted by a test.
