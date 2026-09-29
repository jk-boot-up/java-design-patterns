package com.jk.explore.specialcase;

/**
 * Checkout, written twice: with null checks, and against the Customer interface with no checks at all.
 */
public final class Checkout {

    /** Without the pattern: four places must remember the null check; the points line forgot. */
    public static String withNullChecks(RegisteredCustomer c, long pence) {
        String name = c != null ? c.name() : "Guest";
        int discount = c != null ? c.discountPercent() : 0;
        long due = pence - pence * discount / 100;
        c.earnPoints(due);
        boolean marketing = c != null && c.canReceiveMarketing();
        return name + " pays " + SpecialCaseDemo.pounds(due) + (marketing ? ", added to newsletter" : "");
    }

    /** With the pattern: the same steps, no ifs, for any kind of customer. */
    public static String run(Customer c, long pence) {
        long due = pence - pence * c.discountPercent() / 100;
        c.earnPoints(due);
        return c.name() + " pays " + SpecialCaseDemo.pounds(due) + ", points " + c.points()
                + (c.canReceiveMarketing() ? ", added to newsletter" : "");
    }

    private Checkout() {
    }
}
