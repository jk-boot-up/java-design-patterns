# MVP and MVVM Pattern — Video Narration Script

## 1. MVP and MVVM

Hello, and welcome. This video explains the M V P and M V V M patterns, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Both patterns take the rules out of the screen. In M V P, which stands for Model, View, Presenter, a presenter tells a passive screen exactly what to show. In M V V M, which stands for Model, View, View Model, the screen connects itself to some state, and updates whenever that state changes. Think of a stage play. In M V P, a director stands in the wings and tells each actor every move. In M V V M, the actors watch a scoreboard, and react to it by themselves. In our online store, the cart screen shows a total, an item count, and a checkout button. Right now, the rules for those are tangled into the screen. In this video, we untangle them both ways, and then compare the costs.

## 2. The Scenario

Here is the scenario. The cart screen shows three things. The total price. The number of items. And a checkout button. The checkout button is switched on only when the cart is not empty. So here is the question. Where should these rules live?

## 3. The Screen Decides

First, the old way: the screen decides everything. To check the total, and the checkout rule, we had to create a real screen. One window was opened, just to run a test. The rules are welded to the screen's buttons and labels.

## 4. The Pattern

Now, the pattern. Keep the rules out of the screen. In M V P, a presenter holds the rules. It tells a passive screen what to show. In M V V M, a view model holds the rules and the state. The screen connects to that state once, and follows it from then on. This connecting is called binding.

## 5. A Presenter Tells A Passive View

Second demo: M V P, where a presenter tells a passive screen. We add two items to the cart. The presenter then gives the screen three instructions. Show the total, twenty-five pounds fifty. Show the count, two. And switch the checkout button on. How many windows were opened? None. The rules were checked with no screen at all, using a fake view.

## 6. The View Makes No Decisions

Third demo: the screen makes no decisions. With an empty cart, the presenter says: total zero, count zero, checkout off. Now add one item, then remove it again. The presenter's last three instructions are exactly the same. The presenter decided that checkout is off again. The screen just obeys.

## 7. The View Binds To State

Fourth demo: M V V M, where the screen binds to state. The screen starts by showing zero, no items, and checkout off. We add two items. The screen now shows twenty-five pounds fifty, two items, and checkout on. Nobody told the screen to update. It bound to the view model once, at the start. And the view model holds no reference to any screen at all.

## 8. Many Views, One View Model

Fifth demo: many screens, one view model. A phone screen and a watch screen both bind to the same view model. Both show sixteen pounds, one item, and checkout on. Adding that second screen needed no change to the view model at all.

## 9. The Bill

Finally, the costs of each. In M V V M, imagine a screen that forgot to bind the total. It shows a question mark. Nothing fails, and no error appears. It is simply wrong. In M V P, the screen's interface has three methods. Every new item on the screen adds another method, to the interface, the presenter, and every screen. So M V V M hides the wiring inside the binding. And M V P spells every step out, and grows long.

## 10. How To Recognise It

How can you spot these patterns in code someone else wrote? For M V P, look for a presenter that holds a view interface. And a view implemented by a fake, in tests. For M V V M, look for a view model with observable properties. Names like Live Data, State Flow, or Observable Field. And data binding in frameworks like W P F, Android, Swift U I, or Angular.

## 11. The Verdict

So, here is the verdict. Either way, take the rules out of the screen. Choose M V P when you want every step visible, and easy to check with a fake screen. Choose M V V M when your platform has good binding, and several screens share one state. And in both cases, test the presenter or the view model with no screen. Then check the bindings too.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every number you heard comes from the program's own output. And nothing depends on the clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? For a static page, or a screen with just two fields, the extra layer is bigger than the problem. Keep it for screens with rules that you want to check on their own.

## 14. Thanks for Watching

That's M V P and M V V M. If you remember one sentence, make it this one. Both keep the rules out of the screen, and the price is a longer interface on one side, and hidden wiring on the other. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add a warning that appears when the total is over five hundred pounds. Build it first in the presenter, and then in the view model. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
