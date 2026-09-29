package com.jk.explore.memoization;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: the same questions asked again, memoized, a reusable memo, a function that is not safe to memoize, and the bill.
 */
public final class MemoizationDemo {

    static final String[] AREAS = {"LS1", "BA2", "YO1", "HU3", "EC1", "M1", "G2", "CF10", "BS1", "NE1", "L1", "B3"};

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. The cheapest way to buy 25 mugs, worked out plainly.");
        MultiBuy plain = new MultiBuy();
        long best = plain.plain(25);
        out.add("  offers: 1 for £4, 2 for £7, 3 for £10, 5 for £15");
        out.add("  best price for 25: " + pounds(best) + ", after " + String.format("%,d", plain.calls()) + " calls");
        out.add("  \"best for 20 mugs\" was worked out again every time it was needed");

        out.add("");
        out.add("TWO. Memoized: each answer written down the first time.");
        MultiBuy memo = new MultiBuy();
        out.add("  best price for 25: " + pounds(memo.memoized(25)) + ", after " + memo.calls() + " calls");

        out.add("");
        out.add("THREE. A reusable memo around a slow shipping quote.");
        Memo<String, Long> quotes = new Memo<>(ShippingQuotes::quote);
        for (int view = 0; view < 1000; view++) {
            quotes.apply(AREAS[view % AREAS.length]);
        }
        out.add("  1000 product page views across " + AREAS.length + " postcode areas");
        out.add("  slow carrier calls: " + quotes.slowCalls() + ", " + String.format("%,d", quotes.slowCalls() * ShippingQuotes.MS_PER_QUOTE)
                + " ms instead of " + String.format("%,d", 1000 * ShippingQuotes.MS_PER_QUOTE) + " ms");

        out.add("");
        out.add("FOUR. A function that is not safe to memoize.");
        ShippingQuotes.Euros euros = new ShippingQuotes.Euros();
        Memo<Long, Long> inEuros = new Memo<>(euros::convert);
        out.add("  morning: £100.00 is " + cents(inEuros.apply(10000L)));
        euros.setRate(112);
        out.add("  at noon the rate changes; the memo still says " + cents(inEuros.apply(10000L))
                + ", the real price is " + cents(euros.convert(10000L)));
        out.add("  the answer depended on the time, not only on the price");

        out.add("");
        out.add("FIVE. The bill: a memo never forgets.");
        Memo<String, Long> everyPostcode = new Memo<>(ShippingQuotes::quote);
        for (int i = 0; i < 100_000; i++) {
            everyPostcode.apply("AREA-" + i);
        }
        out.add("  100,000 different postcodes: " + String.format("%,d", everyPostcode.size()) + " answers kept in memory");
        out.add("  real caches add a size limit and an expiry time");
        return out;
    }

    static String pounds(long pence) {
        return String.format("£%d.%02d", pence / 100, pence % 100);
    }

    static String cents(long cents) {
        return String.format("€%d.%02d", cents / 100, cents % 100);
    }

    private MemoizationDemo() {
    }
}
