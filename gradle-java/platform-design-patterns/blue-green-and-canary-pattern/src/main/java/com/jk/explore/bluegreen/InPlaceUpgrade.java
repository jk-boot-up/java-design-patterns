package com.jk.explore.bluegreen;

/** The version where the one running copy is stopped, replaced and started again. */
public class InPlaceUpgrade {

    private final int downtimeRequests;

    public InPlaceUpgrade(int downtimeRequests) {
        this.downtimeRequests = downtimeRequests;
    }

    /** Sends the given number of requests, the first ones arriving while the service is down. Returns failures. */
    public int run(int requests) {
        return Math.min(downtimeRequests, requests);
    }
}
