package com.jk.explore.camelrouter;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;
import org.apache.camel.builder.RouteBuilder;

/**
 * Six acts. An online store puts orders on one queue, and Apache Camel reads each order, looks at what is
 * inside it, and sends it to the queue that suits it. Every count printed comes from the broker itself.
 */
public class CamelRouterDemo {

    static final List<Order> ORDERS = List.of(
            new Order("ORD-1", "physical", "express", "UK", 4999),
            new Order("ORD-2", "digital", "none", "UK", 2500),
            new Order("ORD-3", "physical", "standard", "EU", 120000),
            new Order("ORD-4", "digital", "none", "UK", 90000),
            new Order("ORD-5", "subscription", "none", "UK", 999),
            new Order("ORD-6", "physical", "standard", "EU", 3000));

    public static void main(String[] args) {
        quietLogs();
        if (!Broker.dockerAvailable()) {
            explainNoContainerRuntime(System.out, null);
            return;
        }
        try (Broker broker = new Broker()) {
            try {
                broker.start();
            } catch (RuntimeException e) {
                explainNoContainerRuntime(System.out, e);
                return;
            }
            one(broker);
            two(broker);
            three(broker);
            four(broker);
            five(broker);
            six(broker);
        }
    }

    /**
     * What a learner sees when there is no container runtime to start the broker in. It is two plain
     * sentences and, if there was one, the short reason the runtime gave. It is never a stack trace.
     */
    static void explainNoContainerRuntime(java.io.PrintStream out, Throwable reason) {
        out.println("This demo runs a real RabbitMQ broker in a container, so it needs a container runtime.");
        out.println("Start Docker Desktop, or another Docker-compatible runtime, and run ./gradlew run again.");
        if (reason != null) {
            out.println("The broker could not be started. The runtime said: " + shortReason(reason));
        }
    }

    private static String shortReason(Throwable reason) {
        Throwable deepest = reason;
        while (deepest.getCause() != null) {
            deepest = deepest.getCause();
        }
        String message = deepest.getMessage();
        if (message == null || message.isBlank()) {
            return deepest.getClass().getSimpleName();
        }
        return message.lines().findFirst().orElse(message).strip();
    }

    /**
     * Keeps the libraries quiet so that the only thing printed is the story. Testcontainers reports a
     * missing runtime as a stack trace; this demo reports it as a sentence instead, further down.
     */
    private static void quietLogs() {
        System.setProperty("org.slf4j.simpleLogger.defaultLogLevel", "error");
        System.setProperty("org.slf4j.simpleLogger.log.org.testcontainers", "off");
        System.setProperty("org.slf4j.simpleLogger.log.tc", "off");
        System.setProperty("org.slf4j.simpleLogger.log.com.github.dockerjava", "off");
        System.setProperty("org.slf4j.simpleLogger.log.com.rabbitmq", "off");
    }

    private static void one(Broker broker) {
        System.out.println("ONE. One queue for everything.");
        broker.clear();
        for (Order order : ORDERS) {
            broker.post("warehouse-inbox", order);
        }
        broker.settleQueue("warehouse-inbox", ORDERS.size());
        Warehouse warehouse = new Warehouse();
        for (Order order : broker.take("warehouse-inbox")) {
            warehouse.handle(order);
        }
        System.out.println("  all " + ORDERS.size() + " orders arrived on the warehouse's own queue. it shipped " + warehouse.shipped()
                + " and could do nothing with " + warehouse.couldNotHandle() + ".");
        System.out.println("  the warehouse now holds an if for every kind of order, and every new kind means changing the warehouse.");
    }

    private static void two(Broker broker) {
        System.out.println("TWO. The route reads the content and chooses.");
        Map<String, String> went = routeAll(broker, ShopRoutes.standard(), ORDERS, ORDERS.size());
        for (Order order : ORDERS) {
            System.out.println("  " + order.describe() + " -> " + went.get(order.id()));
        }
        System.out.println("  " + grouped(went) + ".");
        System.out.println("  the shop's route asks " + ShopRoutes.questions()
                + " questions about the content in a fixed order, and nothing but the route knows the answers.");
    }

    private static void three(Broker broker) {
        System.out.println("THREE. The first question answered yes wins.");
        Order big = new Order("ORD-7", "digital", "none", "UK", 150000);
        String first = routeAll(broker, ShopRoutes.standard(), List.of(big), 1).get("ORD-7");
        String last = routeAll(broker, ShopRoutes.highValueLast(), List.of(big), 1).get("ORD-7");
        System.out.println("  a digital gift card worth " + big.pounds() + ". with the high value question asked first: " + first
                + ". with it asked last: " + last + ".");
        System.out.println("  the order of the questions is part of the design, and Camel does not warn you when it changes.");
    }

    private static void four(Broker broker) {
        System.out.println("FOUR. A message no question claims.");
        Order odd = new Order("ORD-8", "subscription", "none", "UK", 999);
        String caught = routeAll(broker, ShopRoutes.standard(), List.of(odd), 1).get("ORD-8");
        System.out.println("  a subscription order, which no question covers. with an otherwise branch it goes to: " + caught + ".");

        broker.clear();
        broker.post(Broker.ORDERS, odd);
        try (ShopRouter router = new ShopRouter(broker, ShopRoutes.noOtherwise())) {
            broker.settleRouted(0);
        }
        System.out.println("  with no otherwise branch the route simply ends. messages left anywhere in the shop: "
                + broker.waitingEverywhere() + ". the broker was told it was handled, so it is gone.");

        String named = routeAll(broker, ShopRoutes.otherwiseUnclaimed(), List.of(odd), 1).get("ORD-8");
        System.out.println("  an otherwise branch that names the problem sends it to: " + named
                + ", where somebody can look at it. that queue is the whole difference between a lost order and a known one.");
    }

    private static void five(Broker broker) {
        System.out.println("FIVE. A new question, and nobody else changes.");
        Order euSubscription = new Order("ORD-10", "subscription", "none", "EU", 999);
        Order euPhysical = ORDERS.get(5);
        Map<String, String> before = routeAll(broker, ShopRoutes.standard(), List.of(euSubscription), 1);
        Map<String, String> after = routeAll(broker, ShopRoutes.withEuVat(), List.of(euSubscription, euPhysical), 2);
        System.out.println("  questions before: " + ShopRoutes.questions() + ", after: " + (ShopRoutes.questions() + 1)
                + ". the senders and the receiving queues were not touched; only the route was.");
        System.out.println("  an EU subscription used to go to " + before.get("ORD-10") + ". it now goes to: " + after.get("ORD-10") + ".");
        System.out.println("  ORD-6, physical and from the EU, still goes to: " + after.get("ORD-6")
                + ", because an earlier question was answered yes first.");
    }

    private static void six(Broker broker) {
        System.out.println("SIX. The bill.");
        broker.clear();
        broker.post(Broker.ORDERS, "id=ORD-9;kind=goods;shipping=standard;region=UK;pence=100");
        try (ShopRouter router = new ShopRouter(broker, ShopRoutes.standard())) {
            broker.settleRouted(1);
        }
        String landed = whereEachWent(broker).get("ORD-9");
        System.out.println("  the sender starts calling physical orders goods. the route's question still looks for physical, so ORD-9 lands on: "
                + landed + ", quietly.");

        AtomicInteger attempts = new AtomicInteger();
        broker.clear();
        broker.post(Broker.ORDERS, new Order("ORD-11", "physical", "standard", "UK", 250000));
        try (ShopRouter router = new ShopRouter(broker, ShopRoutes.fraudCheckBroken(attempts))) {
            broker.settleRouted(1);
        }
        System.out.println("  the fraud branch is broken. Camel tried it " + attempts.get()
                + " times and then put the order on router-errors, which now holds " + broker.waiting("router-errors")
                + ". a route can fail as well as choose, and somebody has to say where the failures go.");
        System.out.println("  and the routing is now a broker and a route to keep running: this demo needed 1 container, 1 exchange and "
                + (Broker.DESTINATIONS.size() + 1) + " queues.");
    }

    /** Clears the shop, posts the orders, starts the route, waits for the broker to settle, and reports where each went. */
    static Map<String, String> routeAll(Broker broker, RouteBuilder routes, List<Order> orders, int expected) {
        broker.clear();
        for (Order order : orders) {
            broker.post(Broker.ORDERS, order);
        }
        try (ShopRouter router = new ShopRouter(broker, routes)) {
            broker.settleRouted(expected);
        }
        return whereEachWent(broker);
    }

    /** Empties every destination queue and records which queue each order was found on. */
    static Map<String, String> whereEachWent(Broker broker) {
        Map<String, String> went = new LinkedHashMap<>();
        for (String queue : Broker.DESTINATIONS) {
            for (Order order : broker.take(queue)) {
                went.put(order.id(), queue);
            }
        }
        return went;
    }

    /** The same answer the other way round: queue by queue, the orders that ended up on it. */
    private static Map<String, List<String>> grouped(Map<String, String> went) {
        Map<String, List<String>> byQueue = new LinkedHashMap<>();
        for (Map.Entry<String, String> entry : went.entrySet()) {
            byQueue.computeIfAbsent(entry.getValue(), q -> new ArrayList<>()).add(entry.getKey());
        }
        return byQueue;
    }
}
