package com.jk.explore.publishersubscriber;

/** Something that happened, with its kind and the order it concerns. */
public record Event(String kind, String orderId) {
}
