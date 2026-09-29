package com.jk.explore.requestreply;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: replies matched by arrival order, correlation IDs, return addresses, many requests in flight, and the bill.
 */
public final class RequestReplyDemo {

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();

        out.add("ONE. Two requests; replies assumed to come back in the same order.");
        try (InventoryService inventory = new InventoryService()) {
            List<String> matched = InOrderRequester.ask(inventory.requests(),
                    List.of("reserve KETTLE-1 x 5", "reserve MUG-1 x 2"));
            matched.forEach(m -> out.add("  " + m));
            out.add("  only 4 kettles exist, so the kettle was refused; the mug reply arrived first and was taken as the kettle's");
        }

        out.add("");
        out.add("TWO. Correlation IDs: every reply names its request.");
        try (InventoryService inventory = new InventoryService();
             Requester checkout = new Requester("WEB", inventory.requests())) {
            Requester.Sent kettle = checkout.send("reserve KETTLE-1 x 5");
            Requester.Sent mug = checkout.send("reserve MUG-1 x 2");
            out.add("  " + kettle.id() + " reserve KETTLE-1 x 5 -> " + kettle.await(2000));
            out.add("  " + mug.id() + " reserve MUG-1 x 2 -> " + mug.await(2000));
            out.add("  the mug reply still arrived first; its correlation ID said which request it answered");

            out.add("");
            out.add("THREE. Return addresses: each requester gets its own replies.");
            try (Requester app = new Requester("APP", inventory.requests())) {
                Requester.Sent fromApp = app.send("reserve TEAPOT-1 x 1");
                Requester.Sent fromWeb = checkout.send("reserve TEAPOT-1 x 2");
                out.add("  phone app " + fromApp.id() + " -> " + fromApp.await(2000));
                out.add("  web checkout " + fromWeb.id() + " -> " + fromWeb.await(2000));
                out.add("  one inventory service; each reply went to the queue named in its request");
            }

            out.add("");
            out.add("FOUR. Many requests in flight at once.");
            List<Requester.Sent> many = new ArrayList<>();
            for (int i = 0; i < 20; i++) {
                many.add(checkout.send(i % 2 == 0 ? "reserve MUG-1 x 1" : "reserve KETTLE-1 x 0"));
            }
            long matchedOk = many.stream().filter(s -> s.await(3000).startsWith("RESERVED")).count();
            out.add("  20 requests sent before any reply: " + matchedOk + " answered and matched");
            out.add("  requests still waiting: " + checkout.pending());

            out.add("");
            out.add("FIVE. The bill: a reply that never comes.");
            inventory.loseNextReply();
            Requester.Sent lost = checkout.send("reserve MUG-1 x 1");
            out.add("  " + lost.id() + ": " + lost.await(500));
            out.add("  still in the waiting table: " + checkout.pending() + "; someone must time it out and clean up");
            checkout.forget(lost.id());
            out.add("  and was the mug reserved or not? the requester cannot tell");
        }
        return out;
    }

    private RequestReplyDemo() {
    }
}
