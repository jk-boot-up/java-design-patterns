package com.jk.explore.memento;

/**
 * One line of a shopping basket: a product, its price, and how many.
 *
 * <p>This is a record, so it cannot be changed after it is created. That
 * matters more than it looks. A snapshot of the basket copies the list of
 * lines, and copying a list only protects you if the things inside it cannot
 * be edited behind your back. Immutable lines are what make a shallow copy
 * safe here.
 */
public record BasketLine(String product, int pounds, int quantity) {

    public int lineTotal() {
        return pounds * quantity;
    }

    @Override
    public String toString() {
        return quantity + " x " + product + "  £" + lineTotal();
    }
}
