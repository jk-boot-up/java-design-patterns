package com.jk.explore.aggregate.domain;

/** Whole pence, always pounds here. The same value object as the Value Object project, cut down to what this project needs. */
public record Money(long pence) implements Comparable<Money> {

    public static final Money ZERO = new Money(0);

    public static Money pounds(long pounds) {
        return new Money(pounds * 100);
    }

    public Money plus(Money other) {
        return new Money(pence + other.pence);
    }

    public Money times(int quantity) {
        return new Money(pence * quantity);
    }

    @Override
    public int compareTo(Money other) {
        return Long.compare(pence, other.pence);
    }

    @Override
    public String toString() {
        return String.format("£%d.%02d", pence / 100, pence % 100);
    }
}
