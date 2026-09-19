package com.jk.explore.domainevent.domain;

/** Something that has already happened in the business. Named in the past tense, and never changed. */
public sealed interface DomainEvent permits OrderPlaced, OrderCancelled {
    String orderId();
}
