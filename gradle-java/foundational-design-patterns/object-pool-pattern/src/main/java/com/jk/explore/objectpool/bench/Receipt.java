package com.jk.explore.objectpool.bench;

/** A small, cheap object: three fields. Exactly the kind of thing people are tempted to pool. */
public final class Receipt {

    long number;
    long pence;
    long customer;

    void fill(long i) {
        number = i;
        pence = i * 3;
        customer = i & 7;
    }

    long total() {
        return number + pence + customer;
    }

    void clear() {
        number = 0;
        pence = 0;
        customer = 0;
    }
}
