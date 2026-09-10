package com.jk.explore.memento;

import java.util.List;

/**
 * A saved copy of a basket — the memento.
 *
 * <p>Two things about this class are the whole pattern.
 *
 * <p>First, it is a <em>copy</em>. The list of lines is copied on the way in
 * with {@link List#copyOf}, so later edits to the basket cannot reach back and
 * change a snapshot that was taken before them. A snapshot is a photograph,
 * not a window.
 *
 * <p>Second, look at what is public and what is not. {@link #label()} is
 * public, and it is all the outside world gets: enough for a history list to
 * show "undo: removed the mug", and nothing more. The two methods that
 * actually give up the basket's contents are package-private, so only
 * {@link Basket}, which lives in this package, can call them. The caretaker
 * can hold a snapshot and hand it back, but it cannot read the basket out of
 * it and it cannot alter it. That is the "narrow interface" the pattern asks
 * for, expressed with nothing more exotic than Java's default access.
 */
public final class BasketSnapshot {

    private final List<BasketLine> lines;
    private final String voucher;
    private final String label;

    BasketSnapshot(List<BasketLine> lines, String voucher, String label) {
        this.lines = List.copyOf(lines);   // the copy — not the caller's list
        this.voucher = voucher;
        this.label = label;
    }

    /** What the shopper did just before this was taken, for the history list. */
    public String label() {
        return label;
    }

    // Package-private on purpose: only Basket may look inside a snapshot.

    List<BasketLine> lines() {
        return lines;
    }

    String voucher() {
        return voucher;
    }

    @Override
    public String toString() {
        return "snapshot before: " + label;
    }
}
