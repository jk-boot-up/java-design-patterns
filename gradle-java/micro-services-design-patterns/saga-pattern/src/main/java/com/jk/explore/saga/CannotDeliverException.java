package com.jk.explore.saga;

/** No courier will carry this parcel to that address. A refusal, not an outage. */
public class CannotDeliverException extends RuntimeException {

    public CannotDeliverException(String orderId) {
        super("no courier covers the delivery address for " + orderId);
    }
}
