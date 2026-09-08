package com.jk.explore.command;

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Objects;

/**
 * The trap, kept for contrast: edit the cart directly, and push a note of
 * "what I just changed" onto a stack so it can be reversed later.
 *
 * <p>This is what undo looks like before anybody reifies the request, and
 * it is worth being fair to it: for a cart that only ever gains new lines,
 * it is correct and it is a third of the code. It falls apart on the cases
 * where the edit's effect depends on what was already there.
 *
 * <p>Two bugs are baked in on purpose, and both are the same mistake:
 * the note records <em>what was asked for</em> rather than <em>what the
 * cart looked like beforehand</em>.
 *
 * <ul>
 *   <li>Adding 2 of a SKU the cart already had 3 of, then undoing, deletes
 *   the line — losing the 3 the customer had chosen earlier.</li>
 *   <li>Applying a coupon over an existing one, then undoing, leaves the
 *   cart with no coupon at all rather than the original.</li>
 * </ul>
 *
 * <p>Both are fixable here, of course — with more fields on the note, and a
 * longer {@code switch}, once for every kind of edit that exists. That
 * growth is the actual complaint.
 */
public final class NaiveCartEditor {

    /** An ad-hoc note of one edit. A new kind of edit means new fields here. */
    private record Change(String kind, String sku, int quantity) { }

    private final Cart cart;
    private final Deque<Change> changes = new ArrayDeque<>();

    public NaiveCartEditor(Cart cart) {
        this.cart = Objects.requireNonNull(cart, "cart");
    }

    public void addItem(String sku, String name, Money unitPrice, int quantity) {
        cart.putLine(new CartLine(sku, name, unitPrice, cart.quantityOf(sku) + quantity));
        changes.push(new Change("add", sku, quantity));
    }

    public void applyCoupon(Coupon coupon) {
        cart.setCoupon(coupon);
        changes.push(new Change("coupon", coupon.code(), 0));
    }

    /** Reverses the last edit — as far as the note it kept allows. */
    public boolean undo() {
        if (changes.isEmpty()) {
            return false;
        }
        Change change = changes.pop();
        switch (change.kind()) {
            case "add" -> cart.removeLine(change.sku());   // wrong if the line already existed
            case "coupon" -> cart.setCoupon(null);         // wrong if a coupon was replaced
            default -> throw new IllegalStateException("no idea how to undo " + change.kind());
        }
        return true;
    }

    public int pendingUndos() {
        return changes.size();
    }
}
