package com.jk.explore.apicomposition;

/** What the Shipping service knows: who is carrying the parcel and where it is. */
public record DeliveryStatus(String carrier, String state, String expectedBy) {

    /**
     * The delivery status to show when Shipping did not answer.
     *
     * There is a temptation to invent something here — "in transit" is nearly always
     * true, after all. Do not. The page is allowed to say it does not know; it is not
     * allowed to make something up, because a shopper who is told the parcel is in
     * transit will not ring up about the one that never left.
     */
    public static DeliveryStatus unknown() {
        return new DeliveryStatus("unknown", "we cannot check this right now", "unknown");
    }

    public boolean isKnown() {
        return !"unknown".equals(carrier);
    }
}
