# Page Object with Selenium Pattern — Video Narration Script

## 1. Page Object with Selenium

Hello, and welcome. This video explains the Page Object pattern, with Selenium, in a real browser. This video is presented by Jayasekhar Konduru. First, a simple definition. A page object is a class for one page of a web application. It knows how to find the page's boxes and buttons, and how long the page takes to answer. So tests only say what a shopper does. Selenium is the open-source tool that drives a real web browser from code. Think of a hotel guest asking the concierge for a taxi. The concierge knows the number, and when the line is busy. In this video, the domain is an online shop's checkout page, tested in a real Chromium browser. By the end, you will hear why tests that find buttons themselves are fragile. How one class fixes a renamed button for every test. And how it waits for the page.

## 2. The Scenario

Here is the scenario. The shop has browser tests for its checkout page. Each test found the coupon box and the apply button itself. And read the total straight away. Then the designers renamed the button.

## 3. Act One — Selectors in the test

First demo: a test that finds the page's elements itself, in a real browser. It types the coupon code. Clicks apply. Reads the total, straight away. Fifty pounds. The old price. The page updates a moment later, from its own script. The test looked too soon.

## 4. Act Two — A button is renamed

Second demo: the designers rename the apply button. Five coupon tests each used the old name. The browser cannot find the button. Zero of five pass.

## 5. Act Three — A Page Object

Third demo: a page object. One class, checkout page, knows the page's elements, and waits for the page. Its apply coupon method clicks, then waits until the page has answered. After the rename, one line in that class changed. All five tests pass. The total, forty-five.

## 6. Act Four — Return the next page

Fourth demo: an action that moves to a new page returns that page. Place order returns the confirmation page. It shows the order number, O R D ten forty-two. And, thank you for your order.

## 7. Act Five — The bill

Fifth demo: the bill. Every page needs its own class, kept in step with the real page. Page objects report. Tests decide. And real browser tests are slow. A browser has to start, and every page really loads.

## 8. The Pattern, with Selenium

Let's name the pattern, with Selenium. One class for each page. It holds the page's selectors, and waits for the page with Selenium's wait. And tests call its methods, in the shop's own words.

## 9. Who Does What

Here is who does what. Checkout page applies coupons, reads the total, and places the order. Confirmation page shows the order number. The browser class runs Chromium in a container. And the shop site serves the real pages.

## 10. Where You Have Seen It

You have probably met this already. Selenium's own guides recommend page objects. Playwright and Cypress projects use page classes too. And the Screenplay pattern is a later refinement of the same idea.

## 11. When To Use It

So, when should you use it? Whenever several browser tests share a page. Keep selectors and waits inside the page object. Wait for real conditions, never fixed pauses. And keep the checks in the tests.

## 12. Thanks for Watching

That's the Page Object, with Selenium. If you remember one sentence, make it this one. Tests say what the shopper does, and one class knows how, and when. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It needs Docker running, and starts the browser for you. Here is one exercise to try. Run the same page objects in Firefox. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
