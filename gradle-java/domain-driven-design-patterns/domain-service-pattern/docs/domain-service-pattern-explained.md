# Domain Service, Explained

## The pattern in one sentence

A domain service is a stateless class, named in business language, that holds
a rule involving several domain objects and belonging to none of them.

## The 5 acts

### 1. The rule, copied twice

`Copies.webCheckout` has the current rule: the gold discount (£6) and the
coupon (£5) do not add up, so the bigger one wins, and Priya pays £54.00.
`Copies.phoneApp` has an older copy that applies both, and charges £49.00. Same
customer, same basket, same coupon, two prices.

### 2. A domain service

`PricingService.price(customer, basket, coupon)` holds the rule, once, in the
domain. The web checkout and the phone app both call it, and both say £54.00.

### 3. In the shop's words

The service returns the price with its reason: "subtotal £60.00; gold 10%
-£6.00 beats SAVE5 -£5.00". It needs the customer, the basket and the coupon,
and belongs to none of them alone, which is exactly why it is a service.

### 4. One service, every case

The same service object prices five combinations: a standard customer with
and without the coupon (£60.00, £55.00), a gold customer with and without it
(£54.00 both), and a £30 basket where the coupon does not apply (£30.00). It
keeps nothing between calls.

### 5. The bill

The basket still works out its own subtotal, £60.00: that fact is its own.
Moving it into a service as well would leave the basket a bag of data with no
behaviour, the "anemic domain model" that too many services produce.

## The verdict

Put a rule on an entity or value object when it belongs to one. Give it a
domain service only when it spans several, keep the service stateless and
well named, and keep workflow steps in application services.

## How to recognise this in code you did not write

- Stateless classes in the domain package named after an activity or policy.
- Methods that take two or more entities or values and return a decision.
- No fields other than other services.

## Where you have already met this

- Pricing, tax and shipping calculators that take several objects.
- Transfer services that move money or stock between two entities.
- Classes named after a business activity: `PricingService`, `RefundPolicy`.
