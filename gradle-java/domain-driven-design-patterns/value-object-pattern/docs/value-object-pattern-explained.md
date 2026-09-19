# Value Object, Explained

## The pattern in one sentence

A value object is a small object defined entirely by its contents, never changed after it is made, and refused when it would be made wrong.

## The six acts

### Money As A Double

Prices as doubles give 3.3000000000000003 for three stamps at 1.10. Ten pounds and ten dollars add up to 20 with no complaint, because the number does not know what it counts.

```
  three stamps at 1.10: 3.3000000000000003.
  0.1 + 0.2 == 0.3: false.
  ten pounds added to ten dollars: 20.0.
  the number has no idea what it is a number of.
```

### Money As A Value

Whole pence multiplied by three give exactly 330. Adding pounds to dollars is refused with a clear message.

```
  three stamps at GBP 1.10: GBP 3.30.
  ten pounds plus ten dollars: refused, cannot combine GBP with USD.
  the amount and its currency travel together.
```

### Equal By Value

Three separate objects of five pounds collapse to one in a set, because equality is by value. A class that compares by identity keeps all three.

```
  three separate objects of 5.00, in a set: 1.
  the same with a class that compares by identity: 3.
  true for two 5.00s, and false for 5.00 and 5.00 dollars.
```

### Never Changed

A mutable price shared by two orders lets one order's discount change the other's price. With values, each discount produces a new amount and the original is untouched.

```
  a mutable price shared by two orders. order B takes 5.00 off. order A now costs: 1500 pence, not 2000.
  the same with values: order B pays GBP 15.00, order A still pays GBP 20.00.
```

### Valid From The Start

Three methods take an email as a string. Two check it, and the third, written last, does not, so a bad address is stored. An EmailAddress cannot be built wrong, so no method that receives one ever checks.

```
  strings: two methods checked, the third did not. stored: [ada@example.com, not an email].
  an EmailAddress: not an email address: not an email. it cannot be built wrong.
  a method that receives an EmailAddress never checks. ada@example.com.
```

### Splitting Is A Decision

Ten pounds split three ways by rounding loses a penny. Allocation gives the odd penny to the first share, and the shares add to exactly ten pounds.

```
  ten pounds three ways, rounded: 3.33 + 3.33 + 3.33 = 9.99. a penny vanished.
  allocated: [GBP 3.34, GBP 3.33, GBP 3.33], adding up to GBP 10.00.
  the type has to say who gets the odd penny. that is a rule, and it lives in one place.
```

## The verdict

Use a value object for anything that has a meaning beyond its raw value: money, an email, a date range, a quantity with a unit. Make it a record, validate in its constructor, and give it the operations that belong to it. Do not wrap every string.

## How to recognise this in code you did not write

- A record or final class with no setters and `equals` written by value.
- A constructor that throws on bad input.
- Methods that return a new instance, such as `plus` and `withName`.
- `java.time` and `BigDecimal`, which are value objects the JDK gave you.

## Where you have already met this

`java.time.LocalDate`, `BigDecimal`, `UUID`, `String`. Every one of them is defined by its contents, never changes, and is compared by value.

## When this is too much

For a value that means nothing beyond its raw type, such as a loop counter or a name shown on a screen, a wrapper is noise. It earns its place where mistakes are expensive and rules exist.
