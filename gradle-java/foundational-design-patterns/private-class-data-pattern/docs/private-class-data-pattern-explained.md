# Private Class Data, Explained

## The pattern in one sentence

Private class data moves the values a class must never change into a private,
unchangeable data object, so not even the class's own methods can overwrite
them.

## The 5 acts

### 1. A method changes its own figures

`LooseInvoice` keeps its total as an ordinary field. Its
`printWithStaffDiscount` method subtracts the discount from that field before
printing. The first print shows £90.00. The second takes ten percent again and
shows £81.00. The invoice, issued for £100.00, now says £81.00.

### 2. Private class data

`Invoice` keeps its number, customer and total in a private `InvoiceData`
record. The print method works out the discounted figure in a local variable.
Printed three times, it shows £90.00 each time, and the invoice still says
£100.00.

### 3. Nothing can write

`InvoiceData` is a record: its fields are final and it has no setters. The
invoice can read `data.netPence()` but has no way to write it. The loose
invoice's shortcut, assigning a new total, would simply not compile.

### 4. Working state beside the data

Not everything must be frozen. The invoice keeps an ordinary `timesPrinted`
counter beside its data, and it reads three. The figures are unchanged at
£100.00. The class decides, field by field, which values may change.

### 5. The bill

Every protected class gains a data class, and every read goes through it:
`data.netPence()` instead of `netPence`. For a class with two fields and no
risky methods, final fields alone would do.

## The verdict

Use it for classes that hold important figures alongside working state, or to
lock down a group of fields in older code. When everything should be
unchangeable, make the whole object immutable instead.

## How to recognise this in code you did not write

- A class holding a `private final SomethingData data` field.
- Records or final-field classes named `...Data`, `...State` or `...Details` inside another class.
- Getters that forward to `data.x()`.

## Where you have already met this

- Final fields grouped into a record inside a service or entity.
- Configuration objects passed into a class and kept read-only.
- The "memento" of an object's state, kept apart from the object.
