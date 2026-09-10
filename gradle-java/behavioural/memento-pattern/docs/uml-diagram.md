# Memento Pattern — UML Sequence Diagram

Shows the runtime interaction behind one undo. The shopper has three products
and a voucher, removes the laptop stand by mistake, and presses undo. Follow
how little the history knows: it asks for a snapshot, keeps it, and later hands
the same object back.

![Memento pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    actor Shopper
    participant UI as BasketUndoDemo
    participant History as BasketHistory
    participant Basket
    participant Snap as BasketSnapshot

    Note over Shopper,Snap: state: 4 items, voucher SAVE5, total £65

    Shopper->>UI: remove the laptop stand
    UI->>History: record(basket, "removed the laptop stand")
    activate History
    History->>Basket: save("removed the laptop stand")
    activate Basket
    Basket->>Snap: new(lines, voucher, label)
    Note right of Snap: List.copyOf — a copy,<br/>not a reference to the live list
    Snap-->>Basket: snapshot
    Basket-->>History: snapshot
    deactivate Basket
    Note over History: pushed onto the stack.<br/>It never looks inside.
    deactivate History

    UI->>Basket: remove("Laptop stand")
    Note over Basket: 3 items, £31.<br/>The snapshot is untouched by this.

    Shopper->>UI: press undo
    UI->>History: undo(basket)
    activate History
    History->>Basket: restore(snapshot)
    activate Basket
    Basket->>Snap: lines()
    Snap-->>Basket: the copied lines
    Basket->>Snap: voucher()
    Snap-->>Basket: "SAVE5"
    Note over Basket: lines and voucher both put back
    deactivate Basket
    History-->>UI: "removed the laptop stand"
    deactivate History

    Note over Shopper,Snap: state: 4 items, voucher SAVE5, total £65
```

</details>

## Notes

- **The history never opens a snapshot.** Every arrow into `BasketSnapshot`
  comes from `Basket`. The caretaker's whole job fits in "hold this, and give
  it back later", and it manages that without knowing what a basket contains.
- **The copy happens at the moment of saving**, in the snapshot's constructor.
  Everything the shopper does afterwards happens to the live list, and cannot
  reach the copy. That single `List.copyOf` is the difference between undo
  working and undo emptying the basket.
- **`restore` puts back both fields.** Lines and voucher travel together,
  because they are both state and the pattern's rule is that a snapshot is
  complete. The naive version restores one of them and silently forgets the
  other.
- **The snapshot is not consumed by being restored.** `restore` reads from it
  and leaves it as it was, so the same snapshot could be restored twice — which
  is what makes redo, or a branching history, possible later without changing
  any of these three classes.
- **The label goes in at save time, not at undo time.** That is what lets a
  history list say "undo: removed the laptop stand" while still being unable to
  read a single thing about the basket itself.
- Compare with `NaiveBasket`: the same shopper does the same three things, but
  there is no snapshot participant at all. `save()` writes down where the live
  list is, so the "before" and "after" states are the same object, and by the
  time undo runs there is nothing left to restore from.
