# Authorization Policy, Explained

## The pattern in one sentence

An Authorization Policy makes every access decision in one place, from rules
over roles and attributes, and denies whatever no rule allows.

## The 5 acts

### 1. Checks in every endpoint

Each endpoint checks access in its own code. Ana cannot cancel Ben's order:
that endpoint checks the owner. But Ana can view Ben's order, because the view
endpoint forgot the owner check. And Sam from support can refund 250, because
the refund endpoint only checks the role, not the limit of 100.

### 2. Roles only

A first step is role-based access control in one place: customers may view
and cancel orders; support may view orders and issue refunds. But Ana still
may view Ben's order, because her role has "view order". A role can say
"customers may view orders", but it cannot say "their own".

### 3. Rules on attributes

Now each rule can look at details: who the user is, who owns the order, and
the refund amount. This is attribute-based access control. Ana is denied
Ben's order; Ben is allowed, as the owner. Sam may refund 80 but not 250, and
Alex, an admin, may refund 250. Each decision carries the rule that allowed
it.

### 4. Deny by default

A developer adds an endpoint to export orders. Nobody has written a rule for
it, so even Alex the admin is denied. Anything no rule allows is refused, so
a new endpoint starts closed and is only opened on purpose.

### 5. The bill

Every request now asks the policy, and every decision is logged with its
reason: six so far. That is useful for audits, but the policy is now on every
request's path, so it must be fast and always available. And as rules grow,
they must stay readable and thoroughly tested.

## The verdict

Use a central policy as soon as different users may do different things.
Start with roles, add attribute rules for ownership and limits, deny by
default, log each decision, and test the policy like any other critical code.

## How to recognise this in code you did not write

- `@PreAuthorize("hasRole('ADMIN')")` and similar annotations.
- Calls such as `policy.check(user, action, resource)`.
- Rego or Cedar policy files kept beside the code.

## Where you have already met this

- Spring Security's `@PreAuthorize` and its `AuthorizationManager`.
- Open Policy Agent (OPA) and AWS Cedar, policy engines with their own rule languages.
- Cloud IAM policies: who may do which action on which resource.
