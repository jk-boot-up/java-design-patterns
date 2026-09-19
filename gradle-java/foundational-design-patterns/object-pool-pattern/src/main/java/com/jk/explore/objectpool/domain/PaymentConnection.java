package com.jk.explore.objectpool.domain;

import java.util.concurrent.atomic.AtomicInteger;

/**
 * <strong>A connection to the payment gateway: expensive to make.</strong>
 * Establishing one takes {@code handshakeMillis}, a stand-in for a real
 * network handshake, and the cost is outside the JVM, which is the whole
 * reason pooling it is a good idea. It also remembers the last card holder it
 * served, so a returned connection can carry someone else's data.
 */
public class PaymentConnection {

    private static final AtomicInteger OPENED = new AtomicInteger();

    private final int number;
    private String lastCardHolder;

    public PaymentConnection(long handshakeMillis) {
        if (handshakeMillis > 0) {
            try {
                Thread.sleep(handshakeMillis);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        this.number = OPENED.incrementAndGet();
    }

    public static int openedSoFar() {
        return OPENED.get();
    }

    public static void resetCounter() {
        OPENED.set(0);
    }

    public int number() {
        return number;
    }

    public String charge(String cardHolder, long pence) {
        this.lastCardHolder = cardHolder;
        return "charged " + cardHolder + " " + pence + " pence on connection " + number;
    }

    /** What a careless caller can read: whoever used this connection last. */
    public String lastCardHolder() {
        return lastCardHolder;
    }

    public void reset() {
        this.lastCardHolder = null;
    }
}
