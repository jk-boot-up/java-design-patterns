package com.jk.explore.processcamel;

import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;

/**
 * The shop's services: two warehouses, payments, shipping and email. Every reply is recorded per order.
 */
public final class Services {

    final Map<String, Integer> main = new ConcurrentHashMap<>(Map.of("KETTLE", 3, "TEAPOT", 0));
    final Map<String, Integer> partner = new ConcurrentHashMap<>(Map.of("KETTLE", 0, "TEAPOT", 2));
    private final Map<String, String> reservedAt = new ConcurrentHashMap<>();
    private final Map<String, List<String>> replies = new ConcurrentHashMap<>();
    private final Map<String, String> status = new ConcurrentHashMap<>();
    private final List<String> emails = new CopyOnWriteArrayList<>();

    public void reserve(Order o) {
        if (take(main, o, "main")) {
            return;
        }
        if (!take(partner, o, "partner")) {
            reply(o, "no stock anywhere");
            throw new IllegalStateException("no stock");
        }
    }

    /** Before the process manager: only the main warehouse is ever asked. */
    public void reserveMainOnly(Order o) {
        if (!take(main, o, "main")) {
            throw new IllegalStateException("out of stock");
        }
    }

    private boolean take(Map<String, Integer> stock, Order o, String name) {
        if (stock.get(o.sku()) > 0) {
            stock.merge(o.sku(), -1, Integer::sum);
            reservedAt.put(o.id(), name);
            reply(o, name + " RESERVED");
            return true;
        }
        reply(o, name + " OUT_OF_STOCK");
        return false;
    }

    /** The compensation for reserve: give the item back to whichever warehouse held it. */
    public void release(String orderId, String sku) {
        String at = reservedAt.remove(orderId);
        if (at != null) {
            (at.equals("main") ? main : partner).merge(sku, 1, Integer::sum);
            replies.computeIfAbsent(orderId, k -> new CopyOnWriteArrayList<>()).add(at + " RELEASED");
        }
    }

    public void pay(Order o) {
        if (o.card().endsWith("0002")) {
            reply(o, "DECLINED");
            throw new IllegalStateException("card declined");
        }
        reply(o, "PAID");
    }

    public void ship(Order o) {
        reply(o, "SHIPPED");
    }

    public void done(String orderId) {
        status.put(orderId, "DONE");
    }

    public void cancelled(String orderId) {
        emails.add(orderId + ": your card was declined");
        status.put(orderId, "CANCELLED, stock released");
    }

    private void reply(Order o, String r) {
        replies.computeIfAbsent(o.id(), k -> new CopyOnWriteArrayList<>()).add(r);
    }

    public List<String> replies(String orderId) {
        return replies.getOrDefault(orderId, List.of());
    }

    public String status(String orderId) {
        return status.getOrDefault(orderId, "unknown");
    }

    public Map<String, String> statuses() {
        return new java.util.TreeMap<>(status);
    }

    public List<String> emails() {
        return emails;
    }

    public int kettles() {
        return main.get("KETTLE");
    }

    /** Waits, up to a limit, until the order's replies include {@code reply}. */
    public boolean awaitReply(String orderId, String reply, long timeoutMillis) throws InterruptedException {
        long deadline = System.currentTimeMillis() + timeoutMillis;
        while (!replies(orderId).contains(reply) && System.currentTimeMillis() < deadline) {
            Thread.sleep(5);
        }
        return replies(orderId).contains(reply);
    }

    /** Waits, up to a limit, until the order has a final status. */
    public boolean awaitStatus(String orderId, long timeoutMillis) throws InterruptedException {
        long deadline = System.currentTimeMillis() + timeoutMillis;
        while (!status.containsKey(orderId) && System.currentTimeMillis() < deadline) {
            Thread.sleep(5);
        }
        return status.containsKey(orderId);
    }
}
