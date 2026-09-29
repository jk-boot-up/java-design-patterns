# Object Mother / Test Data Builder Pattern — Video Narration Script

## 1. Object Mother / Test Data Builder

Hello, and welcome. This video explains two testing patterns, the Object Mother and the Test Data Builder, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Both help tests create the objects they need. An Object Mother is a class of ready-made objects, each with a clear name. A Test Data Builder starts from sensible defaults, and each test changes only the details it cares about. Think of a restaurant kitchen. The chef keeps a shelf of ready-made sauces and stocks. That shelf is the Object Mother. And when a customer asks for the usual, but no onions, the cook starts from the usual and changes just that. That is the builder. In this video, the domain is an online shop's shipping rules, and the tests that check them. By the end, you will hear why hand-built test data hurts. How a mother helps, and where it stops helping. How a builder handles every mix. And the trap of hidden defaults.

## 2. The Scenario

Here is the scenario. The shop's shipping rules are checked by many small tests. Each test built its order by hand. Three constructors, and eight values. Nobody reading the test could tell which of those values mattered.

## 3. Act One — Built by hand

First demo: every test builds its order by hand. A customer, with a name, an email, and a VIP flag. A country. A product line, with a quantity and a price. And a gift-wrap flag. Eight values, just to check that shipping costs four ninety-nine. Which of those eight values matter to this test? The reader cannot tell. And when the customer gains a new field, every test like this must be edited.

## 4. Act Two — An Object Mother

Second demo: an Object Mother. It is one class of ready-made orders, each with a name that says what it is. A domestic order ships for four ninety-nine. A VIP order ships free. An international order pays fifteen. Each test needs one line to get its order. And a new customer field is added in one place.

## 5. Act Three — The mother multiplies

Third demo: the mother multiplies. Tests need mixes. VIP or not. Abroad or not. Gift wrapped or not. Three yes-or-no details make eight combinations. Each one needs its own method, with a longer and longer name. Add one more detail, and it is sixteen.

## 6. Act Four — A Test Data Builder

Fourth demo: a Test Data Builder. It starts with sensible defaults for everything. And it has one method for each detail. A test says: an order, VIP, shipped to France. It pays fifteen, because free VIP shipping is only for the United Kingdom. Another test says: an order, VIP, gift wrapped. It pays two, for the wrapping. Any mix, in one line. And the line names exactly what the test cares about.

## 7. Act Five — The bill

Fifth demo: the bill. A test leaned on a hidden default. A free-shipping test just asked for an order. Back then, the default price was sixty. Over the free-shipping line. Someone lowered the default to thirty. Now the order pays four ninety-nine. And the test fails, with no visible reason. The fix: the test asks for an order totalling sixty. A test must state everything it relies on.

## 8. The Pattern

Let's name the patterns. An Object Mother hands out named, ready-made objects. Good for a few well-known cases. A Test Data Builder starts from defaults. Each test states only the details it cares about. Good for any mix.

## 9. Who Does What

Here is who does what. Test orders is the mother, with methods like domestic, VIP and international. The order builder starts with a UK order of one mug, and has a method for each detail. Shipping rules is the code being tested. And the order is the object that needs eight values to exist.

## 10. Where You Have Seen It

You have probably met these patterns already. Many projects have a fixtures class in their test folder. Lombok can generate builders. And libraries such as Instancio fill objects with data. Ruby's factory bot, and Python's factory boy, are the same idea.

## 11. When To Use It

So, when should you use them? When objects need many values, and many tests need slightly different versions. Use a mother for a few named cases. A builder for many mixes. Keep the defaults dull. And let every test state what it relies on.

## 12. Thanks for Watching

That's the Object Mother and the Test Data Builder. If you remember one sentence, make it this one. A test should only show the details it depends on. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Make the mother's methods return builders, so the two patterns work together. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
