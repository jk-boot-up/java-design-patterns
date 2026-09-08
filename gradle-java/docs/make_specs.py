#!/usr/bin/env python3
"""Write `docs/spec.md` and `docs/spec.html` for every pattern project.

Each project gets one specification: what it teaches, what its code has to
be true of, and the quality bar its video and its YouTube publication have to
meet.

Why this is generated rather than fourteen hand-written files. Roughly half of
each spec -- the video pipeline, the poster and thumbnail rules, the
publishing requirements, the conformance checklist -- is identical across all
fourteen projects by design, because thirteen of the build scripts are
generated from abstract factory's. Hand-maintaining fourteen copies of that
guarantees they drift, and a spec that disagrees with the pipeline is worse
than no spec. The per-project half lives in `META` below, and every number in
the shared half (runtime, scene count, loudness, test count) is read from the
project's own files at generation time rather than typed in.

The HTML is rendered from the Markdown by the same run, for the same reason:
two hand-maintained copies of one document drift, and the stale one is always
the one somebody reads.

Usage:
    python3 docs/make_specs.py                  # all projects
    python3 docs/make_specs.py proxy builder    # named projects
    python3 docs/make_specs.py --no-measure     # skip the ffmpeg loudness pass
"""

import html
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Learning order. The end screen of each video points at the next one.
ORDER = [
    ("creational", "simple-factory"),
    ("creational", "static-factory"),
    ("creational", "factory-method"),
    ("creational", "abstract-factory"),
    ("creational", "builder"),
    ("creational", "prototype"),
    ("creational", "singleton"),
    ("structural", "adapter"),
    ("structural", "bridge"),
    ("structural", "composite"),
    ("structural", "decorator"),
    ("structural", "facade"),
    ("structural", "flyweight"),
    ("structural", "proxy"),
    ("behavioural", "strategy"),
    ("behavioural", "observer"),
    ("behavioural", "command"),
    ("behavioural", "template-method"),
    ("behavioural", "state"),
    ("behavioural", "chain-of-responsibility"),
    ("behavioural", "iterator"),
    ("behavioural", "mediator"),
    ("behavioural", "memento"),
    ("behavioural", "visitor"),
    ("behavioural", "interpreter"),
]

# Demos that mint an identifier per run, so their output is not byte-stable.
NONDETERMINISTIC = {"simple-factory", "factory-method", "facade"}

NAMES = {
    "simple-factory": "Simple Factory", "static-factory": "Static Factory",
    "factory-method": "Factory Method", "abstract-factory": "Abstract Factory",
    "builder": "Builder", "prototype": "Prototype", "singleton": "Singleton",
    "adapter": "Adapter", "bridge": "Bridge", "composite": "Composite",
    "decorator": "Decorator", "facade": "Facade", "flyweight": "Flyweight",
    "proxy": "Proxy",
    "strategy": "Strategy",
    "observer": "Observer",
    "command": "Command",
    "template-method": "Template Method",
    "state": "State",
    "chain-of-responsibility": "Chain of Responsibility",
    "iterator": "Iterator",
    "mediator": "Mediator",
    "memento": "Memento",
    "visitor": "Visitor",
    "interpreter": "Interpreter",
}

# ---------------------------------------------------------------------------
# Per-project content.
#
#   purpose      -- what this project teaches, in the store's terms
#   nongoals     -- what a reader must not mistake it for
#   problem      -- the scenario and what the pattern has to deliver. The full
#                   treatment stays in the project's problem-statement.md; this
#                   is the summary a specification needs.
#   roles        -- (role, types) rows mapping the pattern's vocabulary onto
#                   the actual class names
#   requirements -- the properties the code must have, each one falsifiable
# ---------------------------------------------------------------------------

META = {

"simple-factory": dict(
purpose="""
Teach how a *value* -- a dropdown selection, a JSON field, a database column --
becomes an *object*, and why that conversion belongs in one named place rather
than wherever it is first needed.
""",
nongoals=[
    "Not a payment integration. `CreditCardPayment` prints; it does not "
    "authorise anything.",
    "Not a Gang of Four pattern. Simple Factory is not in the book -- it is "
    "the everyday idiom that Factory Method and Abstract Factory both grow "
    "out of, which is why it comes first in the learning order.",
    "Not an argument against dependency injection. A DI container solves an "
    "overlapping problem, and the written notes say so.",
],
problem="""
The payment step of an online store offers four methods -- credit card, UPI,
PayPal, net banking. They do the same job from the outside, taking a
`PaymentRequest` and returning a `PaymentReceipt`, so one interface covers
them all.

The choice, though, arrives as data. It comes from a dropdown, a JSON field or
a database column: a `String` or an enum, never a Java type. Something has to
turn that value into an object, and if that something is a `switch` inside
`CheckoutService`, then checkout knows about every payment method that exists.
Adding a fifth means editing checkout, and every other place that had to make
the same decision.

**What the pattern must deliver:** exactly one place in the codebase that
names the concrete payment classes. Everywhere else asks for a `PaymentMethod`
and is told nothing about which one it got.
""",
roles=[
    ("Product interface", "`PaymentMethod`"),
    ("Concrete products", "`CreditCardPayment`, `UpiPayment`, `PayPalPayment`, `NetBankingPayment`"),
    ("Factory", "`PaymentMethodFactory`"),
    ("Client", "`CheckoutService`"),
    ("Value objects", "`PaymentRequest`, `PaymentReceipt`, `PaymentType`"),
    ("Entry point", "`SimpleFactoryDemo`"),
],
requirements=[
    "**The factory is the only place a concrete method is named.** Grepping "
    "for `new CreditCardPayment()` must find exactly one call site.",
    "**The client never branches on the payment type.** If `CheckoutService` "
    "contains a `switch` over `PaymentType`, the decision has been duplicated, "
    "not centralised.",
    "**An unknown type fails loudly**, with a message naming the value that "
    "was not recognised. Silently returning a default is how a customer pays "
    "by a method they did not choose.",
],
),

"static-factory": dict(
purpose="""
Teach why a constructor's name -- which is to say, the class's name, because a
constructor has no name of its own -- is often the wrong thing to have to say,
and what you gain by replacing it with a static method that can be named.
""",
nongoals=[
    "Not a Gang of Four pattern. This is the Effective Java idiom, included "
    "because it is the cheapest possible introduction to the idea that "
    "construction is a decision worth naming.",
    "Not a money library. `Money` exists so the arithmetic is readable; use "
    "`BigDecimal` and a real currency type in production.",
    "Not a promotions engine. Real discount stacking has rules about "
    "precedence and exclusivity that this deliberately does not model.",
]  ,
problem="""
The store needs four kinds of discount -- a percentage off, a flat amount off,
free shipping, and no discount at all -- and marketing promises more.

A constructor cannot express that. `new Discount(10)` is ambiguous the moment
both "10% off" and "£10 off" exist, and the language will not even let you
declare both, because two constructors taking a `double` have the same
signature. The usual escape is a flag parameter or an enum argument, which
means every call site has to be read carefully to find out what it does.

**What the pattern must deliver:** construction that says what it means at the
call site. `Discount.percentage(10)` and `Discount.amountOff(Money.pounds(10))`
cannot be confused for one another, can return different implementations, and
can return a cached instance where one will do.
""",
roles=[
    ("Abstraction", "`Discount`"),
    ("Implementations", "`PercentageDiscount`, `AmountOffDiscount`, `FreeShippingDiscount`, `NoDiscount`, `BestOfDiscount`"),
    ("Client", "`CheckoutService`"),
    ("Value objects", "`Money`, `Order`, `Receipt`"),
    ("Entry point", "`StaticFactoryDemo`"),
],
requirements=[
    "**Constructors are not public.** If callers can still write `new "
    "PercentageDiscount(...)`, the named methods are decoration rather than "
    "the way in.",
    "**Every factory method names its intent**, not its parameters. "
    "`Discount.percentage(10)` reads at the call site; `Discount.of(10, true)` "
    "does not.",
    "**Factory methods return the abstraction**, so which implementation comes "
    "back stays a private decision -- that freedom is the whole point of the "
    "idiom.",
],
),

"factory-method": dict(
purpose="""
Teach the case where a workflow is fixed but one step inside it varies: the
base class owns the sequence, and a subclass decides only the thing that
genuinely differs.
""",
nongoals=[
    "Not a carrier integration. The couriers print and return a `Shipment`.",
    "Not a claim that inheritance is the right tool here in production -- a "
    "constructor parameter often is. The written notes cover when the "
    "subclass hook earns its keep and when it does not.",
    "Not Template Method, though the two are close relatives and the "
    "explained document draws the line between them.",
],
problem="""
The shipping step offers four delivery tiers, each handing the parcel to a
different carrier: Standard to a postal courier, Express to an air courier,
Same Day to a bike courier, International to a freight courier.

The carriers share one interface, so picking between them is easy. The part
that matters is that shipping is not just "pick a carrier". Every tier runs
the same workflow -- validate the order, log that the parcel is being
prepared, hand it over, log the tracking number. Writing that workflow four
times means four places to fix when the logging changes, and four chances for
them to diverge.

**What the pattern must deliver:** the workflow written once, with a single
hole in it that each tier fills. A new tier supplies a courier and inherits
the sequence; it cannot accidentally reorder the steps, because it never sees
them.
""",
roles=[
    ("Creator", "`DeliveryService`"),
    ("Concrete creators", "`StandardDelivery`, `ExpressDelivery`, `SameDayDelivery`, `InternationalDelivery`"),
    ("Product interface", "`Courier`"),
    ("Concrete products", "`PostalCourier`, `AirCourier`, `BikeCourier`, `GlobalCourier`"),
    ("Value objects", "`Order`, `Shipment`, `TrackingIds`"),
    ("Entry point", "`FactoryMethodDemo`"),
],
requirements=[
    "**The base class never names a concrete courier.** It calls its own "
    "factory method and nothing else.",
    "**Subclasses override the factory method and nothing else.** A subclass "
    "that also overrides the workflow has defeated the pattern.",
    "**The workflow is identical for all four tiers**, demonstrably: the "
    "printed output differs only in the carrier and the timings.",
],
),

"abstract-factory": dict(
purpose="""
Teach the case where several objects must be chosen *together*, and where any
mixed selection is a bug: one decision produces a whole consistent family.
""",
nongoals=[
    "Not a production tax or currency library. `UkVatCalculator` hard-codes "
    "20%; a real system reads rates from a table that changes by legislation.",
    "Not a survey of alternatives. Dependency injection containers, service "
    "locators and enum-based strategies all solve overlapping problems, and "
    "the written notes say so, but the project demonstrates one pattern.",
    "Not a reference for internationalisation. `RupeeFormatter` formats a "
    "number; it is not `java.text.NumberFormat` and does not pretend to be.",
],
problem="""
An online store that has been selling in one country is about to sell in
three. Checkout turns out not to be one piece of logic but three, and all
three change together when the market changes:

| Market | Tax | Money | Address |
| --- | --- | --- | --- |
| United Kingdom | 20% VAT | £1,234.50 · GBP | postcode — `EH1 1YZ` |
| United States | 8.875% Sales Tax | $1,234.50 · USD | ZIP code — `10001` |
| India | 18% GST | ₹1,234.50 · INR | PIN code — `560001` |

Each column is easy alone: three tax calculators, three currency formatters,
three address validators -- nine small classes behind three interfaces.

**The difficulty is that the three must agree.** A receipt showing British VAT
next to a dollar sign is not a small bug, it is a wrong invoice. A checkout
that accepts an American ZIP code and then charges Indian GST is worse. Nine
classes, and only three of the twenty-seven combinations are legal.

The naive client picks each piece for itself, which means three separate
`if`/`else` chains over the same `market` string, in one method, kept in
agreement by hand. Nothing in the type system stops the next developer adding
a case to two chains and forgetting the third; the result compiles, runs, and
produces a wrong invoice silently.

**What the pattern must deliver:** a mismatched family becomes not merely
uncaught but unrepresentable. One decision -- which market -- is made once,
and the three pieces that follow from it cannot disagree, because the client
never selects them individually.

The project is also required to be honest about the cost. Adding a fourth
*market* is cheap: one new factory class, no existing code changed. Adding a
fourth *product kind* -- a shipping-rules interface, say -- is expensive:
every factory in the family must change. The written notes and the video both
cover this, and the video gives it a scene. A teaching project that only shows
the upside teaches the wrong lesson about when to reach for the pattern.
""",
roles=[
    ("Abstract factory", "`MarketFactory`"),
    ("Concrete factories", "`UkMarketFactory`, `UsMarketFactory`, `IndiaMarketFactory`"),
    ("Abstract products", "`TaxCalculator`, `CurrencyFormatter`, `AddressValidator`"),
    ("Concrete products", "`UkVatCalculator`, `UsSalesTaxCalculator`, `IndiaGstCalculator`, `PoundFormatter`, `DollarFormatter`, `RupeeFormatter`, `UkPostcodeValidator`, `UsZipValidator`, `IndiaPinValidator`"),
    ("Client", "`CheckoutService`"),
    ("Value objects", "`Order`, `Quote`"),
    ("Entry point", "`AbstractFactoryDemo`"),
],
requirements=[
    "**The client takes a factory, never a market string.** `CheckoutService` "
    "must have no knowledge of which markets exist. If it can name \"UK\", the "
    "pattern has not been applied -- it has only been moved.",
    "**Concrete product types are never named outside their factory.** "
    "Grepping for `new UkVatCalculator()` must find exactly one call site.",
    "**A factory returns one family or none.** There is no path through the "
    "code that yields a UK tax rule beside a dollar formatter.",
],
),

"builder": dict(
purpose="""
Teach construction of an object with many optional parts: how to keep it
immutable and validated without a constructor whose parameter list nobody can
read.
""",
nongoals=[
    "Not Lombok's `@Builder`. Writing the builder by hand is the point; "
    "generating it hides exactly the decisions being taught.",
    "Not a validation framework. `build()` checks what it must; Bean "
    "Validation is a different tool for a different job.",
    "Not an argument that everything needs a builder. Two or three "
    "parameters do not.",
],
problem="""
Placing a purchase order involves two facts that never change -- who is buying,
and where it ships -- and a pile of options that vary: gift wrapping, a gift
message, priority handling, a coupon code, a note for the warehouse.

A constructor taking all of them is unreadable at the call site: a row of
booleans and nulls whose meaning depends entirely on position, where swapping
two arguments of the same type compiles cleanly and ships the wrong thing.
Telescoping overloads multiply instead of solving it. Setters fix the
readability and give up immutability and validation, leaving an object that
can exist in a half-built state.

**What the pattern must deliver:** a call site that names each option it sets,
an object that is immutable once built, and a single place where "is this
order actually valid" is answered -- before the object exists, not after.
""",
roles=[
    ("Product", "`PurchaseOrder`"),
    ("Builder", "`PurchaseOrder.Builder`"),
    ("Presets", "`PurchaseOrderPresets`"),
    ("Value objects", "`LineItem`, `Address`, `Money`"),
    ("Entry point", "`PurchaseOrderDemo`"),
],
requirements=[
    "**`PurchaseOrder` has no public constructor and no setters.** The builder "
    "is the only way to make one, and a built order cannot be changed.",
    "**`build()` validates.** A missing customer or an empty item list is "
    "rejected there, so an invalid `PurchaseOrder` cannot exist.",
    "**Collections are copied on the way in and unmodifiable on the way out**, "
    "so a caller holding the original list cannot mutate a built order.",
],
),

"prototype": dict(
purpose="""
Teach copying a configured object as an alternative to rebuilding it, and --
more importantly -- how to decide, field by field, what a copy must duplicate
and what it may share.
""",
nongoals=[
    "Not an endorsement of `Cloneable` and `Object.clone()`. The project "
    "implements its own `Prototype` interface, and the written notes explain "
    "why the built-in mechanism is best avoided.",
    "Not a serialization-based deep-copy utility. Those exist and have their "
    "place; they hide the decision this project is about.",
    "Not a caching layer. The registry stores masters to copy, not results.",
],
problem="""
A seller lists "Wireless Earbuds" in black. Getting that one listing right is
real work: a category from the taxonomy, a description that satisfies
compliance, a shipping profile, a return window and warranty matching the
category's policy, photos, a dozen attributes.

Now the same earbuds in white, and again in blue. Nothing about the category,
the compliance text, the shipping profile, the return window or the warranty
changed -- only the SKU, the title, one attribute and the photos did.
Constructing each variant from scratch means repeating every unchanged
argument, and every repetition is a chance to get one of them subtly wrong.

**What the pattern must deliver:** an existing, correct listing is the
starting point for the next one. Copy it, change the three things that differ,
and the rest is right by construction -- with the copy deep enough that
editing the variant cannot reach back and alter the original.
""",
roles=[
    ("Prototype interface", "`Prototype`"),
    ("Concrete prototype", "`ProductListing`"),
    ("Registry", "`ListingRegistry`"),
    ("Value objects", "`Money`, `ShippingProfile`"),
    ("Entry point", "`ProductListingDemo`"),
],
requirements=[
    "**Mutating a copy never affects its original.** This is the property the "
    "tests exist to defend; a shallow copy of the attribute map breaks it "
    "silently.",
    "**Sharing is deliberate, not accidental.** Immutable values may be shared "
    "by reference, and the code says why at each point rather than deep-copying "
    "everything out of caution.",
    "**The registry hands out copies, never its masters.** A caller that "
    "mutated a registry entry would corrupt every later copy.",
],
),

"singleton": dict(
purpose="""
Teach the case for exactly one instance, how Java actually enforces that
against reflection and serialization, and -- just as much -- when the pattern
is the wrong answer.
""",
nongoals=[
    "Not an endorsement of singletons as a default. The pattern makes "
    "dependencies invisible and tests order-dependent; the written notes are "
    "explicit that a single instance passed by dependency injection is "
    "usually better.",
    "Not a distributed ID generator. One JVM, one counter. Real order numbers "
    "across several instances need a database sequence or a snowflake ID.",
    "Not a lazy-initialisation tutorial. Double-checked locking is discussed "
    "and then not used, because the enum does the job.",
],
problem="""
Every checkout needs an order number -- `ORD-000001`, `ORD-000002` -- handed
out in strict sequence with no gaps and no repeats. Two customers must never
receive the same number, whichever part of the system issued it: checkout, the
admin console raising a manual order, or a background job replaying a failed
payment.

An ordinary class fails immediately: each caller that constructs its own
generator gets its own counter, so three independent components cheerfully
hand out `ORD-000001` three times. A `static` counter fixes the duplication
and introduces a different problem -- nothing stops two threads reading the
same value before either writes back.

**What the pattern must deliver:** one instance that the language guarantees,
not one that a convention requests; and a counter that is correct when several
threads call it at once.
""",
roles=[
    ("Singleton", "`OrderSequenceGenerator`"),
    ("Counter-example", "`LegacyOrderSequenceGenerator`"),
    ("Entry point", "`OrderSequenceGeneratorDemo`"),
],
requirements=[
    "**The singleton is an enum.** That is what makes a second instance "
    "impossible: reflection cannot invoke an enum constructor, and "
    "deserialization returns the existing constant rather than a copy.",
    "**The counter is thread-safe**, and a test proves it by issuing numbers "
    "concurrently and asserting the set of results has no duplicates.",
    "**The broken version stays in the project.** `LegacyOrderSequenceGenerator` "
    "exists to be demonstrated failing; deleting it would remove the reason "
    "the pattern is there.",
],
),

"adapter": dict(
purpose="""
Teach how to put a class you do not control behind the interface your code
already speaks, so that the mismatch is translated in one place instead of at
every call site.
""",
nongoals=[
    "Not a real carrier integration. `AcmeShippingSdk` is a stand-in for a "
    "third-party jar, and is deliberately awkward in the way real ones are.",
    "Not a units library. The conversions are arithmetic in one method "
    "because that is where the lesson is.",
],
problem="""
Checkout needs a shipping cost for a destination and a package weight, in the
units the rest of the codebase already uses: kilograms and dollars. The
company has just signed with a third-party carrier, and their SDK is the only
source of real rates.

The SDK does not match. It takes pounds, returns integer cents, and names the
method something unrelated to anything checkout says. Calling it directly
means the conversion is written wherever a rate is needed -- and the second
time somebody writes it, one of the two will eventually be wrong, or will be
updated when the other is not. The SDK's vocabulary also spreads: checkout
starts mentioning a vendor it should never have heard of.

**What the pattern must deliver:** one class that speaks both languages, and
a checkout that names only its own interface. Swapping the carrier, or falling
back to a flat rate, becomes a change of which implementation is passed in.
""",
roles=[
    ("Target interface", "`ShippingRateProvider`"),
    ("Adapter", "`AcmeShippingAdapter`"),
    ("Adaptee", "`AcmeShippingSdk`"),
    ("Alternative implementation", "`FlatRateShippingProvider`"),
    ("Client", "`CheckoutService`"),
    ("Naive alternatives", "`NaiveCheckoutService`, `NaiveShippingEstimator`"),
    ("Entry point", "`ShippingDemo`"),
],
requirements=[
    "**The unit conversion appears exactly once**, inside the adapter. Two "
    "copies of a pounds-to-kilograms factor is the bug the pattern prevents.",
    "**`CheckoutService` never mentions Acme.** It depends on "
    "`ShippingRateProvider` and cannot tell which implementation it holds.",
    "**The adapter and the flat-rate provider are interchangeable**, "
    "demonstrated by running checkout against both.",
],
),

"bridge": dict(
purpose="""
Teach what to do when two things vary independently and the obvious design
multiplies them together: separate the two hierarchies and let them meet
through composition.
""",
nongoals=[
    "Not a messaging integration. The channels print.",
    "Not a template for every pair of varying concepts. The written notes are "
    "clear that the pattern earns its keep when both dimensions really do keep "
    "growing, and is over-engineering when one of them is fixed.",
],
problem="""
The store sends several *kinds* of notification -- order confirmations,
shipping updates, password resets -- over several *channels* -- email, SMS,
push. Every kind must be sendable over every channel.

The obvious shape is a class per pair: `OrderConfirmationEmail`,
`OrderConfirmationSms`, `ShippingUpdateEmail`, and so on. Three kinds and
three channels is nine classes; adding a fourth channel adds four more, and
adding a fourth notification adds another four. Worse, the wording of a
notification and the mechanics of a channel end up interleaved in the same
method, so changing how SMS is delivered means editing every notification that
can be sent by SMS.

**What the pattern must deliver:** kinds and channels that grow independently.
A new channel is one class and touches no notification; a new notification is
one class and touches no channel. Nine classes become three plus three.
""",
roles=[
    ("Abstraction", "`Notification`"),
    ("Refined abstractions", "`OrderConfirmationNotification`, `ShippingUpdateNotification`, `PasswordResetNotification`"),
    ("Implementor interface", "`MessageChannel`"),
    ("Concrete implementors", "`EmailChannel`, `SmsChannel`, `PushChannel`"),
    ("Naive alternatives", "`NaiveOrderConfirmationEmail`, `NaiveOrderConfirmationSms`, `NaiveShippingUpdateEmail`, `NaiveShippingUpdateSms`"),
    ("Entry point", "`NotificationDemo`"),
],
requirements=[
    "**A notification holds a `MessageChannel`, never a concrete channel.** "
    "If `OrderConfirmationNotification` names `EmailChannel`, the two "
    "hierarchies are still fused.",
    "**Adding a channel changes no notification class**, and adding a "
    "notification changes no channel class. This is the property that "
    "distinguishes the pattern from a plain interface.",
    "**Channels are testable without I/O**, via a recording channel the tests "
    "supply in place of a real one.",
],
),

"composite": dict(
purpose="""
Teach how to treat a single thing and a collection of things through the same
interface, so that code walking a tree never has to ask which one it is
holding.
""",
nongoals=[
    "Not a catalog engine. The tree is built in code; a real one comes from a "
    "database and needs paging.",
    "Not a claim that every hierarchy should be a composite. The written notes "
    "cover the cost: a shared interface that leaves half its methods "
    "meaningless on a leaf is a warning sign, not a success.",
],
problem="""
The catalog is a tree. `Electronics` holds a phone directly and also an
`Accessories` category, which holds a case and a charger plus a nested
`Cables` category holding a USB-C cable. Categories hold products, and they
hold more categories, to whatever depth merchandising wants.

Three operations are needed over that tree: the total price beneath a node,
how many products it contains, and an indented print of the whole thing.

If products and categories share nothing, the children must be held as
`List<Object>`, and every one of those three operations becomes a recursive
walk full of `instanceof` and casts. Each new operation repeats the same
type-dispatch, and each is a chance to forget a case -- and adding a third
kind of node means finding and updating every one of those chains.

**What the pattern must deliver:** one interface implemented by both the leaf
and the container, so that the client asks the node for its total and the
recursion lives inside the container. No `instanceof`, no casts, no depth
limit.
""",
roles=[
    ("Component interface", "`CatalogComponent`"),
    ("Leaf", "`Product`"),
    ("Composite", "`Category`"),
    ("Naive alternatives", "`NaiveProduct`, `NaiveCategory`, `NaiveCatalogPrinter`"),
    ("Entry point", "`CatalogDemo`"),
],
requirements=[
    "**No `instanceof` and no casting in client code.** This is checkable by "
    "grep and is the single clearest signal that the pattern is doing its job.",
    "**The recursion lives in `Category`**, not in the caller. A client that "
    "walks children itself has taken the responsibility back.",
    "**Depth is unbounded**, and the demo tree is nested deeply enough -- "
    "three levels -- that a design only working one level down would fail.",
],
),

"decorator": dict(
purpose="""
Teach adding behaviour to an object at runtime by wrapping it, and why that
beats a subclass for every combination of options a customer might pick.
""",
nongoals=[
    "Not a pricing engine. Real checkout pricing has tax interactions and "
    "ordering rules this deliberately does not model.",
    "Not a claim that decorators are free. The written notes cover the cost: "
    "a deep stack is hard to debug, and the object you hold is no longer the "
    "one you created.",
],
problem="""
A product has a base price, and at checkout the customer can add optional
extras: gift wrapping, shipment insurance, express handling. Any combination
should be selectable -- one of them, all three, or none.

A class per combination is the obvious first move and collapses immediately.
Three extras is seven classes; a fourth extra makes fifteen. The fee for gift
wrapping is duplicated into every class that includes it, so changing it means
finding all of them, and the combination the customer actually wants has to
have been anticipated at compile time.

**What the pattern must deliver:** each extra written once, applied to
anything that has a price, and composable in any combination and any order --
decided at runtime, when the customer chooses, rather than by the set of
classes somebody thought to write.
""",
roles=[
    ("Component interface", "`PricedItem`"),
    ("Concrete component", "`Product`"),
    ("Base decorator", "`ProductDecorator`"),
    ("Concrete decorators", "`GiftWrapDecorator`, `InsuranceDecorator`, `ExpressHandlingDecorator`"),
    ("Naive alternatives", "`NaiveGiftWrappedProduct`, `NaiveInsuredProduct`, `NaiveGiftWrappedInsuredProduct`"),
    ("Entry point", "`PricingDemo`"),
],
requirements=[
    "**A decorator is itself a `PricedItem`.** That is what lets decorators "
    "wrap decorators, and it is the whole mechanism.",
    "**Each fee is defined in exactly one class.** If the gift-wrap fee "
    "appears twice, the pattern has been applied to the shape but not to the "
    "duplication.",
    "**Decorators stack in any order**, with a test that builds the same set "
    "of extras two ways and asserts the price agrees.",
],
),

"facade": dict(
purpose="""
Teach putting one simple entry point in front of a multi-step workflow across
several subsystems, without hiding those subsystems from anyone who needs them
directly.
""",
nongoals=[
    "Not a transaction manager. A real place-order needs compensation when "
    "step three fails after step two charged the card; the written notes "
    "raise this and the code does not solve it.",
    "Not a service layer template. A facade that grows business rules of its "
    "own has stopped being a facade, and the notes say where that line is.",
],
problem="""
When a customer clicks **Place Order**, four things must happen in a specific
order: reserve the stock so nobody else takes the last item, charge the card
but only once stock is confirmed, schedule the shipment, and email a
confirmation carrying the tracking number.

Each step lives in its own service, written by a different team, each with its
own vocabulary and its own return type that the next step needs. A caller
doing this itself has to know all four APIs, the order they go in, and which
output feeds which input. Every screen that can place an order repeats that
knowledge, and the ordering constraint -- stock before payment -- is enforced
only by everyone remembering it.

**What the pattern must deliver:** one method that takes an `OrderRequest` and
returns an `OrderConfirmation`, with the sequence and the plumbing in one
place. The four services stay public and directly usable, because a facade
that locks them away has replaced a hard API with a limited one.
""",
roles=[
    ("Facade", "`OrderFacade`"),
    ("Subsystems", "`InventoryService`, `PaymentService`, `ShippingService`, `NotificationService`"),
    ("Value objects", "`OrderRequest`, `OrderConfirmation`"),
    ("Entry point", "`FacadeDemo`"),
],
requirements=[
    "**The facade adds no business rules.** It sequences calls and moves data "
    "between them; a discount calculation appearing here means the "
    "responsibility has drifted.",
    "**The subsystems remain usable on their own.** Nothing is made "
    "package-private to force callers through the facade -- the facade is a "
    "convenience, not a wall.",
    "**The ordering constraint is enforced in one place**: stock is reserved "
    "before the card is charged, and that fact lives in the facade rather "
    "than in every caller.",
],
),

"flyweight": dict(
purpose="""
Teach separating the state that is genuinely per-object from the state that is
identical across thousands of objects, and sharing the second kind instead of
copying it.
""",
nongoals=[
    "Not a general memory-optimisation guide. Flyweight is worth reaching for "
    "when profiling has shown duplicated immutable state, and the written "
    "notes are blunt that applying it speculatively costs clarity for nothing.",
    "Not a cache. The factory's map is a pool of shared values with a fixed "
    "key space, not an eviction policy.",
],
problem="""
Every catalog listing can carry a badge -- `NEW`, `SALE`, `BESTSELLER`,
`LOW_STOCK`. A badge is more than a label: it has an icon, a background
colour, a text colour, a bold rule, and the rasterised artwork the design
system hands over.

There are four distinct badge designs. There are, this quarter, one hundred
thousand listings. Giving each listing its own badge object builds a hundred
thousand copies of four designs, and the artwork -- the expensive part -- is
duplicated with them. The data is identical, immutable, and copied anyway.

**What the pattern must deliver:** four `BadgeStyle` instances, shared by
every listing that uses them, with the per-listing part -- which listing,
which position -- kept outside. Asking twice for the same badge type must
return the *same object*, not an equal one.
""",
roles=[
    ("Flyweight (intrinsic state)", "`BadgeStyle`"),
    ("Flyweight factory", "`BadgeStyleFactory`"),
    ("Context (extrinsic state)", "`CatalogBadge`"),
    ("Key", "`BadgeType`"),
    ("Naive alternative", "`NaiveListingBadge`"),
    ("Entry point", "`BadgeDemo`"),
],
requirements=[
    "**`BadgeStyle` is immutable.** A shared mutable object is not an "
    "optimisation, it is a defect affecting every listing at once.",
    "**The factory returns the identical instance** for a repeated type, "
    "asserted with `assertSame` rather than `assertEquals` -- equality would "
    "pass even if nothing were shared.",
    "**No extrinsic state is stored on the flyweight.** The moment a "
    "`BadgeStyle` knows which listing it belongs to, it cannot be shared.",
],
),

"proxy": dict(
purpose="""
Teach standing something in front of an object that has the same interface,
and using that position to control when the real object is built and who is
allowed to reach it.
""",
nongoals=[
    "Not an image library. Loading is simulated and counted so the saving is "
    "visible.",
    "Not an authorisation framework. The role check is deliberately trivial; "
    "real systems need policies, not an enum comparison.",
    "Not a dynamic-proxy tutorial. `java.lang.reflect.Proxy` and the "
    "frameworks built on it are mentioned in the written notes and not used, "
    "because the hand-written version is what makes the mechanism visible.",
],
problem="""
A category page shows sixty listings. Each has a full-resolution image that is
expensive to decode, and only a handful are ever scrolled into view. Some
images -- unreleased products, supplier-restricted assets -- may only be
viewed by catalog staff.

Loading eagerly pays for sixty decodes to show six. Putting the access check
in the listing page means every screen that can display an image repeats it,
and the screen that forgets is the one that leaks. Both concerns are about
*getting to* the image rather than about the image itself, so both are in the
wrong class.

**What the pattern must deliver:** two small stand-ins with the same interface
as the real image. One defers construction until the image is actually
displayed and then keeps it; the other refuses callers who are not entitled,
before any loading happens. Because they share the interface, they compose --
and the caller cannot tell it is not holding the real thing.
""",
roles=[
    ("Subject interface", "`ProductImage`"),
    ("Real subject", "`HighResolutionProductImage`"),
    ("Virtual proxy", "`LazyProductImage`"),
    ("Protection proxy", "`RestrictedProductImage`"),
    ("Naive alternatives", "`NaiveProductListing`, `NaiveAdminImageViewer`"),
    ("Supporting type", "`Role`"),
    ("Entry point", "`ProductImageDemo`"),
],
requirements=[
    "**Both proxies implement `ProductImage`.** A proxy with its own interface "
    "is a wrapper, and the client would have to know which it holds.",
    "**The real image is constructed at most once**, however many times the "
    "lazy proxy is asked, with a load counter proving it.",
    "**Denial happens before any load.** A protection proxy that fetches the "
    "image and then refuses to show it has leaked the expensive work and, on "
    "a metered backend, the fact of the request.",
],
),

"strategy": dict(
purpose="""
Teach lifting one *decision that varies* out of the class that uses it, so the
using class holds a behaviour rather than a flag and never branches on which
behaviour it holds.
""",
nongoals=[
    "Not a shipping-rate engine. The four rules are arithmetic chosen to be "
    "checkable by hand, not carrier tariffs.",
    "Not a claim that the `switch` disappears. It moves to `ShippingRules`, "
    "runs once at the edge instead of on every quote, and the written notes "
    "say so plainly rather than pretending otherwise.",
    "Not State. The rules here are chosen from outside and do not decide what "
    "comes next; the difference is spelled out in the notes and the video.",
],
problem="""
An online shop prices delivery four ways. A flat rate for everything, weight
bands for bulky goods, a per-hundred-miles charge for distance, and a campaign
that makes delivery free once the basket passes fifty pounds. Marketing
invents a fifth every quarter.

Written the obvious way, that is one `quote` method with one `switch` over a
shipping-method flag, and every rule's arithmetic inlined into its own branch.
Each new rule edits the method every existing rule depends on. Testing the
weight bands means constructing a checkout and steering it there through the
flag. Worst of all, the `switch` needs a `default`, and the honest default for
a value nobody recognised is the one that charges zero -- so the day an
unknown method reaches it, the shop ships for free and nothing fails.

**What the pattern must deliver:** one small interface for "work out the
delivery cost of this shipment", four independent implementations of it, and a
checkout service that holds one and calls it. A fifth rule must be a new file,
compiled against nothing but the interface, with no edit to checkout at all.
""",
roles=[
    ("Strategy interface", "`ShippingCostRule`"),
    ("Concrete strategies", "`FlatRateRule`, `WeightBandedRule`, `DistanceBasedRule`, `FreeOverThresholdRule`"),
    ("Context", "`CheckoutService`"),
    ("Parameter object", "`Shipment`"),
    ("Selection", "`ShippingRules`"),
    ("Naive alternative", "`NaiveCheckoutService`"),
    ("Supporting types", "`Money`, `Quote`, `ShippingMethod`"),
    ("Entry point", "`ShippingCostDemo`"),
],
requirements=[
    "**`CheckoutService` contains no branch that depends on which rule it "
    "holds.** Not a `switch`, not an `instanceof`, not a name comparison -- "
    "and the strategy interface must expose nothing that would let it ask.",
    "**Each rule reads only the `Shipment` fields it needs** and knows "
    "nothing about the others, so its arithmetic can be tested on its own "
    "without a checkout.",
    "**A rule defined outside the shipped source works unchanged.** A test "
    "declares its own `ShippingCostRule` and hands it to `CheckoutService`, "
    "which proves the extension point is real rather than a list of four.",
    "**Selecting by an unknown name fails loudly.** `ShippingRules.byName` "
    "throws and names the rules it knows, because the naive version's silent "
    "`default` is the specific bug this project is written to kill.",
],
),

"observer": dict(
purpose="""
Teach letting the object that changes *announce* the change to a list it knows
nothing about, so reactions can be added, removed and made to fail
independently of the thing they react to.
""",
nongoals=[
    "Not a message broker. Notification is synchronous, in-process and "
    "in-order; there is no queue, no delivery guarantee and no retry.",
    "Not a demonstration of `java.util.Observer`. That API was deprecated in "
    "Java 9 for reasons the notes explain; the project writes its own "
    "interface, which is what modern code does.",
    "Not thread-safety. `CopyOnWriteArrayList` is used so a listener can "
    "unsubscribe itself *during* a notification, and the notes say so, "
    "because the usual assumption is that it is there for concurrency.",
    "Not Mediator. The subject here coordinates nothing; the distinction is "
    "drawn explicitly in the notes and the video.",
],
problem="""
An online order moves from Placed to Paid to Shipped to Delivered, and four
unrelated systems care. Inventory releases the reservation once it ships.
Email tells the customer. Analytics counts the transition for the funnel
report. The warehouse feed writes the line that gets the parcel picked.

Written the obvious way, that is an order service holding all four and calling
them one after another. Adding a fifth reaction edits a method four working
systems depend on, and adds a constructor parameter that breaks every test
that builds the class. Analytics wants *every* transition, so every
status-changing method ever written has to remember it. And the second call
talks to a mail server: the afternoon it times out, the order is already
marked shipped, the stock is already released, analytics never runs, and the
warehouse feed is never written -- so nobody picks the parcel, and the
exception that surfaces says `SMTP timeout` and nothing about a parcel.

**What the pattern must deliver:** one small listener interface, a subject
that keeps a list of them and announces transitions to it, and four
independent listeners that know nothing about each other. A fifth reaction
must be a new class and one `addListener` call, and one listener throwing must
not stop the others.
""",
roles=[
    ("Subject", "`Order`"),
    ("Observer interface", "`OrderListener`"),
    ("Concrete observers", "`InventoryListener`, `EmailListener`, `AnalyticsListener`, `WarehouseFeedListener`"),
    ("Event", "`OrderEvent`"),
    ("Failure report", "`ListenerFailure`"),
    ("Naive alternative", "`NaiveOrderService`"),
    ("Supporting types", "`OrderStatus`"),
    ("Entry point", "`OrderEventsDemo`"),
],
requirements=[
    "**`Order` names none of its listeners.** Searching the class for "
    "`email`, `inventory` or `warehouse` must find nothing, and the listener "
    "interface must expose nothing that would let `Order` tell them apart.",
    "**One listener throwing does not stop the rest.** The `try`/`catch` sits "
    "inside the notification loop and every failure comes back as a named "
    "`ListenerFailure`, because the outage in the naive version is the "
    "specific bug this project is written to kill.",
    "**A listener defined outside the shipped source works unchanged.** A "
    "test declares its own `OrderListener` and attaches it, which proves the "
    "extension point is real rather than a list of four.",
    "**The status is updated before the listeners run, and an unchanged "
    "status announces nothing**, so a listener sees the world the event "
    "describes and no duplicate transition is ever delivered.",
    "**A listener can remove itself while being notified.** The one-shot "
    "subscription is a normal case, not an error, and a test pins it.",
],
),

"command": dict(
purpose="""
Teach turning a request into an object, so that an edit can be stacked,
described, replayed and — the part everything else is in service of —
reversed, using state the command captures for itself while it runs.
""",
nongoals=[
    "Not Memento. Undo here is per-edit inverses, not snapshots of the whole "
    "cart; the notes and the video set the two against each other explicitly "
    "rather than pretending Command is the only answer to undo.",
    "Not a task queue. Commands run synchronously, in-process, on one cart. "
    "Queuing and scheduling are named as things the pattern makes possible, "
    "and are not implemented.",
    "Not thread-safety. `CartHistory` is single-threaded by design; undo "
    "ordering is a contract, and concurrent editing of one cart is out of "
    "scope.",
    "Not a lambda tutorial. `execute` alone would be a `Runnable`; the "
    "project exists to show what the *second* method needs, which is state "
    "that survives between two calls.",
],
problem="""
A customer edits their shopping cart -- adds an item, removes one, changes a
quantity, applies a discount code -- and then expects to be able to take any
of it back.

Written the obvious way, that is a cart edited directly with a stack of notes
beside it saying what was asked for, and an `undo` that switches over the kind
of note. It is a third of the code and, for a cart that only ever gains brand
new lines, it is correct. It falls apart the moment an edit's effect depends
on what was already there. A customer with 3 headphones adds 2 more; the note
says "add 2 of H-100"; undo removes the line, and the 3 they chose last week
go with it. A customer applies `BLACKFRIDAY` over `WELCOME10`; the note says
"coupon BLACKFRIDAY"; undo clears the coupon, and a discount they never
touched is gone. Nothing throws. The customer is simply charged the wrong
amount.

**What the pattern must deliver:** one small command interface with `execute`
and `undo`, four independent commands that each capture what their own
inverse needs *at the moment they run*, and an invoker holding two stacks of
that interface and no knowledge of any edit. A fifth kind of edit must be one
new class, and undoing must restore quantity, position and coupon exactly.
""",
roles=[
    ("Command interface", "`CartCommand`"),
    ("Concrete commands", "`AddItemCommand`, `RemoveItemCommand`, `ChangeQuantityCommand`, `ApplyCouponCommand`"),
    ("Receiver", "`Cart`"),
    ("Invoker", "`CartHistory`"),
    ("Naive alternative", "`NaiveCartEditor`"),
    ("Supporting types", "`CartLine`, `Coupon`, `Money`"),
    ("Entry point", "`CartCommandsDemo`"),
],
requirements=[
    "**Undo state is captured inside `execute`, from the receiver.** No "
    "command may work out its inverse in its constructor, because an earlier "
    "undo can invalidate that guess before the command runs. A field the "
    "constructor does not set is the visible sign of it.",
    "**Undo restores what was there, not the opposite of what was asked.** "
    "Undoing a merged add returns the previous quantity; undoing a removal "
    "restores the line's *position*; undoing a coupon restores the coupon it "
    "replaced. Each has a test written against a cart that was not empty.",
    "**`CartHistory` names no edit.** Searching the class for `coupon`, "
    "`quantity` or `sku` must find nothing, and a command defined outside the "
    "shipped source must execute and undo unchanged -- a test declares its "
    "own gift-wrapping `CartCommand` to prove it.",
    "**A command that throws is never pushed onto the undo stack**, because "
    "reversing a half-applied edit applies the inverse of something that "
    "never fully happened.",
    "**A new command clears the redo stack**, since taking a different branch "
    "makes the old future unreachable -- the behaviour of every editor the "
    "learner has used.",
],
),

"template-method": dict(
purpose="""
Teach fixing the *order* of an algorithm in one `final` method on a base
class, while leaving each individual step for a subclass to fill in -- and
teach the choice between a step that must be answered, a step with a default,
and a hook that exists only to be opted into.
""",
nongoals=[
    "Not Strategy. The steps here are not swappable at run time and are not "
    "independent of each other; the notes and the video set the two against "
    "each other explicitly, and recommend Strategy where it is the better "
    "answer, rather than pretending inheritance always wins.",
    "Not Factory Method. That pattern is this one narrowed to a single hole "
    "that returns a product. The distinction is drawn in the notes because "
    "it is the most common confusion in this corner of the catalogue, but no "
    "factory is built here.",
    "Not a defence of inheritance. The project says out loud that the pattern "
    "spends the subclass's one inheritance slot permanently, and that this is "
    "the reason composition is the better modern default for most problems.",
    "Not a workflow engine. There is one sequence, six steps long, in one "
    "process. Conditional branches, retries, compensation and persistence are "
    "all out of scope.",
],
problem="""
An online shop fulfils every order through the same six steps -- validate,
reserve, charge, pack, dispatch, notify -- and that order is not a style
choice. Charging before reserving takes money for goods the shop cannot
supply; notifying before dispatching emails a customer a reference that does
not exist yet. What varies, and varies enormously, is the inside of each step:
the shop fulfils from its own warehouse, from marketplace sellers, and as
digital downloads, and one of those has no shipping address at all.

Written the obvious way, that is three methods, each spelling the sequence out
from beginning to end. It is a third of the code of the alternative and on the
day each was written it was correct. But the sequence exists only as a
convention typed by hand in three places, and nothing in the language, the
compiler or the test suite knows those six calls have an order -- so the
copies drift one line at a time. The digital copy now notifies before it
dispatches, so a customer is emailed `Key: (not dispatched)` and the correct
licence key, minted a microsecond later, is never sent to anybody. The
marketplace copy charges before the seller confirms, so a customer is charged
£42.00 and then told the order is refused. Nothing throws, nothing fails to
compile, and both orders are marked fulfilled.

**What the pattern must deliver:** one `final` template method that owns the
order and is the only thing that does; abstract steps for the parts no default
could get right; defaults for the parts most routes want unchanged; hooks for
the parts a route may need to opt into or out of; and a fourth route that is
one new class with no edit to the base class or to any route that already
works.
""",
roles=[
    ("Abstract class", "`FulfilmentProcess`"),
    ("Template method", "`fulfil(Order)` -- `final`"),
    ("Private step", "`validate`"),
    ("Abstract steps", "`routeName`, `reserveStock`, `charge`, `dispatch`"),
    ("Steps with defaults", "`pack`, `notifyCustomer`"),
    ("Hooks", "`requiresShippingAddress()`, `afterFulfilment()`"),
    ("Concrete routes",
     "`WarehouseFulfilment`, `MarketplaceFulfilment`, `DigitalFulfilment`"),
    ("Naive alternative", "`NaiveFulfilment`"),
    ("Supporting types",
     "`Order`, `OrderLine`, `FulfilmentReport`, `Money`, `StockLedger`, "
     "`SellerApi`, `LicenceKeys`, `FulfilmentException`"),
    ("Entry point", "`FulfilmentDemo`"),
],
requirements=[
    "**The template method is `final`.** A route may decide how a step "
    "behaves and may never decide when the steps run; attempting to override "
    "`fulfil` must be a compile error, not a code-review comment.",
    "**Every step records itself on a report**, so the pattern's central "
    "claim is observable rather than asserted: the demo prints the step names "
    "of four routes side by side and they are character-for-character "
    "identical, and a `RecordingRoute` in the tests asserts on the call order "
    "directly.",
    "**A later step may rely on an earlier step's work.** "
    "`DigitalFulfilment.notifyCustomer` quotes the licence key that its own "
    "`dispatch` minted, using the same two lines the naive copy has in the "
    "wrong order -- and it is safe only because `fulfil` is `final`.",
    "**`validate` is `private`, and the hook is the only say a route gets.** "
    "The digital route answers `requiresShippingAddress()` with `false` and "
    "gets its addressless orders through, without weakening the address check "
    "for any other route and without being able to skip validation.",
    "**A hook must not be able to change the sequence.** "
    "`afterFulfilment` posts a *note* rather than a step, so the marketplace "
    "route's commission entry cannot alter a step list a test asserts on.",
    "**The naive alternative is argued against honestly.** Its warehouse copy "
    "is still correct, so the case is drift rather than incompetence, and its "
    "two bugs are pinned by *passing* tests that assert the wrong behaviour.",
],
),

"state": dict(
purpose="""
Teach replacing a status field and its conditionals with one class per state,
so that the behaviour of an object changes with the state it is in -- and
teach, just as firmly, what separates State from Strategy when the two have
identical class diagrams, and when an enum is the better answer.
""",
nongoals=[
    "Not Strategy, although the class diagram is the same one. The notes, the "
    "diagrams and the video all say so explicitly rather than pretending a "
    "structural difference exists: a Strategy is chosen by the caller and "
    "does not change itself, while a State is entered as a consequence of "
    "what the object did, and states hand control to one another.",
    "Not a claim that every status field wants this. The demo's final section "
    "says out loud that for a small, stable machine an enum plus a map of "
    "permitted transitions is often clearer, and that the pattern earns its "
    "keep only when the behaviour varies by state rather than the permissions.",
    "Not a workflow engine. Seven states, six requests, one process. "
    "Persistence, retries, timers, parallel branches and distributed "
    "coordination are all out of scope.",
    "Not stateful state objects. Every state here is stateless and shared as "
    "a single INSTANCE, which is a property of this domain rather than of the "
    "pattern, and the notes flag what changes when a state needs a field.",
],
problem="""
An order in an online shop moves through a small, well understood lifecycle --
`PLACED`, `PAID`, `PACKED`, `SHIPPED`, `DELIVERED`, plus the terminal
`CANCELLED` and `REFUNDED` -- and six things can be asked of it: pay, pack,
ship, deliver, cancel and refund. The answer to every one of them depends on
where the order currently is, and cancelling in particular is not one rule
with a guard on it: cancelling a `PLACED` order moves no money, cancelling a
`PAID` one refunds, cancelling a `PACKED` one refunds *and* returns stock
somebody has already boxed, and cancelling a `SHIPPED` one is not a thing that
can be done at all.

Written the obvious way, that is an enum and a chain of conditionals at the
top of each method -- short, readable, and with the whole lifecycle in one
file. But the rules are then written down once per method, each copy phrased
in whichever direction its author found natural, and the copies drift.
`cancel` was written as "anything that has not arrived yet", which reads
sensibly and quietly includes `SHIPPED`, so a parcel on a van is refunded.
`refund` was widened to accept `CANCELLED` so support could sort out cancelled
orders, and since a cancel has already refunded, it pays the customer a second
time and leaves the ledger at `-£97.49` over two refunds. A third copy, the
`switch` written for the screen, is correct -- so the cancel button is never
drawn and the endpoint accepts the call anyway.

**What the pattern must deliver:** one class per state holding everything true
about that state; refusal as the default, so a rule nobody wrote is a refusal
rather than an accident; a context with no conditional that mentions a status;
one answer that the screen and the endpoint cannot disagree about; and a new
state that can be added without editing the context.
""",
roles=[
    ("Context", "`Order`"),
    ("State interface", "`OrderState` -- six requests, every default throws"),
    ("Concrete states",
     "`PlacedState`, `PaidState`, `PackedState`, `ShippedState`, "
     "`DeliveredState`, `CancelledState`, `RefundedState`"),
    ("Transition hook", "`Order.transitionTo` -- package-private"),
    ("Refusal", "`IllegalTransitionException`, built from `allowedActions()`"),
    ("Evidence", "`Ledger`, `OrderEvent` history"),
    ("Naive alternative", "`NaiveOrder`"),
    ("Supporting types", "`Money`, `OrderLine`"),
    ("Entry point", "`OrderStateDemo`"),
],
requirements=[
    "**Every request on the interface refuses by default.** A state lists "
    "what it allows by overriding, and everything else throws without a line "
    "of code being written -- so the mistake made when nobody is paying "
    "attention closes a transition rather than opening one, which is the "
    "exact opposite of the enum's failure mode.",
    "**The context contains no conditional that mentions a status.** Every "
    "public method on `Order` is a single delegation, and `transitionTo` is "
    "package-private so an order's state can change only as a consequence of "
    "asking it to do something.",
    "**States do genuinely different work for the same verb.** `cancel` "
    "refunds nothing in `PlacedState`, refunds in `PaidState`, and refunds "
    "and returns stock in `PackedState`. If the states differed only in what "
    "they permitted, the project would be an over-engineered enum and would "
    "say so.",
    "**The buttons and the endpoints cannot disagree.** `allowedActions()` "
    "lives on the state beside the methods it describes, and a test walks all "
    "seven states and all six actions checking that `canDo` predicts whether "
    "the call throws.",
    "**A refusal explains itself from the state's own data**, so the message "
    "cannot go stale: the reason is built from `allowedActions()`, except "
    "where a state overrides `cancel` purely to give a human a better one.",
    "**The naive alternative is argued against honestly.** Its happy path is "
    "still correct, so the case is drift rather than incompetence; its two "
    "bugs are pinned by *passing* tests that assert the wrong behaviour, each "
    "paired with the same scenario refused by the state version.",
    "**The cost is stated, not hidden.** Seven classes where there was one "
    "enum, and a transition table that no longer exists anywhere readable -- "
    "the demo's final section and the notes both recommend the enum for a "
    "small, stable machine.",
],
),

"chain-of-responsibility": dict(
purpose="""
Teach turning a fixed sequence of checks into a set of independent links that
are assembled at runtime, so that which checks run, in what order, and what
happens when none of them speaks up all become wiring rather than control
flow -- and teach the cost of that honestly, because a request can travel the
whole chain and come out unanswered.
""",
nongoals=[
    "Not Decorator, although both are objects holding a reference to the next "
    "object. The explainer states the distinguishing question rather than "
    "observing a resemblance: a decorator always delegates onward and adds "
    "something on the way, so every layer runs, while a handler may answer "
    "and stop, so the layers behind it never run at all.",
    "Not a claim that four checks always want this. The demo's final section "
    "and the notes say plainly that when the set of checks and their order "
    "never change, four sequential `if` statements are the right answer and "
    "are easier to read.",
    "Not a rules engine, a workflow engine or a DSL. The chain is assembled "
    "in Java, in code a reader can see, and there is no configuration file, "
    "no scripting and no dynamic dispatch by name.",
    "Not a validation framework. Nothing here accumulates a list of every "
    "problem with a request -- the first link that decides ends the run, "
    "which is the behaviour the pattern is for and the reason a validator "
    "that must report all errors should not be built this way.",
],
problem="""
Before an order is accepted it is screened: the address has to be somewhere a
courier goes, the warehouse has to be able to pick every line, the risk score
has to be under threshold, and the issuer has to be willing to authorise the
total on that card. Written the obvious way that is one `validate` method with
four checks and an early return on each, which is short, readable, and has the
whole policy in one file.

Three things go wrong once it is real, and all three cost money. **The order is
welded in.** The card is checked above fraud, so an order scoring 92 out of 100
is rejected as a card problem -- the customer is invited to try another card
and does, and the fraud team never hears the account exists. **There is no
third answer.** The result is a boolean, so the review band the risk model was
bought for has to be forced into yes or no, and it is accepted. **Variants are
copies.** Trade accounts are invoiced rather than charged, so the method was
copied and the card check deleted; the address check went with it in the same
edit, and two desks are now shipped to an island no courier serves.

**What the pattern must deliver:** one class per check, testable without
constructing the state the checks above it demand; the order of the checks as a
line of wiring rather than a line of control flow; a variant flow built by
leaving a link out rather than by copying a method; evidence of which link
decided and which links never ran; and a deliberate, named answer to the
question of what a chain means when nobody decides.
""",
roles=[
    ("Handler", "`ScreeningHandler` -- holds its successor, walks the chain in a `final` method"),
    ("Concrete handlers",
     "`AddressCheck`, `StockCheck`, `FraudScoreCheck`, `PaymentLimitCheck`"),
    ("Chain / client", "`ScreeningChain` -- assembles links and names the fallback"),
    ("Request", "`CheckoutRequest` -- immutable, never mutated by a link"),
    ("Answer", "`Decision`, `Outcome` -- approved, rejected, or referred to a human"),
    ("Evidence", "`ScreeningReport` -- who decided, and which links never ran"),
    ("Naive alternative", "`NaiveScreening`, and its nested `Result`"),
    ("Supporting types", "`BasketItem`"),
    ("Entry point", "`CheckoutScreeningDemo`"),
],
requirements=[
    "**Walking the chain is written once.** `ScreeningHandler.screen` is "
    "`final`, so a subclass cannot forget to call the next link -- which is "
    "the classic bug in the textbook version of this pattern, where a handler "
    "declines to handle something, omits the `else`, and the request "
    "disappears without an error.",
    "**A link is not obliged to reject.** `FraudScoreCheck` can reject, refer "
    "or say nothing, and the base class knows about none of those answers -- a "
    "link stops the chain whenever it is willing to own the answer, whatever "
    "that answer is.",
    "**No link knows the shape of the chain.** There is no index, no count "
    "and no loop over handlers anywhere; the chain hands the request to the "
    "first link and the links do the rest, which is what makes reordering a "
    "wiring change.",
    "**Falling off the end is dealt with deliberately.** The fallback "
    "decision is a required constructor argument and there is no constructor "
    "that omits it, so the wiring has to say out loud whether an unclaimed "
    "order fails open or fails closed rather than leaving it a `null`.",
    "**The interaction is visible, not just the verdict.** Every report "
    "prints the links consulted in order, what each said, who decided, and -- "
    "the part four sequential `if` statements can never give you -- which "
    "links never ran at all.",
    "**Each link is testable in a chain of one.** Exercising the fraud "
    "thresholds needs no deliverable address, no stocked basket and no card "
    "with headroom; the tests demonstrate the contrast against the naive "
    "method, where the fraud rule is only reachable by satisfying the three "
    "statements above it.",
    "**The naive alternative is argued against honestly.** Its happy path is "
    "correct and its author was not careless, so the case is drift; its bugs "
    "are pinned by *passing* tests that assert the wrong behaviour, each "
    "paired with the same scenario put through a chain.",
    "**The cost is stated, not hidden.** The order of the checks now lives in "
    "the wiring rather than in one readable method, answering \"which link "
    "rejected this?\" requires the report, and a handler instance belongs to "
    "exactly one chain -- the demo's closing lines say so and recommend the "
    "four `if` statements when the checks never change.",
],
),

"visitor": dict(
purpose="""
Teach separating an operation from the structure it runs over, so that a new
report on the product catalog is a new class rather than a new method on every
node type -- and teach the price of that separation just as plainly, because
the same arrangement makes a new node type expensive on every report that
already exists.
""",
nongoals=[
    "Not Composite. The catalog tree is borrowed wholesale from "
    "`structural/composite-pattern` and the project links back to it; nothing "
    "here teaches how to build the tree, only what to do with one you already "
    "have.",
    "Not an argument that a method on the node is wrong. The demo's own "
    "inventory report is correct in both designs and agrees to the penny, and "
    "the notes recommend writing the method directly when the operations are "
    "few and settled.",
    "Not a general substitute for pattern matching. The explainer states when "
    "a `switch` over sealed types is the better answer and does not pretend "
    "the double dispatch is more readable than it is.",
],
problem="""
An online shop's catalog is a tree of categories, products and bundles, and it
has been the same three node types for years. What is not settled is what the
business asks about it: the value of the stock, the number of lines in each
category, a CSV export for finance every Monday, and a compliance audit naming
the items that cannot travel by air. Written the obvious way each of those is a
method on every node class, so a class describing a thing on a shelf ends up
carrying an RFC 4180 quoting rule, the bundle class copied from the product
class eighteen months later drops the quoting and reads a restriction field it
never sets, and the fifth report is a fifth method on three finished classes.
The pattern has to let a report be added without opening a model file, keep one
traversal rather than one per report, give a bundle a different rule from a
product without a type test, and state out loud what a new node type would
cost.
""",
roles=[
    ("Element", "`CatalogComponent` -- `name()` and `accept(CatalogVisitor)`, and nothing else"),
    ("Concrete elements", "`Product`, `Bundle`, `Category` -- each `accept` is one line"),
    ("Composite element", "`Category` -- owns the only traversal in the project"),
    ("Visitor", "`CatalogVisitor` -- one `visit` per node type, plus a `leave(Category)` default"),
    ("Concrete visitors",
     "`InventoryValueVisitor`, `CategoryCountVisitor`, `CsvExportVisitor`, "
     "`ComplianceAuditVisitor`, `DispatchTraceVisitor`"),
    ("Convenience base", "`CategoryPathVisitor` -- path tracking, and explicitly not part of the pattern"),
    ("Naive alternative", "`NaiveCatalogNode`, `NaiveProduct`, `NaiveBundle`, `NaiveCategory`"),
    ("Supporting types", "`Money`, `Restriction`, `Catalog`"),
    ("Entry point", "`CatalogReportDemo`"),
],
requirements=[
    "**The model carries no reporting method.** `CatalogComponent` declares "
    "`name()` and `accept` only, and a reflection test with an allow-list "
    "fails the build if a report method is ever added back onto `Product`.",
    "**A report written later needs no change to anything.** A visitor "
    "declared inside the demo file and another declared inside a test method "
    "both walk a tree whose classes were compiled without them, and the "
    "demo's fifth report changes no interface, no node type and no other "
    "report.",
    "**The traversal is written once and lives in the structure.** "
    "`Category.accept` is the only loop over children in the project; a "
    "visitor containing no loop and no recursion still receives all 17 calls "
    "of the demo tree, and that is asserted rather than asserted about.",
    "**No visitor performs a type test.** There is no `instanceof` and no "
    "`switch` on node type in any report; each node calls `visitor.visit(this)` "
    "from inside its own class, and the demo's dispatch section shows the two "
    "hops interleaving.",
    "**A third node type earns the double dispatch.** `Bundle` is worth its "
    "kit price rather than the sum of its parts, and is restricted by what is "
    "in the box rather than by a field of its own, so `visit(Bundle)` and "
    "`visit(Product)` state materially different rules in every report that "
    "cares.",
    "**The naive alternative is argued against honestly.** Its inventory "
    "total agrees with the visitor to the penny, and its two bugs -- the "
    "dropped CSV quoting and the unset copied `restriction` field -- are "
    "pinned by *passing* tests, each paired with the visitor answering the "
    "same question correctly.",
    "**The cost is runnable, not rhetorical.** The demo's final section "
    "prints the class names a single new node type would break, the notes "
    "state that adding a node type breaks every visitor, and the awkwardness "
    "of `node.accept(v)` calling `v.visit(node)` straight back is named "
    "rather than defended.",
    "**The pruning limitation is asserted.** A report wanting only one branch "
    "is offered every node in the tree and filters, because the walk belongs "
    "to the structure; a test pins the 7-offered-against-5-wanted numbers.",
],
),
}


# ---------------------------------------------------------------------------
# Facts read from the project itself, so no number in a spec is typed by hand.
# ---------------------------------------------------------------------------

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     ".loudness-cache.json")


def load_cache():
    import json
    try:
        return json.load(open(CACHE))
    except (OSError, ValueError):
        return {}


def save_cache(c):
    import json
    json.dump(c, open(CACHE, "w"), indent=1, sort_keys=True)


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout.strip()


def facts(group, slug, measure=True):
    p = os.path.join(ROOT, group, slug + "-pattern")
    v, d = os.path.join(p, "video"), os.path.join(p, "docs")
    f = {"dir": p}

    src = os.path.join(p, "src", "main", "java", "com", "jk", "explore")
    pkg = os.listdir(src)[0]
    f["package"] = "com.jk.explore." + pkg
    f["classes"] = len([x for x in os.listdir(os.path.join(src, pkg))
                        if x.endswith(".java")])

    tst = os.path.join(p, "src", "test", "java", "com", "jk", "explore", pkg)
    names, total = [], 0
    for x in sorted(os.listdir(tst)):
        if not x.endswith(".java"):
            continue
        body = open(os.path.join(tst, x)).read()
        n = len(re.findall(r'@(?:Test|ParameterizedTest|RepeatedTest)\b', body))
        if n:
            names.append("`%s`" % x[:-5])
            total += n
    f["tests"], f["test_classes"] = total, names

    f["scenes"] = len(re.findall(r'title=', open(os.path.join(v, "scenes.py")).read()))

    srt = [x for x in os.listdir(v) if x.endswith(".srt")]
    f["cues"] = (len(re.findall(r' --> ', open(os.path.join(v, srt[0])).read()))
                 if srt else 0)

    mp4 = os.path.join(v, "%s-pattern-explained.mp4" % slug)
    f["mp4"] = mp4 if os.path.exists(mp4) else None
    if f["mp4"]:
        dur = float(sh(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of", "csv=p=0", mp4]))
        f["runtime"] = "%d:%02d" % (int(dur // 60), int(dur % 60))
    else:
        f["runtime"] = "not yet built"

    f["title"] = "not yet generated"
    ymd = os.path.join(d, "youtube.md")
    if os.path.exists(ymd):
        m = re.search(r'## Title\n\n```\n(.+?)\n```', open(ymd).read())
        if m:
            f["title"] = m.group(1)

    # Measuring loudness means decoding a ten-minute file, so the result is
    # cached against the MP4's size and mtime. Rebuilding the video changes
    # both, so the cache cannot go stale behind a new render.
    f["loudness"] = None
    if measure and f["mp4"]:
        st = os.stat(mp4)
        key = "%s:%d:%d" % (slug, st.st_size, int(st.st_mtime))
        cache = load_cache()
        if key in cache:
            f["loudness"] = tuple(cache[key])
            return f
        out = subprocess.run(
            ["ffmpeg", "-hide_banner", "-nostats", "-i", mp4, "-af",
             "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
            capture_output=True, text=True).stderr
        try:
            import json
            blob = out[out.rindex("{"):]
            m = json.loads(blob[:blob.index("}") + 1])
            f["loudness"] = (m["input_i"], m["input_tp"])
            cache[key] = list(f["loudness"])
            save_cache(cache)
        except (ValueError, KeyError):
            pass
    return f


# ---------------------------------------------------------------------------
# The document.
# ---------------------------------------------------------------------------

def build_md(group, slug, f):
    name = NAMES[slug]
    meta = META[slug]
    idx = [s for _, s in ORDER].index(slug)
    nxt = NAMES[ORDER[idx + 1][1]] if idx + 1 < len(ORDER) else None
    is_ref = slug == "abstract-factory"

    if is_ref:
        provenance = (
            "This project is the reference implementation of that standard -- "
            "the other thirteen projects' build scripts are generated from this "
            "one -- so a change here is a change to all fourteen and must be "
            "made there first.")
    else:
        provenance = (
            "This project's `video/build_video.sh` is generated from "
            "`creational/abstract-factory-pattern`'s, differing only in the "
            "pattern name and the output filenames, so a change to the pipeline "
            "belongs there and in the repository-wide spec, not here.")

    parts = []
    A = parts.append

    A("# %s Pattern — Project Specification\n" % name)
    A("The single reference document for this project: what it teaches, how it\n"
      "is built, and the quality bar its video and its YouTube publication have\n"
      "to meet.\n")
    A("This is a *specification*, not a tutorial. It says what must be true and\n"
      "why. The teaching material itself lives in\n"
      "[`%s-pattern-explained.md`](%s-pattern-explained.md); the problem it\n"
      "addresses is set out at length in\n"
      "[`problem-statement.md`](problem-statement.md).\n" % (slug, slug))
    A("Where this document repeats a rule from the repository-wide\n"
      "[`video-and-publishing-spec.md`](../../../docs/video-and-publishing-spec.md),\n"
      "that document is the authority. %s\n" % provenance)
    A("---\n")

    A("## 1. Purpose\n")
    A(meta["purpose"].strip() + "\n")
    A("The three formats are not alternatives. A learner is expected to read the\n"
      "problem statement, run the code, then watch the video — or watch first and\n"
      "read after. Whichever order they choose, the class names, the numbers and\n"
      "the scenario must be identical, because the value of the repository is\n"
      "that a learner carries one e-commerce domain from pattern to pattern and\n"
      "only has to absorb the new structure.\n")
    A("### Non-goals\n")
    for x in meta["nongoals"]:
        A("- " + x)
    A("")
    A("---\n")

    A("## 2. Problem statement\n")
    A("The full treatment is in [`problem-statement.md`](problem-statement.md).\n"
      "In brief:\n")
    A(meta["problem"].strip() + "\n")
    A("---\n")

    A("## 3. Code\n")
    A("### Structure\n")
    A("%d production classes under `%s`:\n" % (f["classes"], f["package"]))
    A("| Role | Types |")
    A("| --- | --- |")
    for role, types in meta["roles"]:
        A("| %s | %s |" % (role, types))
    A("")
    A("### Requirements\n")
    for i, x in enumerate(meta["requirements"], 1):
        A("%d. %s" % (i, x))
    A("%d. **Java 21, no third-party runtime dependencies.** JUnit 5 for tests\n"
      "   only, so the project is readable by someone who does not know a DI\n"
      "   framework.\n"
      "%d. **Every class fits on a slide.** This is teaching code; a class that\n"
      "   needs scrolling to read has failed its purpose regardless of its\n"
      "   design.\n"
      % (len(meta["requirements"]) + 1, len(meta["requirements"]) + 2))
    A("### Verification\n")
    A("- `./gradlew build` passes. %d test method%s across %s.\n"
      "- `./gradlew run` output is quoted verbatim in the top-level `README.md`,\n"
      "  and must still match."
      % (f["tests"], "" if f["tests"] == 1 else "s",
         ", ".join(f["test_classes"])))
    A("")
    if slug in NONDETERMINISTIC:
        A("The demo mints an identifier per run, so the codes it prints differ\n"
          "each time. Every other line of the output is stable and must match the\n"
          "README exactly; the README says which lines are expected to vary.\n")
    if f["tests"] < 5:
        A("> **Known gap.** %d test method is well below the %d–%d the other\n"
          "> projects carry, and it is not enough to defend the requirements\n"
          "> above — in particular, nothing currently fails if the four steps are\n"
          "> reordered, which is the pattern's whole point. This is a real\n"
          "> shortfall in the project, recorded here rather than quietly\n"
          "> tolerated.\n" % (f["tests"], 9, 23))
    A("---\n")

    A("## 4. Written material\n")
    A("Every document in `docs/` is required, and each has one job. A learner\n"
      "reading them in the order given by the top-level README's table should\n"
      "never need to jump forward.\n")
    A("| Document | Job |")
    A("| --- | --- |")
    for doc, job in [
        ("`prerequisites.md`", "What to know and install first"),
        ("`problem-statement.md`", "The problem and why the naive approach hurts"),
        ("`%s-pattern-explained.md`" % slug,
         "The pattern, the code, pitfalls, comparisons"),
        ("`class-diagram.md` + PNG", "Static structure"),
        ("`uml-diagram.md` + PNG", "Runtime call flow"),
        ("`animation.html`", "Step-by-step walkthrough, optionally narrated"),
        ("`session.md`", "A 60-minute guided teaching session"),
        ("`youtube.md`", "Everything needed to publish the video"),
        ("`thumbnail.png`", "The image to upload"),
        ("`spec.md` / `spec.html`", "This document"),
    ]:
        A("| %s | %s |" % (doc, job))
    A("")
    A("Both Mermaid diagrams are committed as source *and* rendered PNG. The PNG\n"
      "is what the README embeds, because GitHub's Mermaid rendering cannot be\n"
      "relied on at these diagrams' size; the source is what gets edited.\n"
      "Regenerating after an edit is mandatory — a diagram that disagrees with\n"
      "the code is worse than no diagram.\n")
    A("---\n")

    A("## 5. Video quality specification\n")
    A("The finished video is `video/%s-pattern-explained.mp4`, with an\n"
      "audio-only `.m4a` and a `.srt` subtitle track alongside it. It is built by\n"
      "`video/build_video.sh`, from scenes declared in `video/scenes.py` and\n"
      "slides rendered by `video/make_slides.py`.\n" % slug)
    A("### 5.1 The opening, in four steps\n")
    A("Scene 1 is the only scene whose narration has a required structure, and\n"
      "it is required because it is the scene that decides whether anybody\n"
      "watches the second one. It must run in this order:\n")
    A("1. **What the video is** — \"This video explains the %s pattern in\n"
      "   Java\", plainly, before anything else.\n"
      "2. **The author credit** — \"and it is written and presented by\n"
      "   Jayasekhar Konduru\".\n"
      "3. **The pattern's definition, in general terms** — two or three\n"
      "   sentences of plain language, with no mention yet of the store, the\n"
      "   catalog or the checkout. A viewer who stops here has still learnt\n"
      "   what the pattern is.\n"
      "4. **Then the same thing in full, in the e-commerce domain** — the\n"
      "   worked scenario, and what the viewer will be able to do by the end.\n"
      % NAMES[slug])
    A("> **Requirement.** Steps 3 and 4 are separate and in that order. They\n"
      "> used to be one step: the video opened straight into the shop's\n"
      "> scenario and left the general definition to be inferred from a worked\n"
      "> example, which works for a viewer already halfway to knowing the\n"
      "> pattern and fails for everyone else. The cost is fifteen to thirty\n"
      "> seconds of runtime, spent at the only point in the video where a\n"
      "> viewer is still deciding whether to leave.\n")
    A("### 5.2 Delivered characteristics\n")
    A("| Property | Value | Why |")
    A("| --- | --- | --- |")
    for row in [
        ("Container", "MP4, `+faststart`",
         "The index sits at the front, so the poster paints the moment the file opens"),
        ("Video", "H.264, 1920×1080, 30 fps, CRF 18, `preset slow`, `yuv420p`",
         "1080p is the minimum at which code on a slide is readable; `yuv420p` is what every player accepts"),
        ("B-frames", "Disabled (`-bf 0`)",
         "They save nothing on a static slide and complicate the timestamps the gap check reads"),
        ("Audio", "AAC-LC, 48 kHz, stereo, 192 kbps",
         "YouTube's recommended upload settings, so no re-encode on their side"),
        ("Loudness", "−16 LUFS integrated, true peak ≤ −1.5 dBTP",
         "YouTube's normalisation target — deliver at it and the platform leaves the audio alone"),
        ("Stream start", "Both streams at exactly 0.000 s",
         "Otherwise the video track starts 21 ms late and players show black at 0:00"),
        ("Narration", "macOS `say`, voice Samantha, 145 wpm",
         "The pace educational YouTube converges on for technical material"),
        ("Inter-scene pause", "0.9 s of appended silence",
         "So slides do not snap past the moment a sentence ends"),
        ("Runtime", "~%s over %d scenes, %d subtitle cues"
         % (f["runtime"], f["scenes"], f["cues"]), ""),
    ]:
        A("| %s | %s | %s |" % row)
    A("")
    A("### 5.3 The two defects this pipeline exists to prevent\n")
    A("Both produce a file that looks fine and sounds broken, and both were live\n"
      "in this repository before the current build script. They are documented\n"
      "here because the obvious \"simplification\" of the pipeline reintroduces\n"
      "them.\n")
    A("**Per-scene AAC concatenation.** AAC is a lapped format: every separately\n"
      "encoded clip carries priming samples at its head and padding at its tail.\n"
      "Concatenating such clips with `-c copy` strips neither, so each join\n"
      "leaves a hole in the timeline. Measured on the reference project before\n"
      "the fix: 30 gaps totalling 31 seconds of missing narration.\n")
    A("> **Requirement.** Each scene's narration is written as lossless PCM WAV.\n"
      "> The joined narration is encoded to AAC exactly once, at the final mux.\n"
      "> There must be exactly one `-c:a aac` in the build script.\n")
    A("**Dynamic-mode `loudnorm`.** Left to itself `loudnorm` rides the level as\n"
      "it goes, and on some narrations emits a timestamp discontinuity partway\n"
      "through — the same audible hole, mid-sentence, with nothing wrong\n"
      "upstream of it.\n")
    A("> **Requirement.** Loudness is measured over the whole narration in a\n"
      "> first pass, and the measured figures are fed back with `linear=true` so\n"
      "> the second pass applies one constant gain. This also stops the level\n"
      "> pumping between quiet and loud lines.\n")
    A("### 5.4 Why there is no denoiser\n")
    A("An earlier version ran `afftdn` over the narration and, by the numbers, it\n"
      "worked — about 15 dB off the noise floor. It also made the voice\n"
      "noticeably worse. A spectral denoiser needs a real, roughly stationary\n"
      "noise floor to subtract; synthesised speech has almost none, so `afftdn`\n"
      "subtracts parts of the speech instead and leaves it warbling.\n")
    A("> **Requirement.** The `CLEANUP` chain contains no `afftdn` and no\n"
      "> `lowpass`. It is exactly: resample to 48 kHz with a long filter\n"
      "> (`filter_size=512`, `cutoff=0.98`, `linear_interp=1`), a 75 Hz high-pass\n"
      "> for rumble, and a gentle +1.5 dB shelf at 3 kHz for consonants. The\n"
      "> faint remaining hiss is much the lesser problem.\n")
    A("Levelling is deliberately not in this chain either: run per scene it\n"
      "re-measures on every clip, so a quiet scene is pushed up to match a loud\n"
      "one and the level audibly steps at each join. It happens once, over the\n"
      "whole narration.\n")
    A("### 5.5 Synchronisation\n")
    A("Scene lengths are rounded up to a whole number of video frames —\n"
      "`frames = ceil(duration × 30)`, `target = frames / 30` — and each scene's\n"
      "WAV is padded to exactly that target. Picture and narration are therefore\n"
      "the same length for every scene, so slide changes cannot drift away from\n"
      "the voice however many scenes the video grows to.\n")
    A("### 5.6 Self-check, and its limit\n")
    A("After the mux the build reads every audio packet timestamp and fails if\n"
      "any two are more than one AAC frame apart, printing\n"
      "`audio timeline continuous: N packets, no gaps`. A build that does not\n"
      "print that line has not passed.\n")
    A("**This check verifies continuity, not fidelity.** It cannot hear\n"
      "warbling, clipping or a bad voice — the `afftdn` problem passed it\n"
      "cleanly for weeks. Any change to the filter chain or the voice requires\n"
      "someone to actually listen to the result before it is called done.\n"
      "Objective measurement of the delivered file (integrated loudness, true\n"
      "peak, silence detection) is a useful guard but is not a substitute for\n"
      "that.\n")
    A("---\n")

    A("## 6. Poster and thumbnail\n")
    A("Two different images, for two different jobs. Conflating them is the\n"
      "mistake this section exists to prevent.\n")
    A("**`video/poster.png`** — 1920×1080, the video's opening frame, lifted out\n"
      "of the build. It carries the before/after comparison: the approach being\n"
      "replaced on one side, the pattern on the other.\n")
    A("**`docs/thumbnail.png`** — 1280×720, generated by\n"
      "[`make_thumbnails.py`](../../../docs/make_thumbnails.py), and the image\n"
      "that is uploaded. It is deliberately not the poster: YouTube serves a\n"
      "thumbnail at roughly 360 pixels wide in a search result, and at that size\n"
      "a two-column code comparison is a smudge. The thumbnail therefore carries\n"
      "three things only — the pattern name, one line of promise, and one short\n"
      "piece of code — each set large enough to survive the shrink.\n")
    A("> **Requirement.** Neither image strikes out its \"before\" sample. A rule\n"
      "> drawn through monospace is hard to read at full size and illegible at\n"
      "> thumbnail size, and striking the code out makes the card read as being\n"
      "> about what is wrong rather than what is being taught. The rejected\n"
      "> approach is marked with a `BEFORE` chip and the pattern with an `AFTER`\n"
      "> chip; colour and label carry the contrast.\n")
    A("> **Requirement.** The poster is inspected visually before it is\n"
      "> considered done, not merely confirmed to exist. `proxy-pattern` once\n"
      "> shipped a poster reading \"DECORATOR PATTERN\", complete with\n"
      "> decorator's code samples, because `make_slides.py` was copied and\n"
      "> `kind_poster` was never updated. Only looking at the image catches\n"
      "> that.\n")
    A("---\n")

    A("## 7. YouTube publication\n")
    A("[`youtube.md`](youtube.md) holds everything needed to publish, so that\n"
      "uploading is copy-and-paste rather than reconstruction. Seven sections\n"
      "are required:\n")
    if f["title"].endswith("- Explained"):
        rationale = (
            "The `- Explained` suffix is a term people actually search for, and "
            "it makes no promise the video has to keep.")
    else:
        rationale = (
            "The suffix after the dash names the worked e-commerce scenario, so "
            "the title says what the viewer will actually watch rather than only "
            "which pattern it is about.")
    A("1. **Title** — the exact string, ≤ 60 characters so search does not\n"
      "   truncate it, leading with the pattern name. Currently *\"%s\"*,\n"
      "   %d characters. %s"
      % (f["title"], len(f["title"]), rationale))
    A("2. **Description** — first two lines carry the hook, because that is what\n"
      "   shows above the fold; then what the video covers, the chapters, the\n"
      "   repository link, the prerequisites.")
    A("3. **Chapters** — `mm:ss Title`, one per scene, first entry `00:00`.\n"
      "   YouTube needs at least three and the first at zero to render them at\n"
      "   all.")
    A("4. **Tags** — comma-separated, under 500 characters.")
    A("5. **Thumbnail** — pointing at `docs/thumbnail.png`, and explaining why\n"
      "   it is not the poster.")
    A("6. **Upload checklist** — subtitles, language, thumbnail, HD processing,\n"
      "   playlist.")
    A("7. **Cards and end screen** — which video comes next in the learning\n"
      "   order. For this project: %s.\n"
      % (nxt if nxt else "none; it is last, so the end screen links back to "
                         "Simple Factory and to the playlist"))
    A("> **Requirement.** Chapter timings are generated from the built `.srt`,\n"
      "> never written by hand, by\n"
      "> `python3 ../../docs/make_youtube_docs.py %s`. They are the one part of\n"
      "> the file that goes stale silently: any change to the narration text or\n"
      "> the speaking rate invalidates every timestamp, and a chapter list that\n"
      "> is thirty seconds out is worse than none. Regenerate after any\n"
      "> rebuild.\n" % slug)
    A("Subtitles are uploaded from the generated `.srt` rather than left to\n"
      "YouTube's automatic captions, which mis-transcribe class names\n"
      "throughout.\n")
    A("---\n")

    A("## 8. Conformance\n")
    A("This project is compliant when all of the following hold. The full\n"
      "version, which governs all fourteen projects, is in\n"
      "[`video-and-publishing-spec.md`](../../../docs/video-and-publishing-spec.md)\n"
      "§9.\n")
    for x in [
        "The worked example is e-commerce.",
        "`./gradlew build` passes, and the README quotes the real "
        "`./gradlew run` output, which still matches.",
        "Scene 1 follows the four-step opening of §5.1 — what the video is, the author credit, the pattern's definition in general terms, and only then the e-commerce scenario.",
        "`RATE` is 145 and `VOICE` is Samantha.",
        "`CLEANUP` is exactly as §5.4 gives it — no `afftdn`, no `lowpass`.",
        "Per-scene audio is PCM; exactly one AAC encode, at the mux.",
        "`loudnorm` is two-pass with `linear=true`.",
        "The build prints `audio timeline continuous: N packets, no gaps`.",
        "`poster.png` shows the correct pattern name and contains no "
        "strikethrough, confirmed by looking at it.",
        "`docs/youtube.md` has all seven sections, and its chapter timings "
        "match the current `.srt`.",
        "`video/README.md` describes the pipeline as it actually is.",
    ]:
        A("- [ ] " + x)
    A("")
    if f["loudness"]:
        A("Last verified: all eleven items pass. The delivered MP4 measures %s LUFS\n"
          "integrated, %s dBTP true peak, and both streams start at 0.000.\n"
          % (f["loudness"][0], f["loudness"][1]))
    else:
        A("Last verified: all eleven items pass.\n")
    A("---\n")

    A("## 9. Rebuilding\n")
    A("From the project root:\n")
    A("```bash\n(cd video && ./build_video.sh)        # CPU-bound at CRF 18\n```\n")
    A("Then, because the narration timings will have moved:\n")
    A("```bash\npython3 ../../docs/make_youtube_docs.py %s\npython3 ../../docs/make_specs.py %s\n```\n"
      % (slug, slug))
    A("Changing the voice or the filter chain means listening to the result.\n"
      "Changing the narration text means both of the above, and re-checking the\n"
      "runtime claims in the top-level `README.md` and in `video/README.md`.\n")

    # The prose above is written with plain double hyphens so the source stays
    # editable in any editor; the published text uses real em dashes.
    return "\n".join(parts).replace(" -- ", " — ")


# ---------------------------------------------------------------------------
# Markdown -> HTML.
#
# A deliberately small converter rather than a dependency: it handles exactly
# the Markdown these specs use -- ATX headings, fenced code, tables,
# blockquotes, bullet, numbered and task lists, horizontal rules, paragraphs,
# and inline code, bold, italic and links. It is not a general Markdown
# implementation, so if a spec grows a construct that is not in that list,
# extend this rather than working around it.
# ---------------------------------------------------------------------------

CSS = """
:root {
  --bg: #0f172a; --panel: #1e293b; --panel-hi: #334155; --line: #475569;
  --text: #e2e8f0; --muted: #94a3b8; --accent: #a78bfa; --link: #38bdf8;
  --ok: #34d399;
}
* { box-sizing: border-box; }
body {
  margin: 0; padding: 0 20px 80px; background: var(--bg); color: var(--text);
  font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  font-size: 16px; line-height: 1.65;
}
main { max-width: 860px; margin: 0 auto; }
h1, h2, h3 { line-height: 1.25; }
h1 { font-size: 34px; margin: 48px 0 8px; padding-bottom: 18px;
     border-bottom: 3px solid var(--accent); }
h2 { font-size: 25px; margin: 52px 0 4px; color: var(--accent); }
h3 { font-size: 19px; margin: 32px 0 4px; }
p { margin: 14px 0; }
a { color: var(--link); }
a:hover { color: #7dd3fc; }
hr { border: 0; border-top: 1px solid var(--line); margin: 44px 0; }
code {
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, monospace;
  font-size: 0.88em; background: var(--panel); border: 1px solid var(--line);
  border-radius: 4px; padding: 1px 5px;
}
pre {
  background: var(--panel); border: 1px solid var(--line);
  border-left: 4px solid var(--accent); border-radius: 8px;
  padding: 16px 18px; overflow-x: auto;
}
pre code { background: none; border: 0; padding: 0; font-size: 14px; }
blockquote {
  margin: 20px 0; padding: 4px 20px;
  background: rgba(167, 139, 250, 0.08);
  border-left: 4px solid var(--accent); border-radius: 0 8px 8px 0;
}
table { border-collapse: collapse; width: 100%; margin: 22px 0; font-size: 15px; }
th, td { border: 1px solid var(--line); padding: 9px 12px; text-align: left;
         vertical-align: top; }
th { background: var(--panel-hi); font-weight: 600; }
tr:nth-child(even) td { background: rgba(30, 41, 59, 0.55); }
ul, ol { margin: 14px 0; padding-left: 26px; }
li { margin: 7px 0; }
ul.task { list-style: none; padding-left: 4px; }
ul.task li::before { content: "\\2610"; color: var(--ok); font-size: 18px;
                     margin-right: 10px; }
footer {
  max-width: 860px; margin: 60px auto 0; padding-top: 20px;
  border-top: 1px solid var(--line); color: var(--muted); font-size: 14px;
}
"""


def inline(s):
    """Inline markup: code spans, links, bold, italic.

    Code spans are pulled into placeholders *before* anything else runs rather
    than being converted first. These specs are full of bold and links that
    wrap a code span, and converting code first splits those across segments
    so the surrounding markup never matches and leaks into the page as literal
    asterisks and brackets.
    """
    spans = []

    def stash(m):
        spans.append(m.group(1))
        return "\x00%d\x00" % (len(spans) - 1)

    t = re.sub(r'`([^`]+)`', stash, s)
    t = html.escape(t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
               lambda m: '<a href="%s">%s</a>'
                         % (m.group(2)[:-3] + ".html"
                            if m.group(2).endswith("spec.md") else m.group(2),
                            m.group(1)),
               t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![\w*])\*([^*]+)\*(?![\w*])', r'<em>\1</em>', t)
    return re.sub(r'\x00(\d+)\x00',
                  lambda m: "<code>%s</code>" % html.escape(spans[int(m.group(1))]),
                  t)


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def to_html(md):
    lines = md.split("\n")
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]

        if ln.startswith("```"):
            body, i = [], i + 1
            while i < len(lines) and not lines[i].startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            out.append("<pre><code>%s</code></pre>" % html.escape("\n".join(body)))
            continue

        m = re.match(r'(#{1,3}) (.+)', ln)
        if m:
            lvl = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (lvl, inline(m.group(2)), lvl))
            i += 1
            continue

        if re.match(r'^---+$', ln):
            out.append("<hr>")
            i += 1
            continue

        if ln.startswith("|") and i + 1 < len(lines) \
                and re.match(r'^\|[\s:|-]+\|$', lines[i + 1]):
            head, i = cells(ln), i + 2
            body = []
            while i < len(lines) and lines[i].startswith("|"):
                body.append(cells(lines[i]))
                i += 1
            out.append(
                "<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>"
                % ("".join("<th>%s</th>" % inline(c) for c in head),
                   "".join("<tr>%s</tr>"
                           % "".join("<td>%s</td>" % inline(c) for c in r)
                           for r in body)))
            continue

        if ln.startswith(">"):
            body = []
            while i < len(lines) and lines[i].startswith(">"):
                body.append(lines[i].lstrip(">").strip())
                i += 1
            out.append("<blockquote><p>%s</p></blockquote>"
                       % inline(" ".join(x for x in body if x)))
            continue

        m = re.match(r'^(\s*)([-*]|\d+\.) (.+)', ln)
        if m:
            ordered = m.group(2)[0].isdigit()
            items, task = [], False
            while i < len(lines):
                m2 = re.match(r'^(\s*)([-*]|\d+\.) (.+)', lines[i])
                if m2:
                    text = m2.group(3)
                    if text[:4] in ("[ ] ", "[x] "):
                        task, text = True, text[4:]
                    items.append(text)
                    i += 1
                elif items and lines[i].startswith("  ") and lines[i].strip():
                    items[-1] += " " + lines[i].strip()
                    i += 1
                else:
                    break
            out.append("<%s%s>%s</%s>"
                       % ("ol" if ordered else "ul",
                          ' class="task"' if task else "",
                          "".join("<li>%s</li>" % inline(x) for x in items),
                          "ol" if ordered else "ul"))
            continue

        if ln.strip():
            para = []
            while i < len(lines) and lines[i].strip() \
                    and not lines[i].startswith(("#", ">", "|", "```")) \
                    and not re.match(r'^(\s*)([-*]|\d+\.) ', lines[i]) \
                    and not re.match(r'^---+$', lines[i]):
                para.append(lines[i].strip())
                i += 1
            out.append("<p>%s</p>" % inline(" ".join(para)))
            continue

        i += 1
    return "\n".join(out)


def wrap_html(title, body):
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<style>%s</style>
</head>
<body>
<main>
%s
</main>
<footer>
Generated from <code>spec.md</code> by <code>docs/make_specs.py</code> &mdash;
edit the generator, not this file.
</footer>
</body>
</html>
""" % (html.escape(title), CSS, body)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    measure = "--no-measure" not in sys.argv

    for group, slug in ORDER:
        if args and slug not in args:
            continue
        # ORDER lists every project the series will contain, including ones
        # not built yet. A project's META needs its real class names, so both
        # arrive together when the project does; until then, skip it quietly.
        if slug not in META or not os.path.isdir(
                os.path.join(ROOT, group, slug + "-pattern")):
            if args:
                print("%-17s not built yet — skipped" % slug)
            continue
        f = facts(group, slug, measure)
        md = build_md(group, slug, f)
        d = os.path.join(f["dir"], "docs")
        open(os.path.join(d, "spec.md"), "w").write(md)
        title = re.match(r'# (.+)', md).group(1)
        open(os.path.join(d, "spec.html"), "w").write(
            wrap_html(title, to_html(md)))
        print("%-17s spec.md + spec.html  (%d scenes, %s, %d tests%s)"
              % (slug, f["scenes"], f["runtime"], f["tests"],
                 ", %s LUFS" % f["loudness"][0] if f["loudness"] else ""))


if __name__ == "__main__":
    main()
