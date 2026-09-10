package com.jk.explore.memento;

import java.util.ArrayList;
import java.util.List;

/**
 * The shopper's basket — the originator.
 *
 * <p>It has two pieces of state: the lines in it, and the voucher code that
 * has been applied. The pattern's rule is that <em>both</em> of them go into a
 * snapshot and <em>both</em> of them come back out, and that the basket is the
 * only class that knows that, because it is the only class that knows what its
 * own state is. Add a third field tomorrow and there is exactly one pair of
 * methods to update.
 */
public class Basket {

    private static final int VOUCHER_POUNDS = 5;

    private final List<BasketLine> lines = new ArrayList<>();
    private String voucher = "";

    public void add(String product, int pounds, int quantity) {
        lines.add(new BasketLine(product, pounds, quantity));
    }

    /** Removes the first line for that product. Does nothing if it is not there. */
    public void remove(String product) {
        lines.removeIf(line -> line.product().equals(product));
    }

    public void applyVoucher(String code) {
        this.voucher = code;
    }

    public String voucher() {
        return voucher;
    }

    public List<BasketLine> lines() {
        return List.copyOf(lines);
    }

    public int itemCount() {
        return lines.stream().mapToInt(BasketLine::quantity).sum();
    }

    public int total() {
        int goods = lines.stream().mapToInt(BasketLine::lineTotal).sum();
        int discount = voucher.isEmpty() ? 0 : Math.min(VOUCHER_POUNDS, goods);
        return goods - discount;
    }

    /**
     * Takes a snapshot of everything this basket currently is.
     *
     * <p>{@code label} says what the shopper is about to do, so a history list
     * can describe the undo without ever looking inside the snapshot.
     */
    public BasketSnapshot save(String label) {
        return new BasketSnapshot(lines, voucher, label);
    }

    /**
     * Puts this basket back exactly as the snapshot found it.
     *
     * <p>The snapshot is not consumed or emptied by this, so the same one can
     * be restored twice, and a caretaker is free to keep it.
     */
    public void restore(BasketSnapshot snapshot) {
        lines.clear();
        lines.addAll(snapshot.lines());
        this.voucher = snapshot.voucher();
    }

    public String describe() {
        StringBuilder sb = new StringBuilder();
        for (BasketLine line : lines) {
            sb.append("    ").append(line).append('\n');
        }
        sb.append("    voucher: ").append(voucher.isEmpty() ? "(none)" : voucher).append('\n');
        sb.append("    total: £").append(total());
        return sb.toString();
    }
}
