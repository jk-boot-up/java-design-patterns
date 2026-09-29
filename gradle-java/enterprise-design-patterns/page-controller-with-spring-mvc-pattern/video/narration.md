# Page Controller with Spring MVC Pattern — Video Narration Script

## 1. Page Controller with Spring MVC

Hello, and welcome. This video explains the Page Controller pattern, with Spring MVC, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A page controller gives each page of a web application its own controller. It reads that page's input, does that page's work, and handles that page's errors. Spring MVC is the open-source web framework most Java applications use. Think of a department store, with a counter for each department. Each counter answers its own questions. The front doors, where bags are checked, are shared. In this video, the domain is an online shop's pages: product, basket, reviews and checkout. By the end, you will hear why one handler for every page breaks. How Spring finds a controller for each page. And where checks every page needs should live.

## 2. The Scenario

Here is the scenario. One handler served every page of the shop. Code added for the basket ran for every page, and the product page crashed. And each new page meant editing the one handler everyone shared.

## 3. Act One — One handler for every page

First demo: one handler for every page. The basket works. But the code that reads the quantity was added at the top, for the basket. It runs for every page. The product page has no quantity. It crashes, with a server error.

## 4. Act Two — A controller per page

Second demo: a controller for each page. The product page has its own class. So does the basket. The kettle costs thirty pounds. The basket holds two mugs. Neither page knows about the other.

## 5. Act Three — Input checked by Spring

Third demo: each page's input, checked by Spring. An unknown product. Not found. A quantity written as the word two. Bad request. Spring could not turn it into a number. The basket page wrote no code for that.

## 6. Act Four — A new page

Fourth demo: a new page. Reviews are added as one new class. Spring finds it by its annotation. Four and a half stars, from twelve customers. No other page was touched.

## 7. Act Five — The bill, and an interceptor

Fifth demo: the bill. Some checks every page needs. The checkout page's author forgot the login check. Anyone can see it. Spring has a place for shared checks, called an interceptor. It is registered once, for the basket and the checkout. Not logged in. Please log in. Logged in. The checkout page.

## 8. The Pattern, in Spring MVC

Let's name the pattern, in Spring's words. A rest controller for each page, with a get mapping for its path. Spring converts each page's input, and answers bad request when it cannot. And an interceptor holds the checks many pages share.

## 9. Who Does What

Here is who does what. Product, basket, reviews and checkout each have their own controller. The login interceptor checks login, before the pages that need it. And the old front handler is the old way, one handler for everything.

## 10. Where You Have Seen It

You have probably met this already. Spring controller classes. PHP files, Java server pages, and Razor pages, one file per page. And the controllers of Django and Rails.

## 11. When To Use It

So, when should you use it? When pages grow their own input, logic and errors. Let Spring check the input. And put every shared check in one place, never in each page.

## 12. Thanks for Watching

That's the Page Controller, with Spring MVC. If you remember one sentence, make it this one. Each page its own controller, and every shared check in one place. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a wishlist page, as a new controller. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
