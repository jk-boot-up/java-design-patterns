package com.jk.explore.executearound;

import java.util.function.Consumer;

/** A customer's store credit, changed in steps that must all happen or none. */
public class Ledger {

    private long balanceCents;

    public Ledger(long balanceCents) {
        this.balanceCents = balanceCents;
    }

    public long balance() {
        return balanceCents;
    }

    public void spend(long cents) {
        balanceCents -= cents;
        if (balanceCents < 0) {
            throw new IllegalStateException("not enough credit");
        }
    }

    public void refund(long cents) {
        balanceCents += cents;
    }

    /** Execute around a set of changes: keep them if all went well, and put everything back if not. */
    public void inTransaction(Consumer<Ledger> steps) {
        long before = balanceCents;
        try {
            steps.accept(this);
        } catch (RuntimeException e) {
            balanceCents = before;
            throw e;
        }
    }
}
