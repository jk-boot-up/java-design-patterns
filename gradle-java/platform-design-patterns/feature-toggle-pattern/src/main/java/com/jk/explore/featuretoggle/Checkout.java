package com.jk.explore.featuretoggle;

/** The checkout ships with gift wrap already in it. A toggle decides who gets it. */
public class Checkout {

    public static final long GIFT_WRAP_CENTS = 300;

    private final Toggles toggles;
    private final boolean giftWrapHasABug;

    public Checkout(Toggles toggles, boolean giftWrapHasABug) {
        this.toggles = toggles;
        this.giftWrapHasABug = giftWrapHasABug;
    }

    /** Returns the total, or -1 if the order failed. */
    public long total(String customerId, long baseCents) {
        if (toggles.isOn("gift-wrap", customerId)) {
            if (giftWrapHasABug) {
                return -1;
            }
            return baseCents + GIFT_WRAP_CENTS;
        }
        return baseCents;
    }
}
