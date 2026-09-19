package com.jk.explore.aggregate.infrastructure;

/** What a load returns: the aggregate, and the version it had when it was read. */
public record Loaded<T>(T value, int version) {
}
