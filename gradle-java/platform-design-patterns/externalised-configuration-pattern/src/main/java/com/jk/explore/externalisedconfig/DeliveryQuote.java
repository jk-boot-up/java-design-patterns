package com.jk.explore.externalisedconfig;

/**
 * What the shop told one customer their delivery would cost, and why.
 *
 * <p>The {@code why} half of that sentence is the part worth noticing. A quote
 * that says only "delivery £4.99" is impossible to argue with and impossible to
 * debug. This one also carries the threshold that was applied and where that
 * threshold came from, so when a customer insists they were promised free
 * delivery you can answer the question instead of guessing at it.
 *
 * <p>{@link #thresholdCameFrom()} is a plain sentence like {@code "the config
 * server"} or {@code "the default compiled into the code"}. In a shop run on
 * externalised configuration that sentence is the first thing you want on the
 * screen, because "which value was in force at 9am on Saturday" becomes a real
 * question the moment the value can change without a release.
 *
 * @param basket the basket that was quoted
 * @param deliveryCost what the customer pays for delivery, zero when it is free
 * @param thresholdApplied the spend-over figure that was in force for this quote
 * @param thresholdCameFrom where that figure was read from, in words
 */
public record DeliveryQuote(Basket basket,
                            Money deliveryCost,
                            Money thresholdApplied,
                            String thresholdCameFrom) {

    /** True when the customer pays nothing for delivery. */
    public boolean isFree() {
        return deliveryCost.pence() == 0;
    }

    /** One line, the way it would read on the checkout page. */
    public String asLine() {
        return basket.orderId() + "  goods " + basket.goodsTotal()
                + "  delivery " + (isFree() ? "FREE" : deliveryCost.toString());
    }
}
