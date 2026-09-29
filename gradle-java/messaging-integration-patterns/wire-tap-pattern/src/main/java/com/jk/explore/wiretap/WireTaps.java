package com.jk.explore.wiretap;

import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.function.Consumer;

/**
 * The pattern's taps: copies of the traffic for someone else to look at, while the real message carries on untouched.
 */
public final class WireTaps {

    /** An audit log: keeps a copy of every message, with the card number masked. */
    public static final class AuditLog implements Consumer<PaymentMessage> {
        private final List<String> lines = new CopyOnWriteArrayList<>();
        private final boolean mask;

        public AuditLog(boolean mask) {
            this.mask = mask;
        }

        public void accept(PaymentMessage m) {
            lines.add((mask ? m.masked() : m).toString());
        }

        public List<String> lines() {
            return lines;
        }
    }

    /** A running total of what went through, for a sales dashboard. */
    public static final class SalesMeter implements Consumer<PaymentMessage> {
        private long charged;
        private long refunded;

        public void accept(PaymentMessage m) {
            if (m.kind().equals("CHARGE")) {
                charged += m.pence();
            } else {
                refunded += m.pence();
            }
        }

        public long net() {
            return charged - refunded;
        }
    }

    /** A slow tap, such as one that writes to a remote log over the network. */
    public static Consumer<PaymentMessage> slow(Consumer<PaymentMessage> inner, long ms) {
        return m -> {
            try {
                Thread.sleep(ms);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            inner.accept(m);
        };
    }

    /** Runs a tap on its own thread, so the main flow never waits for it. */
    public static final class Async implements Consumer<PaymentMessage>, AutoCloseable {
        private final ExecutorService worker = Executors.newSingleThreadExecutor();
        private final Consumer<PaymentMessage> inner;

        public Async(Consumer<PaymentMessage> inner) {
            this.inner = inner;
        }

        public void accept(PaymentMessage m) {
            worker.submit(() -> inner.accept(m));
        }

        @Override
        public void close() throws InterruptedException {
            worker.shutdown();
            worker.awaitTermination(5, TimeUnit.SECONDS);
        }
    }

    private WireTaps() {
    }
}
