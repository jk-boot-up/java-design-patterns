# The Adapter Pattern Pattern — Video Narration Script

## 1. The Adapter Pattern

Hello, and welcome. This video explains the Adapter pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. An adapter wraps a class you cannot change, inside a class with the shape you want. Your code keeps calling the shape it expects. The adapter does the translating. And the awkward original is touched by just one class in your code. Think of a travel plug adapter. Your charger and the wall socket never change. A small adapter in between makes them fit. In our online store, checkout needs shipping prices from another company's toolkit, which uses completely different units. By the end, you will know how to hide a mismatched interface behind one class, and how to write that class yourself.

## 2. The Scenario

Here is the scenario. Checkout needs a shipping price for an order. It gives a delivery zip code, and a weight in kilograms. And it wants the price back in dollars. That is the shape the rest of the code already uses. But the only carrier available is a toolkit from another company, called Acme Shipping. It works in pounds of weight, not kilograms. And it returns the price in whole cents, not dollars.

## 3. Two Shapes That Don't Match

The two shapes just do not match. Checkout wants to ask for a quote, with a zip code and kilograms, and get dollars back. Acme's toolkit takes pounds, and returns cents. So, done naively, every part of the code that needs a price does its own unit conversion, by hand, every time.

## 4. The Naive Approach — Convert at Every Call Site

Here is the naive approach. The naive checkout multiplies kilograms by two point two oh four six two, to get pounds. It calls Acme's toolkit directly. Then it divides the cents by a hundred, to get dollars. And here is the problem. A completely separate class, a shipping estimator, repeats exactly the same conversion. Copied and pasted, not shared.

## 5. Why That Hurts

That does real damage as the system grows. The conversion numbers get copied into every class that needs a price. Every one of those classes depends on Acme's exact method name, and the order of its inputs. Switch to another carrier, or let Acme change its toolkit, and every one of those classes must change, one by one. And none of this is a bug. Both naive classes calculate the correct price. The waste is in the structure: one simple conversion, scattered everywhere.

## 6. The Adapter Pattern

The Adapter pattern fixes exactly this. The classic book on design patterns, by the authors known as the Gang of Four, describes it like this. Convert the interface of a class into another interface that clients expect. In plain words: one class translates, so nothing else has to.

## 7. Remember It With a Wall Plug

Here is how to remember it. Think about travelling with a laptop charger. Your charger has a British plug. The wall socket is American. You do not rewire the charger. And you certainly do not rewire the wall. You plug a small adapter in between. Its whole job is to turn one shape into the other. Neither the charger nor the socket ever changes. One small translator, between two things that were never designed to fit.

## 8. The Four Roles

Every adapter has four roles. The target: the interface checkout already expects, called the shipping rate provider. The adaptee: Acme's toolkit, the mismatched class we cannot change. The adapter: the Acme shipping adapter, which offers the target's shape, and holds Acme's toolkit inside. And the client: the checkout service, which only ever talks to the target. Here is the most important idea in this video. The adapter is the only class in the whole code that knows Acme's toolkit exists. Every other class only sees the shipping rate provider.

## 9. The Target — The Shape Checkout Already Expects

Here is the target, the shipping rate provider. It is written entirely in checkout's own terms. Kilograms in, dollars out. And here is the adaptee, Acme's toolkit. Pounds in, whole cents out. A shape checkout never asked for, and one we cannot change.

## 10. The Adapter — One Class Translates, Once

And here is the adapter. It offers the shipping rate provider's shape, and keeps Acme's toolkit inside it. When asked for a quote, it converts kilograms to pounds. It calls Acme's toolkit. Then it converts the cents back to dollars. Every unit conversion in this whole project happens right here, exactly once.

## 11. The Client — Can't Tell Adapted From Native

And here is the client, the checkout service. It is given a shipping rate provider. Sometimes that is the Acme adapter. Sometimes it is a flat-rate provider, written in the right shape from the start, with no adapting at all. The checkout code never changes between the two. It cannot tell an adapted provider from a native one. And that is the whole payoff.

## 12. Running It

Let's run the project. Checkout calculates a total with either provider, with no special cases. With Acme, through the adapter: sixty-three dollars forty-six. With the flat rate: fifty-seven dollars forty-eight. Looking inside one quote: three and a half kilograms goes in. Acme sees pounds. And thirteen dollars forty-eight comes back out. And the naive classes give exactly the same number. They are not wrong. They are just duplicated, and tied to a shape that belongs behind one class.

## 13. Wrap Up

So, to recap. Use an adapter when an existing interface does not match what your code expects. And you cannot, or should not, change either side. Keep the adapter a pure translator. No new behaviour, no caching, and no retries. Anything beyond translating belongs in a different pattern, the Decorator. And one comparison worth knowing. An adapter fixes two interfaces that already exist, and disagree. The Bridge pattern designs two sides from the start, so they never need fixing.

## 14. Thanks for Watching

That's the Adapter pattern. If you remember one sentence, make it this one. An adapter is one small translator, so the rest of your code never has to know about a mismatched interface. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a second carrier, with yet another set of units. And notice that checkout does not change at all. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
