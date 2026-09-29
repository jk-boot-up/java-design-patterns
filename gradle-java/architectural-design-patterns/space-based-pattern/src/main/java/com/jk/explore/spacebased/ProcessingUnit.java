package com.jk.explore.spacebased;

import java.util.concurrent.atomic.AtomicInteger;

/**
 * The pattern's building block: a copy of the app with its own in-memory copy of the data it needs.
 *
 * <p>It answers orders from memory, with no database in the way, and tells the
 * data grid about every change so the other units' copies catch up.
 */
public final class ProcessingUnit {

    private final String name;
    private final AtomicInteger stock;
    private final DataGrid grid;

    public ProcessingUnit(String name, int stock, DataGrid grid) {
        this.name = name;
        this.stock = new AtomicInteger(stock);
        this.grid = grid;
    }

    public boolean takeOne() {
        int left = stock.getAndUpdate(s -> s > 0 ? s - 1 : s);
        if (left <= 0) {
            return false;
        }
        grid.sold(this, 1);
        return true;
    }

    /** A change made on another unit, arriving through the grid. */
    void applyFromOthers(int sold) {
        stock.addAndGet(-sold);
    }

    public int stock() {
        return stock.get();
    }

    public String name() {
        return name;
    }
}
