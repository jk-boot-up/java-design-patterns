package com.jk.explore.modularmonolith.mud;

import java.util.HashMap;
import java.util.Map;

/**
 * Without the pattern: every table is public, so any part of the shop can read and change any of them.
 */
public final class Tables {

    /** Stock per product. The catalogue's rule is "never below zero", but nothing stops anyone else. */
    public static final Map<String, Integer> STOCK = new HashMap<>();

    /** Payments taken, in pence, per order. */
    public static final Map<String, Long> PAYMENTS = new HashMap<>();

    private Tables() {
    }
}
