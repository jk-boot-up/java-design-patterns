package com.jk.explore.requestreply;

import java.util.Map;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.LinkedBlockingQueue;

/**
 * Takes "reserve SKU x N" requests from its queue, works on several at once, and replies to each request's return address.
 *
 * <p>Kettles are checked in a slow warehouse system, mugs in a fast one, so
 * replies often come back in a different order from the requests.
 */
public final class InventoryService implements AutoCloseable {

    private final BlockingQueue<Message> requests = new LinkedBlockingQueue<>();
    private final ExecutorService workers = Executors.newFixedThreadPool(8);
    private final Map<String, Integer> stock = new ConcurrentHashMap<>(Map.of("KETTLE-1", 4, "MUG-1", 50, "TEAPOT-1", 10));
    private final java.util.concurrent.atomic.AtomicBoolean loseNext = new java.util.concurrent.atomic.AtomicBoolean();
    private final Thread dispatcher;

    public InventoryService() {
        dispatcher = new Thread(() -> {
            try {
                while (true) {
                    Message m = requests.take();
                    workers.submit(() -> handle(m));
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        dispatcher.setDaemon(true);
        dispatcher.start();
    }

    private void handle(Message m) {
        String[] parts = m.body().split(" ");
        String sku = parts[1];
        int qty = Integer.parseInt(parts[3]);
        pause(sku.equals("KETTLE-1") ? 150 : 10);
        if (loseNext.compareAndSet(true, false)) {
            return;
        }
        boolean ok = stock.merge(sku, 0, Integer::sum) >= qty;
        if (ok) {
            stock.merge(sku, -qty, Integer::sum);
        }
        String answer = (ok ? "RESERVED " : "REFUSED ") + qty + " x " + sku;
        m.replyTo().add(new Message("REP-" + m.id(), m.id(), null, answer));
    }

    public BlockingQueue<Message> requests() {
        return requests;
    }

    /** For act five: the next request handled gets no reply, as if the reply were lost on the way. */
    public void loseNextReply() {
        loseNext.set(true);
    }

    static void pause(long ms) {
        try {
            Thread.sleep(ms);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    @Override
    public void close() {
        dispatcher.interrupt();
        workers.shutdownNow();
    }
}
