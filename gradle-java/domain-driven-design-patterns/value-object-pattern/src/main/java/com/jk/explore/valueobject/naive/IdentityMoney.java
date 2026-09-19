package com.jk.explore.valueobject.naive;

/** A money class with no equals: two of the same amount are different objects. */
public class IdentityMoney {

    private final long pence;

    public IdentityMoney(long pence) {
        this.pence = pence;
    }

    public long pence() {
        return pence;
    }
}
