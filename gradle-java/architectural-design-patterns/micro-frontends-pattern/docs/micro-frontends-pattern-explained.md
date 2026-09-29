# Micro-Frontends, Explained

## The pattern in one sentence

Micro-frontends split a page into parts owned and released by different
teams, and assemble the page from those parts with a fallback for each.

## The 5 acts

### 1. One front-end for everything

`OneFrontEnd.productPage` renders all three parts in one method. It works
until the recommendations section throws: then the whole product page fails,
with the basket and product details that had nothing wrong with them. Fixing
it means releasing the whole front-end, every team's code at once.

### 2. Each team serves its part

Each team now runs a small web application, `TeamApp`, that serves only its
fragment. `PageAssembler` holds the layout: three slots, product, basket and
recommendations, each filled by an HTTP request to the team that owns it. The
page looks the same as before.

### 3. Failure stays in its slot

The recommendations app fails, and then answers too slowly. Each time, the
assembler gives up on that fragment after 300 milliseconds and fills its slot
with "recommendations unavailable". The product and basket are served as
normal.

### 4. Independent releases

The basket team releases a new version of its fragment, adding "free delivery
over £40". The next page view shows it. The product and recommendations apps
were not touched, and did not need to know.

### 5. The bill

Every page view is now one page and three fragment requests, and the slowest
fragment sets the pace. And teams drift: the product team starts writing
"30.00 GBP" while the basket team writes "£38.00", and the page looks like two
different shops. A shared design system is the usual answer.

## The verdict

Use micro-frontends when several independent teams keep blocking each other's
front-end releases. Give every fragment a timeout and a fallback, share a
design system, and keep one front-end when one team owns the page.

## How to recognise this in code you did not write

- Pages assembled from includes or fragments served by different apps.
- Module Federation or single-spa in the front-end build.
- Fallback placeholders for parts of a page.

## Where you have already met this

- Server-side includes and edge-side includes (ESI) on CDNs.
- Module Federation in webpack, and single-spa, in the browser.
- Large shops and media sites where each team owns a part of the page.
