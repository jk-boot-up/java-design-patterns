package com.jk.explore.domainevent.domain;

/** A fact: this order was placed, by this customer, for this much. It carries data, not the order itself. */
public record OrderPlaced(String orderId, String customerId, long totalPence) implements DomainEvent {
}
