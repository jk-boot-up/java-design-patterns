package com.jk.explore.valueobject.naive;

/** A money class that can be changed in place. Handy, and the source of a very quiet bug. */
public class MutableMoney {

    private long pence;

    public MutableMoney(long pence) {
        this.pence = pence;
    }

    public void subtract(long pence) {
        this.pence -= pence;
    }

    public long pence() {
        return pence;
    }
}
