package com.jk.explore.wiretap;

/**
 * A message from checkout to the payment service: charge or refund an amount on a card.
 */
public record PaymentMessage(String kind, String orderId, long pence, String card) {

    public PaymentMessage masked() {
        return new PaymentMessage(kind, orderId, pence, "**** " + card.substring(card.length() - 4));
    }

    @Override
    public String toString() {
        return kind + " " + orderId + " " + String.format("£%d.%02d", pence / 100, pence % 100) + " card " + card;
    }
}
