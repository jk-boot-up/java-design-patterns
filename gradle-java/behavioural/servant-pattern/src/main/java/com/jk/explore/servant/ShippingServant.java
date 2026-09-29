package com.jk.explore.servant;

/**
 * The pattern: one class that serves every Shippable item, so the items themselves hold no shipping code.
 *
 * <p>The servant keeps no state of its own. It is handed an item, asks it only
 * what the Shippable interface promises, and does the work. One instance can
 * serve every item in the shop.
 */
public final class ShippingServant {

    private final long basePence;
    private final long perKiloPence;

    public ShippingServant(long basePence, long perKiloPence) {
        this.basePence = basePence;
        this.perKiloPence = perKiloPence;
    }

    public long postage(Shippable item) {
        return basePence + perKiloPence * ((item.grams() + 999) / 1000);
    }

    public String label(Shippable item) {
        return item.name() + " | " + item.grams() + " g | to " + item.city() + " | " + pounds(postage(item));
    }

    static String pounds(long pence) {
        return String.format("£%d.%02d", pence / 100, pence % 100);
    }
}
