# Page Object, Explained

## The pattern in one sentence

A Page Object wraps a page in a class that knows its selectors and timing, so
tests speak in the shop's words.

## The 5 acts

### 1. Tests click selectors

A test drives the checkout page by its selectors. It types SAVE10 into
`#coupon`, clicks `#apply-btn`, and reads `#total` straight away. It sees
50.00. The coupon was accepted, but the page updates a moment later, and the
test read the total too soon.

### 2. A button is renamed

The designers rename the apply button from `#apply-btn` to `#apply-coupon`.
Five coupon tests each named the old selector themselves. None of the five
can find the button, all five fail, and every one must be found and edited.

### 3. A Page Object

Now a `CheckoutPage` class is the only place that knows the page. Its
`applyCoupon` method types the code, clicks the button, and waits until the
page says the coupon is applied. After the rename, one selector was changed in
that class and all five tests pass. Each test just says
`applyCoupon("SAVE10")` and reads a total of 45.00.

### 4. Return the next page

Actions that move to another page return that page's object.
`checkout.placeOrder()` returns a `ConfirmationPage`, which shows order
ORD-1042 and the thank-you message. The test cannot ask the checkout page for
an order number by mistake: the methods follow the real journey.

### 5. The bill

Every page now has a class that must be kept in step with the real page. And
there is a rule to keep: page objects report what the page shows, and the
tests decide whether it is right. A page object that asserts its own results
hides what each test is checking.

## The verdict

Use page objects once several browser tests share a page. Name methods after
what a shopper does, hide waiting inside them, return the next page from
navigation, and keep the checks in the tests.

## How to recognise this in code you did not write

- Classes named `...Page` with methods like `login()` or `applyCoupon()`.
- Selectors as constants in one class, not in tests.
- Methods returning another page object after a click.

## Where you have already met this

- Selenium's documentation recommends page objects.
- Playwright and Cypress projects organised into page or component classes.
- The Screenplay pattern, a later refinement built around actors and tasks.
