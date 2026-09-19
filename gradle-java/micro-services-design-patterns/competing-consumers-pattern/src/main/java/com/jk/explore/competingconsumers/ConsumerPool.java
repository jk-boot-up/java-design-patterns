package com.jk.explore.competingconsumers;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;

/** N threads, each looping: take a message, handle it, acknowledge it or give it back if the handler throws. */
public class ConsumerPool implements AutoCloseable {

    private final List<Thread> threads = new ArrayList<>();
    private volatile boolean running = true;

    public ConsumerPool(Broker broker, int consumers, java.util.function.BiConsumer<String, Delivery> handler) {
        for (int i = 0; i < consumers; i++) {
            String name = "consumer-" + (char) ('A' + i);
            Thread t = new Thread(() -> {
                while (running) {
                    try {
                        Delivery d = broker.receive();
                        if (d == null) {
                            continue;
                        }
                        try {
                            handler.accept(name, d);
                            broker.ack(d);
                        } catch (RuntimeException e) {
                            broker.nack(d);
                        }
                    } catch (InterruptedException e) {
                        return;
                    }
                }
            }, name);
            t.start();
            threads.add(t);
        }
    }

    /** Waits, up to a deadline, for something to become true. */
    public static boolean until(java.util.function.BooleanSupplier condition) {
        long deadline = System.nanoTime() + 10_000_000_000L;
        while (System.nanoTime() < deadline) {
            if (condition.getAsBoolean()) {
                return true;
            }
            Thread.onSpinWait();
        }
        return false;
    }

    @Override
    public void close() {
        running = false;
        threads.forEach(Thread::interrupt);
        for (Thread t : threads) {
            try {
                t.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
}
