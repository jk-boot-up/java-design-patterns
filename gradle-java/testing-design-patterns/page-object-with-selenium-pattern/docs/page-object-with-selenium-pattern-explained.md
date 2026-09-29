# Page Object with Selenium, Explained

## The pattern in one sentence

With Selenium, a page object wraps a real page's selectors and waits in one
class, so browser tests speak in shop terms.

## The 5 acts

### 1. Selectors in the test

A test drives the real checkout page by its selectors: it types SAVE10, clicks
#apply-btn and reads #total straight away. It sees 50.00. The coupon was
accepted, but the page's JavaScript updates the total 300 milliseconds later,
and the test read it too soon.

### 2. A button is renamed

The designers rename the button from #apply-btn to #apply-coupon. Five coupon
tests each named the old selector. In the real browser, each fails with
Selenium's NoSuchElementException: zero of five pass.

### 3. A Page Object

Now CheckoutPage is the only class that knows the page. Its applyCoupon types
the code, clicks the button, and waits with WebDriverWait until the status
text appears. After the rename, one selector was changed in that class, and
all five tests pass, each reading a total of 45.00.

### 4. Return the next page

Placing the order moves the real browser to the confirmation page, and
placeOrder returns its page object, ConfirmationPage, which waits for it and
shows order ORD-1042 with the thank-you message.

### 5. The bill

Every page needs its object, kept in step with the real page, and the checks
stay in the tests: page objects report, tests decide. And real browser tests
are slow: this demo started a browser in a container, and every page load was
real.

## The verdict

Use page objects for every browser test suite that shares pages. Keep
selectors and waits inside them, wait for real conditions, return the next
page from navigation, and keep the checks in the tests.

## How to recognise this in code you did not write

- Classes named ...Page holding By selectors.
- WebDriverWait inside page methods, not in tests.
- Methods that return another page object after a click.

## Where you have already met this

- Selenium's own documentation, which recommends page objects.
- Playwright and Cypress projects organised into page classes.
- The Screenplay pattern, a later refinement.
