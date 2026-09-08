package com.jk.explore.state;

import java.util.ArrayList;
import java.util.List;

/**
 * The trap, kept for contrast: the same order lifecycle written as a status
 * field and a chain of conditionals per method.
 *
 * <p>Be fair to it. It is a third of the code, every rule is visible without
 * opening another file, and on the day it was written it was correct. The
 * problem is that the same rule — which states may be cancelled — is now
 * written out in three separate chains, in three methods, and nothing keeps
 * them in agreement. Two of them have since drifted.
 *
 * <p>The two {@code // Drifted} comments below mark the differences. Both are
 * one condition. Both cost real money. Neither throws.
 */
public final class NaiveOrder {

    public enum Status { PLACED, PAID, PACKED, SHIPPED, DELIVERED, CANCELLED, REFUNDED }

    private final String id;
    private final Money total;
    private final Ledger ledger = new Ledger();
    private final List<String> history = new ArrayList<>();

    private Status status = Status.PLACED;

    public NaiveOrder(String id, Money total) {
        this.id = id;
        this.total = total;
    }

    public void pay() {
        if (status != Status.PLACED) {
            throw new IllegalTransitionException(status.name(), "pay", "it is not PLACED");
        }
        ledger.charge(total);
        move(Status.PAID, "charged " + total);
    }

    public void pack() {
        if (status != Status.PAID) {
            throw new IllegalTransitionException(status.name(), "pack", "it is not PAID");
        }
        move(Status.PACKED, "boxed at Reading");
    }

    public void ship() {
        if (status != Status.PACKED) {
            throw new IllegalTransitionException(status.name(), "ship", "it is not PACKED");
        }
        move(Status.SHIPPED, "consignment CON-" + id);
    }

    public void deliver() {
        if (status != Status.SHIPPED) {
            throw new IllegalTransitionException(status.name(), "deliver", "it is not SHIPPED");
        }
        move(Status.DELIVERED, "signed for");
    }

    public void cancel(String reason) {
        // Drifted: written as "anything that has not arrived yet", which reads
        // sensibly and quietly includes SHIPPED. The parcel is on a van.
        if (status == Status.DELIVERED || status == Status.CANCELLED
                || status == Status.REFUNDED) {
            throw new IllegalTransitionException(status.name(), "cancel",
                    "it is not cancellable");
        }
        Money back = ledger.charged().minus(ledger.refunded());
        if (!back.isZero()) {
            ledger.refund(back);
        }
        move(Status.CANCELLED, reason + " — refunded " + back);
    }

    public void refund(String reason) {
        // Drifted: CANCELLED was added here so support could "sort out"
        // cancelled orders. A cancel has already refunded, so this pays twice.
        if (status != Status.DELIVERED && status != Status.CANCELLED) {
            throw new IllegalTransitionException(status.name(), "refund",
                    "it has not been delivered");
        }
        ledger.refund(total);
        move(Status.REFUNDED, reason + " — refunded " + total);
    }

    /**
     * The third copy of the same rules, written for the screen.
     *
     * <p>It says a SHIPPED order can only be delivered, which is right — and
     * which {@link #cancel} disagrees with. So the button is not drawn and the
     * endpoint accepts the call anyway.
     */
    public List<String> allowedActions() {
        return switch (status) {
            case PLACED -> List.of("pay", "cancel");
            case PAID -> List.of("pack", "cancel");
            case PACKED -> List.of("ship", "cancel");
            case SHIPPED -> List.of("deliver");
            case DELIVERED -> List.of("refund");
            case CANCELLED, REFUNDED -> List.of();
        };
    }

    private void move(Status next, String detail) {
        history.add(String.format("%-8s -> %-10s %s", status.name(), next.name(), detail));
        status = next;
    }

    public Status status() {
        return status;
    }

    public Ledger ledger() {
        return ledger;
    }

    public List<String> history() {
        return List.copyOf(history);
    }
}
