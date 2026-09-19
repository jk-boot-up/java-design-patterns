# MVP and MVVM, Explained

## The pattern in one sentence

MVP and MVVM both take the rules out of the screen. In MVP a presenter tells a passive view what to show. In MVVM the view binds to state that a view model keeps up to date.

## The six acts

### The Screen Decides

To check the total and the checkout rule, a screen was needed. One window was opened. The rules are welded to the widgets.

```
  to check the total and the checkout rule, a screen was needed. windows opened: 1.
  total label: £16.00, checkout enabled: true. the rules are welded to the widgets.
```

### A Presenter Tells A Passive View

After two adds, the view was told: show the total, twenty five pounds fifty; show the count, two; enable checkout. Windows opened: none. The rules were checked with no screen.

```
  after two adds the view was told: [showTotal £25.50, showCount 2, enableCheckout true].
  windows opened: 0. the rules were checked with no screen.
```

### The View Makes No Decisions

An empty cart: total zero, count zero, checkout off. Add one item and remove it, and the last three calls are the same. The presenter decides that checkout is off again. The view just obeys.

```
  an empty cart: [showTotal £0.00, showCount 0, enableCheckout false].
  add then remove: the last three calls were [showTotal £0.00, showCount 0, enableCheckout false].
  the presenter decides checkout is off again. the view just obeys.
```

### The View Binds To State

The screen starts as zero, no items, checkout off. After two adds it shows twenty five pounds fifty, two items, checkout on. Nobody told the screen. It bound once. The view model holds no reference to any view.

```
  drawn at the start: £0.00 | 0 items | checkout off.
  after two adds: £25.50 | 2 items | checkout on.
  nobody told the screen. it bound once. the view model holds no reference to any view.
```

### Many Views, One View Model

A phone screen and a watch screen bind to the same view model. Both show sixteen pounds, one item, checkout on. A second screen cost no change to the view model.

```
  phone: £16.00 | 1 items | checkout on.
  watch: £16.00 | 1 items | checkout on.
  a second screen cost no change to the view model.
```

### The Bill

In M V V M, a screen that forgot to bind the total draws a question mark. Nothing failed. It is just wrong. In M V P, the view interface has three methods, and each new thing on the screen adds one to the interface, the presenter and every view. M V V M hides the wiring in the binding. M V P spells it out, and gets long.

```
  MVVM: a screen that forgot to bind the total draws: ? | 1 items | checkout on. nothing failed. it is just wrong.
  MVP: the view interface has 3 methods. each new thing on the screen adds one to the interface, the presenter and every view.
  MVVM hides the wiring in the binding. MVP spells it out, and gets long.
```

## The verdict

Take the rules out of the screen either way. Use MVP when you want every step visible and easy to check with a fake view. Use MVVM when your platform has good binding, and several screens share one state. Test the presenter or the view model with no screen, and check the bindings too.

## How to recognise this in code you did not write

- A `Presenter` that holds a `View` interface.
- A `ViewModel` with observable properties, `LiveData`, `StateFlow` or `ObservableField`.
- Data binding in WPF, Android, SwiftUI or Angular.
- A `View` implemented by a test double.

## Where you have already met this

Android apps with ViewModel and Jetpack, WPF and .NET MAUI, SwiftUI's observable objects, and Angular and Vue with their reactive state.

## When this is too much

For a static page, or a screen with two fields, the extra layer is more than the problem. Keep it for screens with rules that you want to check on their own.
