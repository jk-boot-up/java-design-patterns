# Adapter Pattern — Video Narration Script

## 1. The Adapter Pattern

Hello, and welcome. This video explains the Adapter pattern in Java, and it is written and presented by Jayasekhar Konduru. Let's start with the simple definition. The adapter pattern wraps a class whose interface you cannot change inside one that has the interface you want. Your code goes on calling the interface it expects, the adapter does the translating, and the awkward original is touched by exactly one class in your codebase. That's the idea in a sentence — making two interfaces that were never designed for each other work together anyway. The rest of the video does it properly, by building a real working Java project: a checkout flow that needs shipping rates from a third-party S D K with completely different units. By the end you'll know how to isolate an incompatible interface behind one class, and how to write that class yourself.

## 2. The Scenario

So, imagine checkout for an online store. Checkout needs a shipping rate for an order, given a destination ZIP code and a weight in kilograms, and it wants a price back in dollars. That's the shape the rest of the codebase already uses everywhere. And the only carrier available is a third-party S D K, Acme Shipping. It works in pounds, not kilograms, and it returns a price in integer cents, not dollars.

## 3. Two Shapes That Don't Match

Look closely and the two shapes just don't line up. Checkout wants to call something like quoteRate, pass a ZIP code and a weight in kilograms, and get dollars back. Acme's S D K gives you fetchCostInCents, taking pounds, returning cents. Naively, every place in the codebase that needs a rate ends up doing its own unit conversion, by hand, every single time.

## 4. The Naive Approach — Convert at Every Call Site

So here's the naive approach. NaiveCheckoutService multiplies kilograms by two point two oh four six two to get pounds, calls Acme's S D K directly, then divides the returned cents by a hundred to get dollars. And here's the problem. NaiveShippingEstimator, an entirely separate class elsewhere in the codebase, repeats this exact same conversion independently — copy-pasted, not shared.

## 5. Why That Hurts

And that does real damage as the system grows. The pounds-per-kilogram constant and the cents-to-dollars division get copy-pasted into every class that needs a rate. Every one of those callers is coupled to Acme's exact method name and parameter order. Switch carriers, or Acme changes their S D K, and every caller needs to change, one at a time. None of this is a bug — both naive classes compute a correct rate. The waste is structural: one mechanical conversion, scattered everywhere.

## 6. The Adapter Pattern

The adapter pattern fixes exactly this. In Gang of Four terms, adapter converts the interface of a class into another interface clients expect, letting classes work together that couldn't otherwise, because of incompatible interfaces. In plain language? One class translates, so nothing else in the codebase ever has to.

## 7. Remember It With a Wall Plug

Here's how to remember it forever. Think about traveling with a laptop charger. Your charger has UK prongs, the wall socket has US slots. You don't rewire the charger, and you certainly don't rewire the wall. You plug a small adapter in between, and its entire job is translating one physical shape into the other. Neither the charger nor the socket ever changes. One small translator, sitting between two things that were never designed together.

## 8. The Four Roles

Every adapter setup has four roles. The target, ShippingRateProvider, the interface clients already expect. The adaptee, AcmeShippingSdk, the existing incompatible class we don't control. The adapter, AcmeShippingAdapter, which implements the target and holds the adaptee. And the client, CheckoutService, which only ever depends on the target interface. Here's the single most important idea in this whole video. AcmeShippingAdapter is the only class in the entire codebase that imports AcmeShippingSdk. Every other class only ever sees ShippingRateProvider.

## 9. The Target — The Shape Checkout Already Expects

This is the target, ShippingRateProvider. It's declared entirely in checkout's own terms — kilograms in, dollars out. And this is the adaptee, AcmeShippingSdk. Pounds in, integer cents out, a method called fetchCostInCents. It's a shape checkout never asked for, and one we don't control.

## 10. The Adapter — One Class Translates, Once

And this is the adapter, AcmeShippingAdapter. It implements ShippingRateProvider and holds an AcmeShippingSdk by composition. quoteRate converts kilograms to pounds, calls the S D K, then converts the returned cents back to dollars. Every unit conversion in this entire project happens right here, exactly once.

## 11. The Client — Can't Tell Adapted From Native

And here's the client, CheckoutService. It's constructed with a ShippingRateProvider — sometimes that's an adapted AcmeShippingAdapter, sometimes it's a FlatRateShippingProvider written natively, with no adapting involved at all. CheckoutService's own code never changes between the two. It genuinely cannot tell an adapted implementation from a native one — that's the whole payoff.

## 12. Running It

When we run the project, checkout produces a total with either provider, no branching in sight. The isolated quoteRate call shows exactly what's happening under the hood: three point five kilograms goes in, Acme sees pounds, and thirteen dollars forty eight comes back out. And down at the bottom, the naive classes produce the exact same number — they aren't wrong, they're just duplicated, and coupled directly to a shape that belongs behind one seam.

## 13. Wrap Up

So, to recap. Use adapter when an existing interface doesn't match what your code already expects, and you can't or shouldn't change either side. Keep the adapter a pure translator — no new behavior, no caching, no retry logic. Anything beyond translation belongs in a decorator, not here. And if you remember one sentence from today, make it this one. Adapter reconciles two interfaces that already exist and disagree. Bridge designs two hierarchies from the start so they never have to agree on more than one seam.

## 14. Thanks for Watching

And that's the adapter pattern. If you got something out of this, do give it a thumbs up, and subscribe. It genuinely helps the channel, and it's what makes more of these possible. And if there's a pattern you'd like me to cover next, drop it in the comments. I read every one. All the source code, the written notes and an interactive animation are in the repository. Thanks for watching, and I'll see you in the next one.
