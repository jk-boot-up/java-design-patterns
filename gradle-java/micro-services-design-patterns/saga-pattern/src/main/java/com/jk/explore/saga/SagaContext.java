package com.jk.explore.saga;

import java.util.List;

/**
 * What the steps of one saga hand to each other.
 *
 * A compensation needs to know what to compensate — you cannot refund a payment without
 * its charge reference — so the references handed back by each service are kept here as
 * the saga runs. This is the saga's state, and in a real shop it would be a row in a
 * database, written to after every step, so that the saga can be picked up again if the
 * process running it dies mid-way.
 */
public final class SagaContext {

    /** One line of the basket. */
    public record Line(String sku, int quantity, Money unitPrice) {

        public Money lineTotal() {
            return unitPrice.times(quantity);
        }
    }

    private final String orderId;
    private final String customerId;
    private final List<Line> lines;

    private String reservationRef;
    private String chargeRef;
    private String orderRef;
    private String shipmentRef;
    private boolean emailSent;

    public SagaContext(String orderId, String customerId, List<Line> lines) {
        this.orderId = orderId;
        this.customerId = customerId;
        this.lines = List.copyOf(lines);
    }

    public String orderId() {
        return orderId;
    }

    public String customerId() {
        return customerId;
    }

    public List<Line> lines() {
        return lines;
    }

    public Money total() {
        return lines.stream().map(Line::lineTotal).reduce(Money.pence(0), Money::plus);
    }

    public String reservationRef() {
        return reservationRef;
    }

    public void reservationRef(String ref) {
        this.reservationRef = ref;
    }

    public String chargeRef() {
        return chargeRef;
    }

    public void chargeRef(String ref) {
        this.chargeRef = ref;
    }

    public String orderRef() {
        return orderRef;
    }

    public void orderRef(String ref) {
        this.orderRef = ref;
    }

    public String shipmentRef() {
        return shipmentRef;
    }

    public void shipmentRef(String ref) {
        this.shipmentRef = ref;
    }

    public boolean emailSent() {
        return emailSent;
    }

    public void emailSent(boolean sent) {
        this.emailSent = sent;
    }
}
