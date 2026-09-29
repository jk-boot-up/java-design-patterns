package com.jk.explore.contextmap.kernel;

/**
 * Shared kernel: whole pence, so sales and shipping add up the same way.
 */
public record Money(long pence) {

    public Money plus(Money other) {
        return new Money(pence + other.pence);
    }

    @Override
    public String toString() {
        return String.format("£%d.%02d", pence / 100, pence % 100);
    }
}
