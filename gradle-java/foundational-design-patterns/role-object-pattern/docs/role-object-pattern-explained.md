# Role Object, Explained

## The pattern in one sentence

A role object keeps one core object for an identity and models each activity
it performs for a while as a separate object that can be added and removed.

## The 5 acts

### 1. A subclass per kind

`Customer` holds Priya's twelve orders. When she opens a shop, the code creates
a `SellingCustomer`, a different object: it has zero orders, and it is not the
same object as her customer record. With three kinds of role (buyer, seller,
affiliate), every combination needs its own class: seven of them.

### 2. One account, many roles

`Account` holds the identity: `C-17`, Priya. A `Buyer` role holds her twelve
orders. When she opens a shop, a `Seller` role is added to the same account.
She now plays both roles, and all twelve orders are still there.

### 3. Roles with behaviour

Each role has its own data and methods. The `Seller` role lists a hand-thrown
mug under the shop name "Priya's Pottery". An `Affiliate` role is added at
five percent; she refers orders of £40 and £60 and earns £5.00. `Account`
itself knows nothing about shops or commission.

### 4. Dropping a role

The marketplace suspends Priya's selling. The `Seller` role is removed; her
roles are now buyer and affiliate. Trying to list another mug is refused:
"Priya is not a seller". She can still buy, and places her thirteenth order.

### 5. The bill

Every caller has to ask for a role before using it, and decide what to do when
the answer is no. And the data is spread out: her name lives on the account,
her shop name lived on a role that is now gone.

## The verdict

Use it when roles come and go during an object's life, combine freely, and
bring their own data and behaviour. Keep identity on the core, give each role
its own data, and decide what should happen to that data when a role is
removed.

## How to recognise this in code you did not write

- A core `Party`, `Person` or `Account` with a collection of roles.
- Methods like `as(Role.class)`, `getRole(...)` or `hasRole(...)`.
- Roles that keep a reference back to their core.

## Where you have already met this

- User accounts with roles such as customer, seller and admin in marketplaces.
- Party and PartyRole models in enterprise data, where a person or company plays customer, supplier and employee.
- Actors and their roles in UML and in games.
