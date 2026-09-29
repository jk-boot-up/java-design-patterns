package com.jk.explore.memoization;

/**
 * A slow shipping quote (a call to the carrier, 200 ms), and an exchange rate that changes during the day.
 */
public final class ShippingQuotes {

    public static final int MS_PER_QUOTE = 200;

    /** Pence to ship one parcel to a postcode area: depends only on the area. */
    public static long quote(String area) {
        return 300 + (Math.abs(area.hashCode()) % 5) * 50;
    }

    /** Euro cents for a pound price, at today's rate. Depends on the time: not safe to memoize by price alone. */
    public static final class Euros {
        private int centsPerPound = 116;

        public long convert(long pence) {
            return pence * centsPerPound / 100;
        }

        public void setRate(int centsPerPound) {
            this.centsPerPound = centsPerPound;
        }
    }

    private ShippingQuotes() {
    }
}
