package com.jk.explore.statetable;

/**
 * Without the pattern: each method checks the status its own way. Two checks were forgotten.
 *
 * <p>{@code cancel} only refuses SHIPPED, so a DELIVERED order can be
 * cancelled. {@code refund} only refuses PLACED, so an order can be refunded
 * twice. Nothing here looks wrong on its own.
 */
public final class IfElseOrder {

    private Status status = Status.PLACED;
    private int refunds;

    public void pay() {
        if (status != Status.PLACED) {
            throw new IllegalStateException("already paid");
        }
        status = Status.PAID;
    }

    public void ship() {
        if (status == Status.PAID) {
            status = Status.SHIPPED;
        } else {
            throw new IllegalStateException("not paid");
        }
    }

    public void deliver() {
        if (status == Status.SHIPPED) {
            status = Status.DELIVERED;
        }
    }

    public void cancel() {
        if (status == Status.SHIPPED) {
            throw new IllegalStateException("already shipped");
        }
        status = Status.CANCELLED;
    }

    public void refund() {
        if (status == Status.PLACED) {
            throw new IllegalStateException("nothing paid");
        }
        refunds++;
        status = Status.REFUNDED;
    }

    public Status status() {
        return status;
    }

    public int refunds() {
        return refunds;
    }
}
