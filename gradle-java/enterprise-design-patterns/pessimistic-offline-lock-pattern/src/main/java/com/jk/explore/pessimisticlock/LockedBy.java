package com.jk.explore.pessimisticlock;

public class LockedBy extends RuntimeException {
    private final String holder;

    public LockedBy(String resource, String holder) {
        super(resource + " is locked by " + holder);
        this.holder = holder;
    }

    public String holder() {
        return holder;
    }
}
