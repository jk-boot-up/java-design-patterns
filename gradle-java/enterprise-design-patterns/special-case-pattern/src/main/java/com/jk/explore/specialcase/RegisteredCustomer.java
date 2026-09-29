package com.jk.explore.specialcase;

/**
 * An ordinary customer with an account, loyalty points and a member discount.
 */
public final class RegisteredCustomer implements Customer {

    private final String name;
    private long points;

    public RegisteredCustomer(String name, long points) {
        this.name = name;
        this.points = points;
    }

    public String name() {
        return name;
    }

    public long points() {
        return points;
    }

    /** One point per pound spent. */
    public void earnPoints(long spentPence) {
        points += spentPence / 100;
    }

    public int discountPercent() {
        return 5;
    }

    public boolean canReceiveMarketing() {
        return true;
    }
}
