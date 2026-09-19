package com.jk.explore.boundedcontext.shipping;

import com.jk.explore.boundedcontext.shared.CustomerId;
import com.jk.explore.boundedcontext.shared.CustomerRenamed;
import com.jk.explore.boundedcontext.shared.EventBus;

import java.util.HashMap;
import java.util.Map;

public class ShippingContext {

    private final Map<CustomerId, Recipient> recipients = new HashMap<>();

    public ShippingContext(EventBus bus) {
        bus.subscribe(this::onRenamed);
    }

    public void register(Recipient recipient) {
        recipients.put(recipient.id(), recipient);
    }

    public Recipient recipient(CustomerId id) {
        return recipients.get(id);
    }

    /** Shipping's own translation of a Sales fact into a change to its own model. */
    private void onRenamed(CustomerRenamed event) {
        Recipient old = recipients.get(event.id());
        if (old != null) {
            recipients.put(event.id(), new Recipient(old.id(), event.newName(), old.address(), old.parcelsInTransit()));
        }
    }
}
