package com.jk.explore.contentrouter;

import java.util.function.Predicate;

/** If the message satisfies the test, it goes to that channel. */
public record Route(String description, Predicate<Order> test, String channel) {
}
