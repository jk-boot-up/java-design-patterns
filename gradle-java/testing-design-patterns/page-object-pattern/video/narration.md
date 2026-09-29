# Page Object Pattern — Video Narration Script

## 1. Page Object

Hello, and welcome. This video explains the Page Object pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Browser tests drive a web page the way a person would. A page object is a class for one page. It knows how to find the page's boxes and buttons, and how long the page takes to update. So the tests only say what a shopper does. Think of a hotel guest asking the concierge for a taxi. The guest does not need the taxi firm's number. The concierge knows it. And if the number changes, only the concierge needs to know. In this video, the domain is an online shop's checkout page, and the automated tests that check it. By the end, you will hear why tests that find buttons themselves are fragile. How one class fixes a renamed button for every test. How it hides waiting. And what it costs to keep.

## 2. The Scenario

Here is the scenario. The shop has automated browser tests for its checkout page. Each test typed the coupon code, clicked the apply button, and read the total, all by itself. Each test knew the names the page uses for those elements.

## 3. Act One — Tests click selectors

First demo: tests that click selectors themselves. A selector is the name a test uses to find a box or a button on the page. The test types a coupon code. It clicks the apply button. Then it reads the total, straight away. It sees fifty. The old price. The coupon was accepted. But the page updates a moment later, and the test looked too soon.

## 4. Act Two — A button is renamed

Second demo: the designers rename the apply button. It was called apply button. Now it is called apply coupon. Five coupon tests each used the old name. None of them can find the button. Zero of five pass. And every one must be found and edited.

## 5. Act Three — A Page Object

Third demo: a page object. One class, checkout page, is the only place that knows the page. Its selectors, and its timing. Its apply coupon method types the code, clicks the button, and waits until the page has updated. After the rename, one line in that class changed. And all five tests pass. Each test simply says, apply coupon save ten. And reads a total of forty-five.

## 6. Act Four — Return the next page

Fourth demo: an action that moves to a new page returns that page. Place order returns the confirmation page. The confirmation page shows the order number, O R D ten forty-two. And the message, thank you for your order. The test cannot ask the checkout page for an order number by mistake. The code follows the real journey.

## 7. Act Five — The bill

Fifth demo: the bill. Every page now needs its own class. And each must be kept in step with the real page. And there is a rule to keep. Page objects report what the page shows. The tests decide whether it is right. A page object that checks its own results hides what each test is testing.

## 8. The Pattern

Let's name the pattern. One class for each page. It is the only place that knows the page's selectors, and how long the page takes to update. Tests call its methods, in the shop's own words.

## 9. Who Does What

Here is who does what. Checkout page can apply a coupon, read the total, and place the order. Confirmation page shows the order number. The fake browser stands in for a real browser driver. And the tests decide whether what they see is right.

## 10. Where You Have Seen It

You have probably met this pattern already. Selenium's own guides recommend page objects. Playwright and Cypress projects are often organised into page classes. And the Screenplay pattern is a later refinement of the same idea.

## 11. When To Use It

So, when should you use it? Once several browser tests share a page. Name methods after what a shopper does. Hide the waiting inside them. Return the next page when an action moves on. And keep the checks in the tests.

## 12. Thanks for Watching

That's the Page Object pattern. If you remember one sentence, make it this one. Tests say what the shopper does, and one class knows how. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Move the coupon box into its own small component class. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
