# Mediator Pattern — UML Sequence Diagram

Shows the runtime interaction behind one click. The shopper has a UK order
with Express shipping and gift wrap ticked, and changes the delivery country
to the United States. Follow how far the widget's own involvement goes: it
records the new country, says so, and stops.

![Mediator pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    actor Shopper
    participant Country as CountrySelector
    participant Form as CheckoutForm
    participant Ship as ShippingSelector
    participant Wrap as GiftWrapCheckbox
    participant Total as TotalLabel
    participant Button as PlaceOrderButton

    Note over Shopper,Button: state: UK, Express, gift wrapped, £48, button enabled

    Shopper->>Country: select("US")
    activate Country
    Note right of Country: stores "US" — and that is all it does
    Country->>Form: changed(this)
    deactivate Country

    activate Form
    Note over Form: the country changed, so the form is reshaped

    Form->>Ship: showOptions(["International"])
    Note right of Ship: options replaced, chosen cleared to ""

    Form->>Wrap: setAvailable(false)
    Note right of Wrap: withdrawn AND unticked, in one call

    Form->>Ship: chosen()
    Ship-->>Form: ""
    Form->>Wrap: isTicked()
    Wrap-->>Form: false
    Form->>Total: show(40)

    Form->>Country: country()
    Country-->>Form: "US"
    Form->>Ship: chosen()
    Ship-->>Form: ""
    Form->>Button: setEnabled(false)
    deactivate Form

    Note over Shopper,Button: state: US, no courier, no wrap, £40, button disabled

    Shopper->>Ship: select("International")
    activate Ship
    Ship->>Form: changed(this)
    deactivate Ship
    activate Form
    Note over Form: not the country, so no reshaping — price and button only
    Form->>Total: show(52)
    Form->>Button: setEnabled(true)
    deactivate Form
```

</details>

## Notes

- **Every arrow into `CheckoutForm` is `changed`.** There is one inbound
  message in the whole diagram, sent by whichever widget the shopper touched.
  Widgets do not have a vocabulary for talking to the form beyond "something
  about me is different now".
- **Every arrow out of `CheckoutForm` is the form pushing state down.** No
  widget calls another. Draw a line down the middle of the diagram and every
  message crosses it.
- **The two branches of `changed` are visible as two shapes.** The country
  change reshapes the form and then reprices it; the shipping change only
  reprices it. That difference is the single `if` in `changed`, and it is the
  only branching in the pattern.
- **`setAvailable(false)` does two things in one message**, and that is the
  fix for the tangled version's first bug. Withdrawing the offer and clearing
  the tick cannot be separated, because there is only one call that does
  either.
- **The button is re-checked after every change, unconditionally.** Nothing
  decides whether it *needs* re-checking. That is what stops the second bug:
  the mediator does not have to notice that clearing the shipping method
  affects the button, because it re-asks the question every time regardless.
- Compare with `NaiveCheckoutForm`: the same messages arrive at the same
  widgets, but they originate from `NaiveCountry`, so the diagram has no
  centre. Each new widget adds arrows to and from every widget it touches,
  and the picture stops being readable at about six participants — which is
  roughly where a real checkout form starts.
