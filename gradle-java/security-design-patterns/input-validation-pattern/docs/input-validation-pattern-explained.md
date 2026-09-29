# Input Validation, Explained

## The pattern in one sentence

Input Validation checks everything from outside at the boundary, against
rules for what is allowed, before the program uses it.

## The 5 acts

### 1. Trusting the form

Checkout reads the quantity as a number and multiplies. A quantity of minus
five mugs at 9.99 gives a total of minus 49.95: the shop would pay the
customer. And "not-an-email" is saved as the customer's email address,
because nobody checked it.

### 2. Check at the boundary

Now every field is checked where it enters the program, against rules for
what is allowed: a product code shaped like MUG-12, a whole-number quantity
from 1 to 99, and a plausible email address. A bad form gets all three
problems reported at once, so the customer can fix them together. A good form
is accepted, with a total of 19.98.

### 3. Types that cannot be wrong

Each field becomes a small type that checks itself when it is made. Trying to
make a `Quantity` of minus five fails. Checkout takes a `ValidOrder`, built
only from such types, so it never needs to check again: if it has one, every
value in it is valid.

### 4. Encode on the way out

A product review says "Lovely mug", followed by a script tag. Shown on the
page as typed, the browser would run the script in every shopper's browser.
Shown with its angle brackets encoded, the page displays the text instead of
running it. Validating input and encoding output are two different jobs, and
both are needed.

### 5. The bill

Rules must be fair. A rule allowing only plain A to Z letters rejects a real
customer called Siobhán O'Brien. A rule for letters in any alphabet, with
apostrophes and hyphens, accepts that name. And checks in the browser are only
a convenience: a request sent without the browser skips them, so the server
must always check.

## The verdict

Check every outside input on the server, with allow-list rules that are
strict about harm and fair to real people. Parse into self-checking types,
report all problems together, and encode text for wherever it is shown.

## How to recognise this in code you did not write

- `@Valid`, `@NotBlank`, `@Min` and `@Pattern` annotations.
- Value types that throw from their constructors.
- HTML templates that escape output by default.

## Where you have already met this

- Jakarta Bean Validation annotations such as `@Min`, `@Email` and `@Pattern`, and Spring's `@Valid`.
- Value objects in Domain-Driven Design that check themselves when created.
- The OWASP Input Validation and Cross-Site Scripting cheat sheets.
