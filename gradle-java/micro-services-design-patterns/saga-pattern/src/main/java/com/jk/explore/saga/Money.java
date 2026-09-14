package com.jk.explore.saga;

/** An amount in pounds, held as whole pence so nothing rounds badly. */
public record Money(long pence) {

    public static Money pence(long pence) {
        return new Money(pence);
    }

    public Money times(int quantity) {
        return new Money(pence * quantity);
    }

    public Money plus(Money other) {
        return new Money(pence + other.pence);
    }

    public Money minus(Money other) {
        return new Money(pence - other.pence);
    }

    /** Refunds are negative, so the sign goes in front of the pounds, not inside the pence. */
    @Override
    public String toString() {
        long absolute = Math.abs(pence);
        return String.format("%s£%d.%02d", pence < 0 ? "-" : "",
                absolute / 100, absolute % 100);
    }
}
