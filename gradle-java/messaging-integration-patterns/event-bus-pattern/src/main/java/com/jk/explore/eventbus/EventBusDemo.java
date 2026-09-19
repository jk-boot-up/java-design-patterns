package com.jk.explore.eventbus;

import java.util.ArrayList;
import java.util.List;

public class EventBusDemo {

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. Everyone knows everyone.");
        int components = 5;
        System.out.println("  " + components + " components that each tell each other about orders: " + components * (components - 1) + " references between them.");
        System.out.println("  add a sixth and it needs " + 2 * components + " more.");
    }

    private static void two() {
        System.out.println("TWO. Everyone knows the bus.");
        EventBus bus = new EventBus();
        List<String> log = new ArrayList<>();
        for (String name : List.of("inventory", "email", "analytics")) {
            bus.subscribe(OrderPlaced.class, e -> log.add(name + " saw " + e.orderId()));
        }
        bus.post(new OrderPlaced("ORD-1", 4999));
        System.out.println("  " + log + ".");
        System.out.println("  " + "5 components, each with 1 reference to the bus: 5 references, not 20. the poster has no reference to any subscriber.");
    }

    private static void three() {
        System.out.println("THREE. By type.");
        EventBus bus = new EventBus();
        List<String> placedOnly = new ArrayList<>();
        List<String> everything = new ArrayList<>();
        bus.subscribe(OrderPlaced.class, e -> placedOnly.add(e.orderId()));
        bus.subscribe(OrderEvent.class, e -> everything.add(e.getClass().getSimpleName() + " " + e.orderId()));
        bus.post(new OrderPlaced("ORD-1", 4999));
        bus.post(new OrderCancelled("ORD-1"));
        System.out.println("  a subscriber for OrderPlaced heard: " + placedOnly + ".");
        System.out.println("  a subscriber for every OrderEvent heard: " + everything + ".");
    }

    private static void four() {
        System.out.println("FOUR. One failing subscriber.");
        EventBus bus = new EventBus();
        List<String> log = new ArrayList<>();
        bus.subscribe(OrderPlaced.class, e -> {
            throw new IllegalStateException("mail server timed out");
        });
        bus.subscribe(OrderPlaced.class, e -> log.add("analytics counted " + e.orderId()));
        bus.post(new OrderPlaced("ORD-1", 4999));
        System.out.println("  email failed, analytics still heard it: " + log + ". recorded: " + bus.failures() + ".");
        System.out.println("  the poster did not see the failure. it posted, and carried on.");
    }

    private static void five() {
        System.out.println("FIVE. An event nobody hears.");
        EventBus bus = new EventBus();
        List<String> dead = new ArrayList<>();
        bus.post(new OrderPlaced("ORD-1", 4999));
        System.out.println("  no subscriber yet. dead events counted: " + bus.deadEvents() + ", and nothing complained.");
        bus.subscribe(DeadEvent.class, d -> dead.add(d.event().toString()));
        bus.post(new OrderPlaced("ORD-2", 100));
        System.out.println("  with a subscriber for DeadEvent: " + dead + ".");
        System.out.println("  a typo in an event type, or a forgotten subscription, is a silent loss unless something listens for dead events.");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        EventBus bus = new EventBus();
        bus.subscribe(OrderPlaced.class, e -> { });
        bus.subscribe(OrderEvent.class, e -> { });
        System.out.println("  who reacts to an OrderPlaced? nothing in the code that posts it says. the bus can be asked: " + bus.subscribersOf(OrderPlaced.class) + " subscribers.");
        for (int i = 0; i < 1000; i++) {
            bus.subscribe(OrderPlaced.class, e -> { });
        }
        System.out.println("  1000 short-lived components subscribe and are then thrown away without unsubscribing: " + bus.subscribers() + " subscribers still held.");
        List<Runnable> cancels = new ArrayList<>();
        EventBus tidy = new EventBus();
        for (int i = 0; i < 1000; i++) {
            var s = tidy.subscribe(OrderPlaced.class, e -> { });
            cancels.add(s::cancel);
        }
        cancels.forEach(Runnable::run);
        System.out.println("  the same, each cancelling its subscription: " + tidy.subscribers() + " held.");
        System.out.println("  and delivery is a plain method call in one process: a slow subscriber holds up the poster.");
    }
}
