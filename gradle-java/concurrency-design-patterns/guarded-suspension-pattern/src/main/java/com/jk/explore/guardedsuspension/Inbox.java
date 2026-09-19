package com.jk.explore.guardedsuspension;

/** Where new orders arrive for a picker to take. */
public interface Inbox {

    void put(String order);

    /** Takes an order, waiting for one if there is none. May return null if it gives up. */
    String take() throws InterruptedException;

    /** How many times a waiting thread woke up. */
    int wakeups();
}
