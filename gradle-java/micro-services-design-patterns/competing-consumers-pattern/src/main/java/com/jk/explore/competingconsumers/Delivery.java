package com.jk.explore.competingconsumers;

/** One message handed to one consumer, with the number of times it has been handed out. */
public record Delivery(int id, String body, int attempt) {
}
