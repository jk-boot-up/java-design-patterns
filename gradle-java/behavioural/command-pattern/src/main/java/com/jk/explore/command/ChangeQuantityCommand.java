package com.jk.explore.command;

import java.util.Objects;

/**
 * Sets the quantity of a line the cart already holds.
 *
 * <p>The simplest of the four to reverse — put the old number back — and it
 * is here to make the point that the interesting part of a command is never
 * {@code execute}. It is what {@code execute} has to remember.
 *
 * <p>Setting a quantity of zero is refused rather than quietly treated as a
 * removal. Two edits that undo differently should be two commands, and a
 * history full of "change quantity" entries that sometimes removed a line
 * is a history nobody can read.
 */
public final class ChangeQuantityCommand implements CartCommand {

    private final String sku;
    private final int newQuantity;

    private int previousQuantity;

    public ChangeQuantityCommand(String sku, int newQuantity) {
        this.sku = Objects.requireNonNull(sku, "sku");
        if (newQuantity < 1) {
            throw new IllegalArgumentException(
                    "quantity must be at least 1; to take the line out, use RemoveItemCommand");
        }
        this.newQuantity = newQuantity;
    }

    @Override
    public String describe() {
        return "set " + sku + " to " + newQuantity;
    }

    @Override
    public void execute(Cart cart) {
        CartLine line = cart.line(sku).orElseThrow(() -> new IllegalStateException(
                "cannot change the quantity of " + sku + ": it is not in the cart"));
        previousQuantity = line.quantity();
        cart.putLine(line.withQuantity(newQuantity));
    }

    @Override
    public void undo(Cart cart) {
        if (previousQuantity == 0) {
            throw new IllegalStateException("cannot undo a command that has not run: " + describe());
        }
        CartLine line = cart.line(sku).orElseThrow(() -> new IllegalStateException(
                "cannot undo " + describe() + ": " + sku + " is no longer in the cart"));
        cart.putLine(line.withQuantity(previousQuantity));
    }
}
