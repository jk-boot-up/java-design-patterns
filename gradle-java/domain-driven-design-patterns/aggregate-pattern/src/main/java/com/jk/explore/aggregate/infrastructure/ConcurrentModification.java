package com.jk.explore.aggregate.infrastructure;

public class ConcurrentModification extends RuntimeException {
    public ConcurrentModification(String key) {
        super(key + " was changed by someone else since it was read");
    }
}
