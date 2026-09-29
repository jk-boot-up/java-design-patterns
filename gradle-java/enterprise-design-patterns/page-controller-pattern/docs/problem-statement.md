# Problem Statement

## The scenario

The shop's web site has a product page, a basket and a checkout, served over
HTTP.

## The naive version

`OneHandler` serves every page from one method. Code added at the top for one
page (quantity parsing for the basket) runs for all of them, and the product
page fails with a 500.

## What this project must deliver

- The shared-method failure shown: a 500 on the product page.
- One controller per page, registered with the JDK's HTTP server.
- Input errors answered by the page they belong to (404, 400).
- A new page added as one class and one line.
- The cost shown: a forgotten login check on checkout.
- Every response asserted by a test, over real HTTP on localhost.
