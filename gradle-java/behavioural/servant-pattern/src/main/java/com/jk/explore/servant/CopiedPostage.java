package com.jk.explore.servant;

/**
 * Without the pattern: each kind of item carried its own copy of the postage sum.
 *
 * <p>When the carrier raised its prices, the parcel copy was updated and the
 * other two were missed. Each method looks right on its own.
 */
public final class CopiedPostage {

    /** Parcel's copy: updated to the new rates, 120p plus 160p per started kilo. */
    public static long parcel(Items.Parcel p) {
        return 120 + 160L * ((p.grams() + 999) / 1000);
    }

    /** Letter's copy: still the old rates. */
    public static long letter(Items.Letter l) {
        return 100 + 150L * ((l.grams() + 999) / 1000);
    }

    /** Gift card's copy: still the old rates. */
    public static long giftCard(Items.GiftCard g) {
        return 100 + 150L * ((g.grams() + 999) / 1000);
    }

    private CopiedPostage() {
    }
}
