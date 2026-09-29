package com.jk.explore.pollingconsumer;

import java.util.ArrayList;
import java.util.List;

/**
 * The warehouse label printer: can hold 10 jobs in its buffer and prints 5 labels every tick (a tenth of a second).
 */
public final class LabelPrinter {

    public static final int BUFFER = 10;
    public static final int PER_TICK = 5;

    private final List<String> printed = new ArrayList<>();
    private int inBuffer;

    /** Push: someone hands the printer a job whether or not it has room. */
    public boolean push(String order) {
        if (inBuffer >= BUFFER) {
            return false;
        }
        inBuffer++;
        printed.add(order);
        return true;
    }

    public void print(List<String> batch) {
        printed.addAll(batch);
    }

    public int printed() {
        return printed.size();
    }
}
