# Page Controller, Explained

## The pattern in one sentence

A page controller is a small class for one page or action of a web site that
reads that page's input, decides what to do and sends the reply.

## The 5 acts

### 1. One handler for every page

`OneHandler` serves every address from one method. Quantity parsing was added
at the top for the basket. The basket answers `200 basket: 2 x MUG-1`, but the
product page has no quantity, and now returns `500 server error:
NumberFormatException`.

### 2. A controller per page

Each address now has its own controller, registered with the JDK's web server:
`/product` to `ProductController`, `/basket` to `BasketController`,
`/checkout` to `CheckoutController`. The product page shows the kettle, and
the basket takes two mugs.

### 3. Errors stay on their page

Each controller reads and checks its own input. An unknown product gives
`404 no product SOFA-9`, from the product controller only. A quantity of "two"
gives `400 quantity must be a number`, from the basket only. The product page
for the mug still answers 200.

### 4. A new page

A reviews page is added: one new class, `ReviewsController`, and one line
registering `/reviews`. No other controller is opened, and the page answers
"4.5 stars from 12 customers".

### 5. The bill

Checks that every page needs are written in every controller. The basket
repeats the login check and answers `401 please log in`. The checkout
controller's author forgot it, so checkout answers 200 to a visitor who is not
logged in. Front Controller exists to fix exactly this.

## The verdict

Use page controllers for simple sites whose pages are mostly independent. As
soon as many pages share checks, logging or layout, move those into a Front
Controller or filters so they cannot be forgotten.

## How to recognise this in code you did not write

- One class or file per URL: `ProductController`, `product.jsp`, `product.php`.
- `createContext("/basket", ...)` or one servlet per path.
- The same login check at the top of many controllers.

## Where you have already met this

- Classic JSP and PHP pages, where each file handles one page.
- Servlets mapped one per URL in `web.xml`.
- Spring MVC `@Controller` classes with one handler method per page.
- `HttpServer.createContext(path, handler)` in the JDK.
