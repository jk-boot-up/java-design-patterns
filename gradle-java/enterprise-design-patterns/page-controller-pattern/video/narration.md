# Page Controller Pattern — Video Narration Script

## 1. Page Controller

Hello, and welcome. This video explains the Page Controller pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A page controller is a small class for one page of a web site. It reads that page's input, decides what to do, and sends the reply. Every page gets its own. Think of a department store with a separate desk for each service. A returns desk, a gift-wrapping desk, a café till. Each knows only its own job. But a store-wide rule has to be taught at every desk. In this video, the domain is an online shop's web site. It has a product page, a basket, and a checkout, served by a real web server running on the same computer. By the end, you will hear how one handler for every page lets changes leak. How page controllers fix it. How to add a page. And the check that gets forgotten.

## 2. The Scenario

Here is the scenario. The shop's web site has three addresses. Product shows a product. Basket adds something to the basket. Checkout takes payment. All three were served by one handler. One long method, that looked at the address and chose what to do.

## 3. Act One — One handler for every page

First demo: one handler for every page. The product page, the basket, and every other address go through one long method. Someone added a line at the top, to read the quantity, for the basket. The basket works: two mugs. But the product page has no quantity. It now fails with a server error. A change for one page broke another.

## 4. Act Two — A controller per page

Second demo: a page controller for each page. The product page has its own small class. So does the basket. So does checkout. The web server sends each address to its controller. The product page shows the steel kettle, thirty pounds. The basket takes two mugs. Both work.

## 5. Act Three — Errors stay on their page

Third demo: each page handles its own input, and its own errors. A customer asks for a product that does not exist. The product page answers four oh four: no such product. Someone types the word two as a quantity. The basket answers four hundred: quantity must be a number. And the product page for the mug still works.

## 6. Act Four — A new page

Fourth demo: a new page is a new class, and one line. The shop adds a reviews page. One new controller, and one line telling the server about it. The reviews page answers: four point five stars, from twelve customers. No other controller was touched.

## 7. Act Five — The bill

Fifth demo: the bill. Checks that every page needs are written in every controller. A visitor who is not logged in opens the basket. Four oh one: please log in. The same visitor opens checkout. Two hundred: pay with the card on file. Checkout's author forgot the login check. The Front Controller pattern exists to fix exactly this.

## 8. The Pattern

Let's name the pattern. Give each page its own small controller. The controller reads that page's input. It makes that page's decisions. And it sends that page's reply. The web server keeps a simple map: this address goes to that controller.

## 9. Who Does What

Here is who does what. The JDK's built-in web server maps each address to a controller. Product controller serves the product page. Basket controller serves the basket, and checks the login. Checkout controller serves checkout. And one handler is the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern already. Classic web sites with one JSP or PHP file per page are page controllers. So are servlets mapped one per address. And Spring M V C controller classes, with a method for each page, are the modern form.

## 11. When To Use It

So, when should you use it? For simple sites, where the pages are mostly independent. As soon as many pages share checks, logging, or layout, move those into a front controller, or into filters. Then they run for every page, and cannot be forgotten.

## 12. Thanks for Watching

That's the Page Controller pattern. If you remember one sentence, make it this one. One small controller per page, and each page looks after itself. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add the missing login check to checkout, and a test that proves it. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
