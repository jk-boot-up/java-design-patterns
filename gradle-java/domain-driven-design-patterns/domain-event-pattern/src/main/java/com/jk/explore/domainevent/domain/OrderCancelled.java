package com.jk.explore.domainevent.domain;

public record OrderCancelled(String orderId, String reason) implements DomainEvent {
}
