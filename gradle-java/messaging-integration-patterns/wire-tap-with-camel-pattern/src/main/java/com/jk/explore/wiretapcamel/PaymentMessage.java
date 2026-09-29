package com.jk.explore.wiretapcamel;

/**
 * A payment instruction. Deliberately mutable, as many real message objects are, so the demo can
 * show what happens when a tap changes the object it was handed.
 */
public final class PaymentMessage {

    private final String kind;
    private final String orderId;
    private final long pence;
    private String card;

    public PaymentMessage(String kind, String orderId, long pence, String card) {
        this.kind = kind;
        this.orderId = orderId;
        this.pence = pence;
        this.card = card;
    }

    public PaymentMessage copy() {
        return new PaymentMessage(kind, orderId, pence, card);
    }

    public String getKind() {
        return kind;
    }

    public String getOrderId() {
        return orderId;
    }

    public long getPence() {
        return pence;
    }

    public String getCard() {
        return card;
    }

    public void setCard(String card) {
        this.card = card;
    }

    @Override
    public String toString() {
        return String.format("%s %s £%.2f card %s", kind, orderId, pence / 100.0, card);
    }
}
