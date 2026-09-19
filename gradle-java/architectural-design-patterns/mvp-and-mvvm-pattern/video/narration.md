# MVP and MVVM Pattern — Video Narration Script

## 1. MVP and MVVM

Hello, and welcome. This video explains the MVP and MVVM pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: M V P and M V V M both take the rules out of the screen. In M V P, a presenter tells a passive view what to show. In M V V M, the view binds to state that a view model keeps up to date. This is another project in the architecture category, whose subject is how a whole application is arranged, and who may depend on whom. In our online store, the cart screen shows a total, a count and a checkout button, and the rules for them are tangled into the screen. By the end you will see a screen whose rules cannot be checked without opening a window, see a presenter tell a passive view, see the view make no decisions, see a view bind to state, see two screens share one view model, and see the bill, which is a long interface on one side and hidden wiring on the other.

## 2. The Scenario

Here is the scenario. The cart screen shows a total, an item count, and a checkout button. The button is on only when the cart is not empty. The question: where do these rules live?

## 3. The Screen Decides

First, the screen decides. To check the total and the checkout rule, a screen was needed. One window was opened. The rules are welded to the widgets.

## 4. The Pattern

The pattern. Keep the rules out of the screen. In M V P, a presenter tells a passive view what to show. In M V V M, a view model keeps state, and the view binds to it.

## 5. A Presenter Tells A Passive View

Second, M V P: a presenter tells a passive view. After two adds, the view was told: show the total, twenty five pounds fifty; show the count, two; enable checkout. Windows opened: none. The rules were checked with no screen.

## 6. The View Makes No Decisions

Third, the view makes no decisions. An empty cart: total zero, count zero, checkout off. Add one item and remove it, and the last three calls are the same. The presenter decides that checkout is off again. The view just obeys.

## 7. The View Binds To State

Fourth, M V V M: the view binds to state. The screen starts as zero, no items, checkout off. After two adds it shows twenty five pounds fifty, two items, checkout on. Nobody told the screen. It bound once. The view model holds no reference to any view.

## 8. Many Views, One View Model

Fifth, many views, one view model. A phone screen and a watch screen bind to the same view model. Both show sixteen pounds, one item, checkout on. A second screen cost no change to the view model.

## 9. The Bill

Last, the bill. In M V V M, a screen that forgot to bind the total draws a question mark. Nothing failed. It is just wrong. In M V P, the view interface has three methods, and each new thing on the screen adds one to the interface, the presenter, and every view. M V V M hides the wiring in the binding. M V P spells it out, and gets long.

## 10. How To Recognise It

How do you recognise this in code you did not write? A Presenter that holds a View interface. A ViewModel with observable properties, LiveData, StateFlow or ObservableField. Data binding in WPF, Android, SwiftUI or Angular. A View implemented by a test double.

## 11. The Verdict

Here is my verdict, plainly. Take the rules out of the screen either way. Use MVP when you want every step visible and easy to check with a fake view. Use MVVM when your platform has good binding, and several screens share one state. Test the presenter or the view model with no screen, and check the bindings too.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? For a static page, or a screen with two fields, the extra layer is more than the problem. Keep it for screens with rules that you want to check on their own.

## 14. Thanks for Watching

That's MVP and MVVM. If you take one sentence away, take this one: M V P and M V V M keep the rules out of the screen, and the price is a longer interface on one side, and hidden wiring on the other. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add a warning line that shows when the total is over five hundred pounds, first in the presenter, then in the view model. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
