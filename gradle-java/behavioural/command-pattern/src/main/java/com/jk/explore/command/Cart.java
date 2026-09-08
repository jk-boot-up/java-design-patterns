package com.jk.explore.command;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

/**
 * The receiver: a shopping cart, and every edit that can be made to one.
 *
 * <p>This class knows nothing about commands, undo, or history. It offers
 * the smallest set of operations that can express a cart edit, and every
 * one of them is reversible <em>by some other operation on this same
 * class</em> — which is the property the commands rely on and the reason
 * they can be written without reaching inside.
 *
 * <p>Insertion order is preserved, because a cart that reshuffles itself
 * when a line is edited looks broken to the customer, and because an undone
 * removal has to put the line back where it was.
 */
public final class Cart {

    private final Map<String, CartLine> lines = new LinkedHashMap<>();
    private Coupon coupon;

    /** The lines, in the order they were first added. */
    public List<CartLine> lines() {
        return List.copyOf(lines.values());
    }

    /** The line for a SKU, if the cart has one. */
    public Optional<CartLine> line(String sku) {
        return Optional.ofNullable(lines.get(Objects.requireNonNull(sku, "sku")));
    }

    /** How many of a SKU are in the cart; zero if it is not there at all. */
    public int quantityOf(String sku) {
        return line(sku).map(CartLine::quantity).orElse(0);
    }

    public boolean contains(String sku) {
        return lines.containsKey(Objects.requireNonNull(sku, "sku"));
    }

    public int lineCount() {
        return lines.size();
    }

    /**
     * Puts a line in the cart, replacing any line for the same SKU.
     *
     * <p>Replacing rather than merging is deliberate: merging would make
     * this operation depend on what was already there, and a command that
     * has recorded the previous quantity could no longer restore it by
     * calling one method.
     */
    public void putLine(CartLine line) {
        lines.put(Objects.requireNonNull(line, "line").sku(), line);
    }

    /**
     * Puts a line back at a known position, used only by undo.
     *
     * <p>Removing the second of five lines and re-adding it leaves it fifth,
     * which is not what "undo" means to the person looking at the screen.
     */
    public void insertLineAt(int index, CartLine line) {
        Objects.requireNonNull(line, "line");
        if (index < 0 || index > lines.size()) {
            throw new IndexOutOfBoundsException(
                    "no such position in a cart of " + lines.size() + " lines: " + index);
        }
        List<CartLine> rest = new ArrayList<>(lines.values());
        rest.add(index, line);
        lines.clear();
        for (CartLine each : rest) {
            lines.put(each.sku(), each);
        }
    }

    /** Where a SKU sits in the cart, or -1 if it is not there. */
    public int positionOf(String sku) {
        Objects.requireNonNull(sku, "sku");
        int i = 0;
        for (String each : lines.keySet()) {
            if (each.equals(sku)) {
                return i;
            }
            i++;
        }
        return -1;
    }

    /** Takes a line out entirely. Returns it, so a caller can put it back. */
    public Optional<CartLine> removeLine(String sku) {
        return Optional.ofNullable(lines.remove(Objects.requireNonNull(sku, "sku")));
    }

    /** The coupon currently on the cart, if any. */
    public Optional<Coupon> coupon() {
        return Optional.ofNullable(coupon);
    }

    /** Sets the coupon, or clears it when given {@code null}. At most one applies. */
    public void setCoupon(Coupon coupon) {
        this.coupon = coupon;
    }

    /** The total before any discount. */
    public Money subtotal() {
        Money total = Money.zero();
        for (CartLine line : lines.values()) {
            total = total.plus(line.lineTotal());
        }
        return total;
    }

    /** What the coupon takes off, or zero when there is no coupon. */
    public Money discount() {
        return coupon == null ? Money.zero() : coupon.discountOn(subtotal());
    }

    /** What the customer pays. */
    public Money total() {
        return subtotal().minus(discount());
    }

    /** A receipt-style dump, used by the demo and by nothing else. */
    public String describe() {
        StringBuilder out = new StringBuilder();
        for (CartLine line : lines.values()) {
            out.append("    ").append(line).append('\n');
        }
        if (lines.isEmpty()) {
            out.append("    (empty)\n");
        }
        out.append(String.format("    %-36s %19s%n", "subtotal", subtotal()));
        if (coupon != null) {
            out.append(String.format("    %-36s %19s%n", coupon, "-" + discount()));
        }
        out.append(String.format("    %-36s %19s%n", "total", total()));
        return out.toString();
    }
}
