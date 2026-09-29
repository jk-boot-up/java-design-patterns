package com.jk.explore.halfsync;

import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

/**
 * The slow, blocking work each order needs: save it, charge the card, send the email. 100 ms in all.
 */
public final class OrderWork {

    private final List<String> done = new CopyOnWriteArrayList<>();

    /** Plain, step-by-step, blocking code: easy to read, easy to debug. */
    public void process(String orderId) {
        pause(30);   // save to the database
        pause(50);   // charge the card
        pause(20);   // send the confirmation email
        done.add(orderId);
    }

    public int done() {
        return done.size();
    }

    static void pause(long ms) {
        try {
            Thread.sleep(ms);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
