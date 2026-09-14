package com.jk.explore.saga;

/**
 * The bank said no.
 *
 * Worth separating from {@link ServiceUnavailableException}: an outage might be over in a
 * second, and a declined card will be declined again for the same reason. One is worth
 * retrying and the other is worth stopping for.
 */
public class CardDeclinedException extends RuntimeException {

    public CardDeclinedException(String orderId) {
        super("the card was declined for " + orderId);
    }
}
