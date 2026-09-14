package com.jk.explore.cqrs;

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

    @Override
    public String toString() {
        return String.format("£%d.%02d", pence / 100, pence % 100);
    }
}
