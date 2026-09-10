package com.jk.explore.memento;

import java.util.ArrayList;
import java.util.List;

/**
 * The trap: undo written without a snapshot, the way it usually gets written
 * the first time.
 *
 * <p>It looks right. There is a save, there is an undo, and if you read them
 * side by side they appear to be opposites. Two things are wrong with them,
 * and neither one throws.
 *
 * <p>The first is on the {@code savedLines = lines} line. That does not copy
 * anything. It writes down where the list is, not what is in it, so the
 * "saved" list and the live list are the same list — every later add and
 * remove edits the save as well. And then {@code undo()} clears the live list,
 * which is also the saved list, and copies the now-empty saved list back over
 * it. The shopper clicks undo and their basket is empty.
 *
 * <p>The second is quieter still: the voucher is not saved at all. Nobody
 * decided not to save it. It simply was not on anyone's mind on the day undo
 * was written, and there is no line of code you could review to find that out.
 */
public class NaiveBasket {

    private static final int VOUCHER_POUNDS = 5;

    private final List<BasketLine> lines = new ArrayList<>();
    private String voucher = "";

    private List<BasketLine> savedLines;

    public void save() {
        savedLines = lines;          // an alias, not a copy
        // and nothing whatsoever about the voucher
    }

    public void undo() {
        if (savedLines == null) {
            return;
        }
        lines.clear();               // this clears savedLines too — same list
        lines.addAll(savedLines);
    }

    public void add(String product, int pounds, int quantity) {
        lines.add(new BasketLine(product, pounds, quantity));
    }

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

    public String describe() {
        StringBuilder sb = new StringBuilder();
        for (BasketLine line : lines) {
            sb.append("    ").append(line).append('\n');
        }
        if (lines.isEmpty()) {
            sb.append("    (the basket is empty)\n");
        }
        sb.append("    voucher: ").append(voucher.isEmpty() ? "(none)" : voucher).append('\n');
        sb.append("    total: £").append(total());
        return sb.toString();
    }
}
