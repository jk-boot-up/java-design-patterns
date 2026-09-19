package com.jk.explore.ratelimiter;

/** The product search: it can serve a fixed number of requests a second, and counts what it is given beyond that. */
public class SearchService {

    private final int capacityPerSecond;
    private int accepted;

    public SearchService(int capacityPerSecond) {
        this.capacityPerSecond = capacityPerSecond;
    }

    public void handle() {
        accepted++;
    }

    public int capacityPerSecond() {
        return capacityPerSecond;
    }

    public int accepted() {
        return accepted;
    }

    public int overCapacity() {
        return Math.max(0, accepted - capacityPerSecond);
    }
}
