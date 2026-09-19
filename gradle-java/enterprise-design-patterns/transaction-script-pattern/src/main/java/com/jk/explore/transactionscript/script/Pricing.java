package com.jk.explore.transactionscript.script;

/** The shared helper: still procedural, still no objects, but the rule now lives once. */
public final class Pricing {

    private Pricing() {
    }

    public static long total(String sku, int quantity) {
        long unit = sku.startsWith("ESP") ? 30000 : 800;
        long total = unit * quantity;
        return quantity >= 5 ? total - total / 10 : total;
    }
}
