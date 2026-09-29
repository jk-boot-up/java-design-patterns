package com.jk.explore.requestreplyrabbit;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts, against a real RabbitMQ broker started and stopped by this program.
 */
public final class RabbitRequestReplyDemo {

    public static void main(String[] args) throws Exception {
        if (!Broker.containerRuntimeAvailable()) {
            System.out.println(Broker.NO_RUNTIME_ADVICE);
            return;
        }
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();
        try (Broker broker = new Broker()) {
            try {
                broker.start();
            } catch (RuntimeException e) {
                out.add(Broker.WOULD_NOT_START_ADVICE);
                return out;
            }
            try (InventoryService inventory = new InventoryService(broker);
                 Requester web = new Requester(broker, false);
                 Requester app = new Requester(broker, true)) {

                out.add("ONE. Two requests; replies taken in the order they come back.");
                web.send(null, "reserve KETTLE-1 x 5", 0);
                web.send(null, "reserve MUG-1 x 2", 0);
                queued(broker, 2);
                inventory.handleWaiting();
                Poll.until("two replies", () -> web.arrivals().size() == 2);
                out.add("  reserve KETTLE-1 x 5 -> " + web.arrivals().get(0));
                out.add("  reserve MUG-1 x 2    -> " + web.arrivals().get(1));
                out.add("  the mug was answered first, from the cache, and taken as the kettle's reply");

                out.add("");
                out.add("TWO. Correlation IDs: each reply carries its request's ID.");
                web.send("WEB-1", "reserve KETTLE-1 x 5", 0);
                web.send("WEB-2", "reserve MUG-1 x 2", 0);
                queued(broker, 2);
                inventory.handleWaiting();
                out.add("  WEB-1 reserve KETTLE-1 x 5 -> " + web.await("WEB-1", 10_000));
                out.add("  WEB-2 reserve MUG-1 x 2    -> " + web.await("WEB-2", 10_000));
                out.add("  the mug reply still came first; its correlation ID said which request it answered");

                out.add("");
                out.add("THREE. Return addresses: each requester names where its reply should go.");
                app.send("APP-1", "reserve TEAPOT-1 x 1", 0);
                web.send("WEB-3", "reserve TEAPOT-1 x 2", 0);
                queued(broker, 2);
                inventory.handleWaiting();
                out.add("  phone app APP-1 -> " + app.await("APP-1", 10_000) + "  (reply to: amq.rabbitmq.reply-to)");
                out.add("  web checkout WEB-3 -> " + web.await("WEB-3", 10_000) + "  (reply to: its own exclusive queue)");
                out.add("  RabbitMQ's direct reply-to needs no reply queue declared at all");

                out.add("");
                out.add("FOUR. Many requests in flight at once.");
                List<String> ids = web.ids(20, "BULK-");
                for (String id : ids) {
                    web.send(id, "reserve MUG-1 x 0", 0);
                }
                queued(broker, 20);
                out.add("  20 requests sent before any reply; the service handled " + inventory.handleWaiting());
                Poll.until("20 replies", () -> ids.stream().allMatch(id -> web.reply(id) != null));
                out.add("  20 answered and matched; requests still waiting: " + web.waitingCount());

                out.add("");
                out.add("FIVE. The bill: a reply that never comes.");
                web.send("WEB-24", "reserve MUG-1 x 1", 500);
                String reply = web.await("WEB-24", 500);
                out.add("  the inventory service is busy; WEB-24: " + (reply == null ? "no reply after 0.5 s" : reply));
                out.add("  still in the waiting table: " + web.waitingCount() + "; the requester must time it out and clean up");
                web.forget("WEB-24");
                Poll.until("the request to expire in the queue", () -> broker.waiting(InventoryService.QUEUE) == 0);
                out.add("  the request was sent with a 0.5 s expiry, so RabbitMQ dropped it: when the service returns it handles "
                        + inventory.handleWaiting());
                out.add("  so the mug was not reserved late behind the requester's back; without the expiry, nobody could tell");
            }
        }
        return out;
    }

    /** Publishing does not wait, so wait until the requests really are on the queue. */
    private static void queued(Broker broker, int n) {
        Poll.until(n + " requests on the queue", () -> broker.waiting(InventoryService.QUEUE) == n);
    }

    private RabbitRequestReplyDemo() {
    }
}
