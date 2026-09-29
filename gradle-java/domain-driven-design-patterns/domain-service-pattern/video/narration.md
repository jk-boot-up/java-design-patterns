# Domain Service Pattern — Video Narration Script

## 1. Domain Service

Hello, and welcome. This video explains the Domain Service pattern, from domain-driven design, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Some business rules involve several objects, and belong to none of them. A domain service is a class for such a rule. It holds no data of its own, and it is named in the business's own words. Think of a referee at a football match. Whether a tackle was a foul involves two players and the rules. Neither player decides. The referee applies the rules, the same way every time. In this video, the domain is an online shop. Gold customers get ten percent off. A coupon gives five pounds off baskets over forty pounds. And the two do not add up. By the end, you will hear how copies of a rule drift apart. How a domain service fixes it. How it explains itself. And how services can empty your objects.

## 2. The Scenario

Here is the scenario. Gold customers get ten percent off. The coupon save five gives five pounds off baskets over forty pounds. The rule is: they do not add up. The bigger discount wins. The web checkout had a copy of this rule. So did the phone app.

## 3. Act One — The rule, copied twice

First demo: the pricing rule, copied into the web checkout and the phone app. Priya is a gold customer. Her basket is sixty pounds, and she has the coupon save five. The rule is: gold discount and coupon do not add up. The bigger one wins. The web checkout says fifty-four pounds. The phone app says forty-nine. The app's copy is older. It adds both discounts.

## 4. Act Two — A domain service

Second demo: a domain service. The rule now lives in one class, the pricing service. It takes the customer, the basket, and the coupon. The web checkout calls it. The phone app calls it. Both say fifty-four pounds.

## 5. Act Three — In the shop's words

Third demo: the rule speaks the shop's language. The service gives its reason. Subtotal sixty pounds. Gold ten percent, six pounds off, beats save five, five pounds off. A customer service agent could read that out, word for word. And the rule needs the customer, the basket, and the coupon. It belongs to none of them alone.

## 6. Act Four — One service, every case

Fourth demo: one stateless service, every case. A standard customer, no coupon: sixty pounds. With the coupon: fifty-five. A gold customer, with or without the coupon: fifty-four. A thirty pound basket, below the coupon's minimum: thirty pounds. One service object priced all five. It keeps nothing between calls.

## 7. Act Five — The bill

Fifth demo: the bill. The basket still works out its own subtotal: sixty pounds. That fact belongs to the basket. Move that into a service too, and the basket becomes a bag of data with no behaviour. Too many services empty your objects.

## 8. The Pattern

Let's name the pattern. Find a rule that needs several domain objects, and belongs to none of them. Give it its own class, in the domain. Keep it stateless: no data kept between calls. And name it in the business's own words. Everything that needs the rule calls that one class.

## 9. Who Does What

Here is who does what. The pricing service holds the discount rule. Customer, basket, and coupon are the domain objects. Each keeps its own facts, such as the basket's subtotal. Price is what the service returns: a total, and the reason for it. And copies holds the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern already. Pricing, tax, and shipping calculators that take several objects are domain services. So is a transfer that moves money or stock between two accounts. And so are policies, such as a refund policy, named after the business decision they make.

## 11. When To Use It

So, when should you use it? If a rule belongs to one object, put it on that object. If it genuinely spans several, give it a domain service. Stateless, and well named. And keep workflow steps, such as load, call, save, and send an email, out of it. Those belong in an application service.

## 12. Thanks for Watching

That's the Domain Service pattern. If you remember one sentence, make it this one. A rule nobody owns gets its own home, and everyone uses that one. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add free delivery for gold customers over fifty pounds. Then decide: does it belong in the service, or on an object? If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
