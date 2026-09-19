package com.jk.explore.flagd;

/** Ships with gift wrap already in it. flagd says who gets it. If flagd cannot be reached, nobody does. */
public class Checkout {

    public static final long GIFT_WRAP_CENTS = 300;

    private final Flagd flags;
    private final boolean giftWrapHasABug;

    public Checkout(Flagd flags, boolean giftWrapHasABug) {
        this.flags = flags;
        this.giftWrapHasABug = giftWrapHasABug;
    }

    /** Returns the total, or -1 if the order failed. */
    public long total(String customerId, long baseCents) {
        Boolean on = flags.evaluate("gift-wrap", customerId);
        if (Boolean.TRUE.equals(on)) {
            return giftWrapHasABug ? -1 : baseCents + GIFT_WRAP_CENTS;
        }
        return baseCents;
    }
}
