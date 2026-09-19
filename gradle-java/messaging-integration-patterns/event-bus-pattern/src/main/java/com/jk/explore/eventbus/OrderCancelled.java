package com.jk.explore.eventbus;

public record OrderCancelled(String orderId) implements OrderEvent {
}
