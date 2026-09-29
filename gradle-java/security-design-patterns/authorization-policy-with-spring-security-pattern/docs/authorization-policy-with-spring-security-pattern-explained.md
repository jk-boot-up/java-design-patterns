# Authorization Policy with Spring Security, Explained

## The pattern in one sentence

With Spring Security, an authorization policy is URL rules that deny by
default plus @PreAuthorize rules beside each endpoint, with refusals
published as events.

## The 5 acts

### 1. Signed in is enough

The old view endpoint only asks that the user is signed in; it was meant to
check the owner itself and forgot. Ana, a customer, asks for ben's order
ORD-7 and gets it: HTTP 200.

### 2. Roles only

A URL rule requires the customer role for viewing orders. Ana has it, so ana
still sees ben's order: HTTP 200. A role can say "customers may view orders",
but not "their own orders".

### 3. Rules beside each endpoint

Now each endpoint carries its own rule. Viewing requires the owner, checked by
the order policy bean, or support, or admin: ana gets 403 on ben's order, ben
gets 200. Refunds require admin, or support with an amount up to 100: sam
refunds 80 but not 250, and alex, an admin, refunds 250.

### 4. Deny by default

A developer added an export endpoint and wrote no rule for it. The URL rules
end with `anyRequest().denyAll()`, so even alex, an admin, is refused: HTTP
403. A new endpoint starts closed until someone decides who may use it.

### 5. The bill

Spring Security announced the three refusals as events, once a publisher was
configured; before error dispatches were permitted, each refusal was counted
twice. The rules are strings in Spring's expression language, checked only
when they run, so a typo fails at the first request, not at build time. And a
rule on one method protects only that method, which is why `denyAll()` must
close everything else.

## The verdict

Use URL rules for broad access and end them with denyAll(); put detailed rules
beside each endpoint; keep shop facts in a named policy bean; publish
refusals; and test every rule, because they are checked only at run time.

## How to recognise this in code you did not write

- `authorizeHttpRequests(...).anyRequest().denyAll()`.
- `@PreAuthorize("hasRole('ADMIN') or ...")`.
- `@EnableMethodSecurity` on a configuration class.

## Where you have already met this

- `@PreAuthorize` and `hasRole` in Spring applications.
- `authorizeHttpRequests` blocks in `SecurityFilterChain` beans.
- Policy engines such as Open Policy Agent, for rules kept outside the code.
