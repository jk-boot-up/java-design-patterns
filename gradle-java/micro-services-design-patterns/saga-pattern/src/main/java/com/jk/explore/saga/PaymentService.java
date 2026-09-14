package com.jk.explore.saga;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Payments, and the clearest example in the project of why compensation is not rollback.
 *
 * A charge is an entry in {@link #entries()}. A refund is <em>another</em> entry, with a
 * minus in front of it. Nothing is ever removed. The customer's statement will show both
 * lines, they will see the money leave and come back, and they may well ring up to ask why
 * — which is a support cost that a database rollback would never have created.
 */
public final class PaymentService {

    public static final long LATENCY_MILLIS = 100;

    /** One movement of money. Charges are positive, refunds negative. */
    public record Entry(String ref, String orderId, Money amount, String kind) {
    }

    private final List<Entry> entries = new ArrayList<>();
    private final Map<String, Entry> charges = new LinkedHashMap<>();
    private final RemoteCall<SagaContext, String> charge;
    private final RemoteCall<String, String> refund;
    private int nextRef = 1;
    private boolean declineEverything;

    public PaymentService(SimulatedClock clock, CallLog log) {
        this.charge = new RemoteCall<>("Payments", LATENCY_MILLIS, this::doCharge, clock, log);
        this.refund = new RemoteCall<>("Payments", LATENCY_MILLIS, this::doRefund, clock, log);
    }

    public String charge(SagaContext context) {
        return charge.invoke(context);
    }

    public String refund(String chargeRef) {
        return refund.invoke(chargeRef);
    }

    public void failNextCharge(int count) {
        charge.failNext(count);
    }

    /** Scripts the refund to fail — the case a saga must have an answer for. */
    public void failNextRefund(int count) {
        refund.failNext(count);
    }

    /** The bank refusing the card, which is not an outage and must not be retried. */
    public void declineEverything() {
        declineEverything = true;
    }

    public List<Entry> entries() {
        return List.copyOf(entries);
    }

    /** What the shop is actually holding: charges less refunds. */
    public Money netTaken() {
        return entries.stream().map(Entry::amount).reduce(Money.pence(0), Money::plus);
    }

    private String doCharge(SagaContext context) {
        if (declineEverything) {
            throw new CardDeclinedException(context.orderId());
        }
        String ref = "chg-" + nextRef++;
        Entry entry = new Entry(ref, context.orderId(), context.total(), "CHARGE");
        entries.add(entry);
        charges.put(ref, entry);
        return ref;
    }

    private String doRefund(String chargeRef) {
        Entry original = charges.get(chargeRef);
        if (original == null) {
            throw new IllegalArgumentException("no such charge: " + chargeRef);
        }
        // Note what this does not do: it does not delete the charge.
        entries.add(new Entry("ref-" + nextRef++, original.orderId(),
                Money.pence(-original.amount().pence()), "REFUND"));
        return "refunded " + chargeRef;
    }
}
