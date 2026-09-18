# MVC, Explained

## The pattern in one sentence

Split a screen into three roles — a **Model** that owns state and
computation, a **View** that only renders, and a **Controller** that turns
input into calls on the model — so that anything reading the model sees the
same numbers, because none of them is allowed to compute its own.

## The three roles, and what each one is not allowed to know

| Role | Class | Job | Must not know |
| --- | --- | --- | --- |
| Model | `OrderSummaryModel` | Holds the placed order's lines and its **one** total | How it will be displayed |
| View | `ScreenSummaryView`, `EmailConfirmationView` | Turn a model into text | How the total was calculated, or where the order came from |
| Controller | `OrderSummaryController` | Place the order, build the model, hand it to whichever views are asked for | Nothing about formatting — it never builds a string |

`OrderSummaryView` accepts exactly one thing: a finished `OrderSummaryModel`.
That narrowness is the whole mechanism. A view that could be handed a
`Product` or a raw price could multiply one — and the moment it can, two
views can disagree, which is exactly what `RoundedEmailView` demonstrates in
this project's naive package.

## Classic MVC, and the web MVC you have actually used

**Say this plainly, because almost nobody means the same thing by "MVC".**

Classic Smalltalk MVC has the **view observe the model directly** — the
model changes, and every subscribed view redraws itself without being told
to by name. This project simplifies that for a synchronous console demo:
the controller builds the model once and hands it to the views it was asked
to render, rather than the views independently subscribing and pulling. The
principle that survives the simplification is the one that matters: **the
view never fetches anything itself, and never sees anything but the finished
model.**

**Web MVC — the Spring, Rails or Django kind almost everyone meets first —
does not have this observation at all.** A controller method assembles a
model (often literally a map of key-value pairs) and hands it to a template
engine, which renders once and is done. There is no ongoing subscription,
no redraw, because a web response is sent once and the page is gone. If you
have written a Spring `@Controller` method that returns a view name and adds
attributes to a `Model` parameter, you have already used this half of the
idea — you were just never shown the Smalltalk half it is named after.

## MVP and MVVM, in one scene

Both are the same separation with the arrows redrawn. **MVP** (Model-View-
Presenter) makes the view fully passive — it has no reference to the model
at all, and a Presenter pulls data from the model and pushes it into the
view through an interface, which makes the view trivial to fake in a test.
**MVVM** (Model-View-ViewModel) goes further and has the view **bind** to a
ViewModel's properties, so that a ViewModel change updates the screen with
no explicit push at all — the mechanism most modern UI frameworks (data
binding, reactive streams) actually use under a different name. Teaching
either properly needs a UI toolkit with real data binding, which this
console-based course does not have; the distinction worth keeping is that
MVC's view can read its model directly, MVP's cannot, and MVVM's binds to
it automatically.

## The rule, written where a build can read it

```java
ArchRule rule = noClasses()
    .that().resideInAPackage(VIEW)
    .should().dependOnClassesThat()
        .resideInAPackage(INFRASTRUCTURE)
    .because(
        "a view that reads the catalogue or storage "
      + "directly can compute a number the model "
      + "never agreed to");

rule.check(layers);
```

`ArchitectureRuleCatchesTheShortcutTest` widens the same rule to the `naive`
package and asserts the failure names `RoundedEmailView` and the class it
reached for, `ProductTable`.

## The forced change, performed and counted

**Before:** one view, `ScreenSummaryView`, reading `OrderSummaryModel`.
**After:** a second view, `EmailConfirmationView`, added — reading the same
model, computing nothing.

```
files added     : 1   view/EmailConfirmationView.java
files modified  : 1   PlaceAnOrderDemo.java (the composition root)
lines changed   : 2
classes across model + controller + views : 21
of those, opened                          : 1
of those, never opened                    : 20
```

Twenty classes never opened, and — the point a file count alone cannot make
— the new view's total is *guaranteed* to match the old one's, not merely
observed to. `EmailConfirmationView.render` contains no arithmetic operator
anywhere in it.

## The bill

**A narrow view interface is a real constraint.** A view that legitimately
needs something the model does not expose has exactly one honest option:
widen the model, for everyone, rather than reach around it. That discipline
has to be enforced by habit as much as by the architecture test, because the
test only catches a view importing `infrastructure` — it cannot catch a
model growing fifteen getters nobody uses because one view once needed a
sixteenth.

**A synchronous console demo is not classic MVC's hardest case.** Real UI
frameworks earn their complexity keeping several views in sync as a model
changes *while the program is running* — a cart total updating on screen the
instant an item is added, with nobody polling. This project's controller
builds the model once per checkout, which sidesteps that entirely. The
written notes say so rather than claim more than the code shows.

**Controllers grow.** The single most common failure mode of MVC in
production is a controller that starts routing input and ends up containing
business rules, because "just one more check" is always easier to add to
the method already handling the request than to find its proper home. This
project's controller is three calls long on purpose, and staying that short
is a discipline, not a guarantee the pattern provides for free.

## When this is too much

A Model/View/Controller split earns its keep the moment more than one
output has to represent the same state — a screen and an email, a screen
and a PDF receipt, a desktop app and a CLI. It is not worth it for a program
with exactly one output that is never going to grow a second, where a single
method that computes and prints in one pass is not a shortcut, it is the
whole of what is needed.

## Comparison with the naive versions

| | No separation | Two views, one computing its own total | Two views, one model |
| --- | --- | --- | --- |
| Can the screen be tested without a checkout? | No | Yes | Yes |
| Can a second view disagree with the first? | N/A — one method | Yes, silently | No — neither can compute anything |
| What tells you a view reached into storage | Nobody | Nobody | `ArchitectureTest`, by name, in seconds |
