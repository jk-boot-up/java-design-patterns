package com.jk.explore.command;

import java.util.Objects;

/**
 * Adds a quantity of a product to the cart.
 *
 * <p>This is the command whose undo is not trivial, and it is the one worth
 * reading twice. Adding two of something the cart already holds three of
 * leaves five — so undoing it is <em>not</em> "remove that line". It is
 * "put the quantity back to three". The two cases look nothing alike, and
 * which one applies is not known until the moment the command runs.
 *
 * <p>Hence {@link #previousQuantity}, which is captured inside
 * {@link #execute(Cart)} and is the entire reason this class has a field
 * that the constructor does not set.
 */
public final class AddItemCommand implements CartCommand {

    private final String sku;
    private final String name;
    private final Money unitPrice;
    private final int quantity;

    /** Zero when the cart did not have this SKU at all. Set by execute. */
    private int previousQuantity;
    private boolean executed;

    public AddItemCommand(String sku, String name, Money unitPrice, int quantity) {
        this.sku = Objects.requireNonNull(sku, "sku");
        this.name = Objects.requireNonNull(name, "name");
        this.unitPrice = Objects.requireNonNull(unitPrice, "unitPrice");
        if (quantity < 1) {
            throw new IllegalArgumentException("cannot add " + quantity + " of " + sku);
        }
        this.quantity = quantity;
    }

    @Override
    public String describe() {
        return "add " + quantity + " x " + sku;
    }

    @Override
    public void execute(Cart cart) {
        previousQuantity = cart.quantityOf(sku);
        cart.putLine(new CartLine(sku, name, unitPrice, previousQuantity + quantity));
        executed = true;
    }

    @Override
    public void undo(Cart cart) {
        if (!executed) {
            throw new IllegalStateException("cannot undo a command that has not run: " + describe());
        }
        if (previousQuantity == 0) {
            cart.removeLine(sku);
        } else {
            cart.putLine(new CartLine(sku, name, unitPrice, previousQuantity));
        }
    }
}
