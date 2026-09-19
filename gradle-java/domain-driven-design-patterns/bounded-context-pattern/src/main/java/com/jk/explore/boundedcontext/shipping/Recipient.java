package com.jk.explore.boundedcontext.shipping;

import com.jk.explore.boundedcontext.shared.CustomerId;

/** In Shipping, a customer is a recipient: a name and a place to deliver to. Active means a parcel is on its way. */
public record Recipient(CustomerId id, String name, String address, int parcelsInTransit) {

    public boolean isActive() {
        return parcelsInTransit > 0;
    }
}
