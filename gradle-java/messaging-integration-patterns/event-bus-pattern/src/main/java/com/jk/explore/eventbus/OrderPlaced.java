package com.jk.explore.eventbus;

public record OrderPlaced(String orderId, long pence) implements OrderEvent {
}
