package com.jk.explore.deadletter;

/** A message that could not be handled, with what an operator needs to know about why. */
public record DeadLetter(Message message, int attempts, String lastError, String fromChannel) {
}
