# Type Object, Explained

## The pattern in one sentence

A type object turns the kind of a thing into data: instead of a subclass for each kind, there is one class, and each object points at a type object that holds what differs.

## The six acts

### A Class For Each Kind

Three kinds, three classes, and they differ only in three numbers. A novel totals thirteen hundred. A gift card is a fourth kind. That is a fourth class, a new build, and a release.

```
  3 kinds, 3 classes, and they differ only in three numbers. a novel: 1300.
  a gift card is a fourth kind. that is a fourth class, a new build and a release.
```

### A Type That Is Data

One product class. A novel totals thirteen hundred, a laptop ninety six thousand, tea six twenty. Laptops can be returned after ten days, but not after twenty.

```
  one Product class. novel 1300, laptop 96000, tea 620.
  laptops can be returned after 10 days: true. after 20 days: false.
```

### A New Kind At Run Time

Types before: three. After: four. Classes added: none. A twenty five pound card totals twenty five hundred, and cannot be returned after one day.

```
  types before 3, after 4. classes added: 0. a 25 pound card totals 2500, and can be returned after 1 day: false.
```

### Change The Type, Change Every Product

Tax on tea is twenty, on coffee forty. Grocery tax is raised to ten percent, in one place. Tea is now forty, and coffee eighty.

```
  tax on tea 20, on coffee 40.
  grocery tax raised to 10 percent, in one place. tea 40, coffee 80.
```

### A Type That Inherits

An ebook states only its shipping: none. Its tax, zero, and its return days, thirty, come from book.

```
  ebook states only its shipping: 0. tax 0 and return days 30 come from book.
```

### The Bill

A typo, b o k, is found when the program runs. With a class for each kind, the typo would not compile. Laptops need a serial number checked, and a type holds data, not steps. A flag says so, but the code that checks it is still somewhere else. And every new difference between kinds is a new field, that the code must remember to read. The type has six fields already.

```
  a typo, "bok": no type named bok, found when it runs. with a class for each kind, the typo would not compile.
  laptops need a serial number checked, and a type holds data, not steps. the flag says so: requiresSerial true. the code that checks it is still somewhere else.
  every new difference between kinds is a new field, and every field is a thing the code must remember to read. the type has 6 fields already.
```

## The verdict

Use a type object when kinds differ in data, and new kinds should be added without new code. Let types inherit defaults. Where kinds differ in steps, use a strategy or a subclass. Check the name of a type early, and keep the number of fields small.

## How to recognise this in code you did not write

- A `Type`, `Kind` or `Category` object referenced by another.
- Rows in a `product_types` table, with a foreign key from `products`.
- Card, unit or enemy types in games, defined in data files.
- `Currency`, `Locale` and `Charset`, which describe things as data.

## Where you have already met this

Game engines and their monster types, product catalogues, and the ways a database row points at its type.

## When this is too much

If the kinds are few, fixed, and differ in behaviour, plain subclasses are clearer. A type object pays off when kinds are many, or added by non-programmers.
