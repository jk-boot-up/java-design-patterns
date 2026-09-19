package com.jk.explore.boundedcontext.shared;

/** A fact published by Sales and understood by anyone who cares, in a shared language of ids and plain values. */
public record CustomerRenamed(CustomerId id, String newName) {
}
