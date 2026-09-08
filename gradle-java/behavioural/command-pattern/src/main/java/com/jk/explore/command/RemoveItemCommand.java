package com.jk.explore.command;

import java.util.Objects;

/**
 * Takes a whole line out of the cart.
 *
 * <p>Undo has to restore two things, and the second one is the one people
 * forget: the line itself, <em>and where it was</em>. Removing the second
 * of five lines and undoing it by adding the line back leaves it fifth,
 * which is not what undo means to the customer looking at the screen.
 */
public final class RemoveItemCommand implements CartCommand {

    private final String sku;

    private CartLine removed;
    private int position;

    public RemoveItemCommand(String sku) {
        this.sku = Objects.requireNonNull(sku, "sku");
    }

    @Override
    public String describe() {
        return "remove " + sku;
    }

    @Override
    public void execute(Cart cart) {
        position = cart.positionOf(sku);
        removed = cart.removeLine(sku).orElseThrow(() -> new IllegalStateException(
                "cannot remove " + sku + ": it is not in the cart"));
    }

    @Override
    public void undo(Cart cart) {
        if (removed == null) {
            throw new IllegalStateException("cannot undo a command that has not run: " + describe());
        }
        cart.insertLineAt(position, removed);
    }
}
