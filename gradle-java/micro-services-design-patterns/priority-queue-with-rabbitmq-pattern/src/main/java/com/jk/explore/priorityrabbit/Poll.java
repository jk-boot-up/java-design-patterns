package com.jk.explore.priorityrabbit;

import java.util.function.BooleanSupplier;

/**
 * Waits for a real condition, checking often, and gives up after a limit. Never a fixed sleep.
 */
public final class Poll {

    public static void until(String what, BooleanSupplier condition) {
        long deadline = System.currentTimeMillis() + 30_000;
        while (!condition.getAsBoolean()) {
            if (System.currentTimeMillis() > deadline) {
                throw new IllegalStateException("gave up waiting for " + what);
            }
            try {
                Thread.sleep(20);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new IllegalStateException(e);
            }
        }
    }

    private Poll() {
    }
}
