package com.jk.explore.boundedcontext.support;

import com.jk.explore.boundedcontext.shared.CustomerId;

/** In Support, a customer is a contact: a person to phone, with tickets. Active means an open ticket. */
public record Contact(CustomerId id, String name, String phone, int openTickets) {

    public boolean isActive() {
        return openTickets > 0;
    }
}
