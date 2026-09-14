package com.jk.explore.apicomposition;

/**
 * The arithmetic that surprises people.
 *
 * A page that needs three services to answer is up only when all three are up, and
 * probabilities of independent things all happening are multiplied, not averaged. Three
 * services at 99.9% give a page at 99.7%. Put another way, each service is allowed about
 * forty-three minutes of downtime a month and the page gets a bit over two hours of it,
 * because the outages do not overlap.
 *
 * <p>The way out is not better services. It is needing fewer of them, which is what
 * {@link #whenOnlyOneIsRequired} measures: once Catalog and Shipping are optional, the
 * page is up whenever Orders is up, and the other two outages cost a gap on the page
 * instead of the page.
 */
public final class Availability {

    private Availability() {
    }

    /** The chance every one of these is up at the same moment. */
    public static double whenAllAreRequired(double... perService) {
        double together = 1.0;
        for (double service : perService) {
            together *= service;
        }
        return together;
    }

    /** The chance the page renders at all, when only the first service is required. */
    public static double whenOnlyOneIsRequired(double required) {
        return required;
    }

    /** Minutes of downtime a month at a given availability, to one decimal place. */
    public static double downtimeMinutesPerMonth(double availability) {
        double minutesInAMonth = 30 * 24 * 60;
        return Math.round((1.0 - availability) * minutesInAMonth * 10) / 10.0;
    }

    public static String asPercent(double availability) {
        return String.format("%.3f%%", availability * 100);
    }
}
