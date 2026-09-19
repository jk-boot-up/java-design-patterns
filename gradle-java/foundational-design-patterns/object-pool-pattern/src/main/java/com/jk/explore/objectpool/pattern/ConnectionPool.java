package com.jk.explore.objectpool.pattern;

import com.jk.explore.objectpool.domain.PaymentConnection;

import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.TimeUnit;

/**
 * <strong>A pool of connections, borrowed and returned.</strong> The right
 * use of the pattern: the thing pooled is expensive to create <em>outside</em>
 * the JVM. Connections are created up front, once.
 *
 * <p>{@code resetOnReturn} is the difference between a safe pool and one that
 * hands the next borrower the previous customer's data.
 */
public class ConnectionPool {

    private final BlockingQueue<PaymentConnection> idle;
    private final boolean resetOnReturn;
    private final int size;

    public ConnectionPool(int size, long handshakeMillis, boolean resetOnReturn) {
        this.size = size;
        this.idle = new ArrayBlockingQueue<>(size);
        this.resetOnReturn = resetOnReturn;
        for (int i = 0; i < size; i++) {
            idle.add(new PaymentConnection(handshakeMillis));
        }
    }

    public PaymentConnection borrow() throws InterruptedException {
        return idle.take();
    }

    /** Waits at most {@code millis}. Returns null when the pool is exhausted. */
    public PaymentConnection borrow(long millis) throws InterruptedException {
        return idle.poll(millis, TimeUnit.MILLISECONDS);
    }

    public void giveBack(PaymentConnection connection) {
        if (resetOnReturn) {
            connection.reset();
        }
        idle.add(connection);
    }

    public int size() {
        return size;
    }

    public int idleCount() {
        return idle.size();
    }
}
