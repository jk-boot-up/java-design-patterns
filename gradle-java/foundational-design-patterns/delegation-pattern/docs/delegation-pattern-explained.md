# Delegation, Explained

## The pattern in one sentence

Delegation is when an object does not do a job itself, but hands it to a helper object that it holds, and that it can swap.

## The six acts

### A Subclass For Each Way

Premium, gift wrap, and both: four classes for two features. A third feature would need eight. A premium gift order is ninety six hundred. And an order cannot change its class once it exists.

```
  premium, gift wrap, and both: 4 classes for 2 features. a third feature would need 8.
  premium and gift order: 9600. and an order cannot change its class once it exists.
```

### The Order Hands The Pricing On

One order class. With no rule, ten thousand. With premium, nine thousand. With gift wrap, ten thousand six hundred.

```
  one Order class. no rule 10000, premium 9000, gift wrap 10600.
```

### Change The Helper While It Lives

The customer joins the premium plan while shopping. The same order object: ten thousand, then nine thousand.

```
  the customer joins the premium plan while shopping. the same order object: 10000 then 9000.
```

### Two Helpers At Once

Premium then gift wrap: ninety six hundred, the same as the class made for both. Classes added: none.

```
  premium then gift wrap: 9600, the same as the class made for both. classes added: 0.
```

### The Helper Needs To See The Order

Gift wrap is three hundred for each item, so it must look at the order it was called for. Two items: ten thousand six hundred. Three items: ten thousand nine hundred. That is why the order passes itself in: the helper is a different object, and does not know which order it is helping.

```
  gift wrap is 300 for each item, so it must look at the order it was called for. 2 items: 10600. 3 items: 10900.
  that is why the order passes itself in: the helper is a different object, and does not know which order it is helping.
```

### The Bill

One total made three calls to helpers, where inheritance made none: one more hop for every helper. To look like a helper with four methods, the order had to write four forwarding methods that only pass the call on. And a helper knows nothing of its owner unless it is told.

```
  one total() made 3 calls to helpers, where inheritance made none: one more hop for every helper.
  to look like a helper with 4 methods, the order had to write 4 forwarding methods that only pass the call on.
  and a helper knows nothing of its owner unless it is told: it cannot call a method on the order that the order did not pass in.
```

## The verdict

Prefer holding a helper to inheriting from a parent, when what varies is one job. Pass the owner in if the helper needs it. Let the helper be swapped, and combined. Accept the extra hop, and the forwarding code, or use a language feature that writes it for you.

## How to recognise this in code you did not write

- A field of an interface type, and a method that just calls it.
- Strategy, State, Decorator and Proxy, which are all delegation with a purpose.
- Kotlin's `by` keyword, and Lombok's `@Delegate`.
- `Collections.unmodifiableList`, which hands each call to a list it holds.

## Where you have already met this

Almost every framework's plugin points, Java's `Iterator` and `Comparator` in use, and the phrase composition over inheritance.

## When this is too much

If there is one fixed way of doing a job, do it directly. Delegation pays off when a job varies, or must change at run time.
