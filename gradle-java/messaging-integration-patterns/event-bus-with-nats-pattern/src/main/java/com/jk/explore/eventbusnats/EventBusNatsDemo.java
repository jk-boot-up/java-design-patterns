package com.jk.explore.eventbusnats;

import java.util.Collections;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

/**
 * Six acts, against a real NATS server in a container.
 *
 * <p>The store publishes what happened. Other services listen for what they care about. Nobody holds a
 * reference to anybody. The last two acts are the price of that.
 */
public class EventBusNatsDemo {

    static final String ORDER_PLACED = "store.orders.placed";
    static final String ORDER_CANCELLED = "store.orders.cancelled";
    static final String PAYMENT_TAKEN = "store.payments.taken";
    static final String STOCK_LOW = "store.stock.low";
    static final String ALL_ORDER_EVENTS = "store.orders.*";
    static final String EVERYTHING = "store.>";

    public static void main(String[] args) throws Exception {
        quietLogging();
        if (!NatsServer.containerRuntimeAvailable()) {
            System.out.println("This demo needs a container runtime, such as Docker Desktop or Colima, running on this machine. Start it, then run this again.");
            return;
        }
        try (NatsServer server = new NatsServer()) {
            server.start();
            one();
            two(server);
            three(server);
            four(server);
            five(server);
            six(server);
        }
    }

    private static void one() {
        System.out.println("ONE. Everyone knows everyone.");
        DirectStore store = new DirectStore(5);
        System.out.println("  " + 5 + " services that each tell the other four when an order is placed: " + store.wires() + " wires between them, and every wire is an address that can be wrong or down.");
        System.out.println("  add a sixth service and it needs " + store.wiresForOneMoreService() + " more.");
    }

    private static void two(NatsServer server) throws Exception {
        System.out.println("TWO. Everyone knows the bus.");
        try (StoreBus checkout = new StoreBus("checkout", server.url());
             StoreBus email = new StoreBus("email", server.url());
             StoreBus warehouse = new StoreBus("warehouse", server.url());
             StoreBus analytics = new StoreBus("analytics", server.url())) {
            StoreSubscriber emailListener = email.subscribe("email", ORDER_PLACED);
            StoreSubscriber warehouseListener = warehouse.subscribe("warehouse", ORDER_PLACED);
            StoreSubscriber analyticsListener = analytics.subscribe("analytics", ORDER_PLACED);

            checkout.publish(ORDER_PLACED, "OrderPlaced ORD-1");
            checkout.settle();

            emailListener.waitForNext();
            warehouseListener.waitForNext();
            analyticsListener.waitForNext();

            System.out.println("  checkout published OrderPlaced ORD-1 under the name " + ORDER_PLACED + " and returned. it was told nothing about who was listening.");
            System.out.println("  " + List.of(emailListener.heard().get(0), warehouseListener.heard().get(0), analyticsListener.heard().get(0)) + ".");
            System.out.println("  " + new DirectStore(5).wiresThroughABus() + " services, each with 1 connection to the bus: " + new DirectStore(5).wiresThroughABus() + " wires, not " + new DirectStore(5).wires() + ".");
        }
    }

    private static void three(NatsServer server) throws Exception {
        System.out.println("THREE. By name.");
        try (StoreBus checkout = new StoreBus("checkout", server.url());
             StoreBus email = new StoreBus("email", server.url());
             StoreBus warehouse = new StoreBus("warehouse", server.url());
             StoreBus analytics = new StoreBus("analytics", server.url())) {
            StoreSubscriber justPlaced = email.subscribe("email", ORDER_PLACED);
            StoreSubscriber anyOrderEvent = warehouse.subscribe("warehouse", ALL_ORDER_EVENTS);
            StoreSubscriber everything = analytics.subscribe("analytics", EVERYTHING);

            checkout.publish(ORDER_PLACED, "OrderPlaced ORD-1");
            checkout.publish(ORDER_CANCELLED, "OrderCancelled ORD-1");
            checkout.publish(PAYMENT_TAKEN, "PaymentTaken ORD-1");
            checkout.publish(STOCK_LOW, "StockLow SKU-42");
            checkout.settle();

            justPlaced.waitFor(1);
            anyOrderEvent.waitFor(2);
            everything.waitFor(4);

            System.out.println("  checkout published four events: an order placed, that order cancelled, a payment taken, and stock running low.");
            System.out.println("  a listener for " + ORDER_PLACED + " received " + justPlaced.received() + ": " + justPlaced.events() + ".");
            System.out.println("  a listener for " + ALL_ORDER_EVENTS + ", where the star stands for one word, received " + anyOrderEvent.received() + ": " + anyOrderEvent.events() + ".");
            System.out.println("  a listener for " + EVERYTHING + ", where the arrow stands for the rest of the name, received " + everything.received() + ": " + everything.events() + ".");
        }
    }

    private static void four(NatsServer server) throws Exception {
        System.out.println("FOUR. One failing subscriber.");
        try (StoreBus checkout = new StoreBus("checkout", server.url());
             StoreBus email = new StoreBus("email", server.url());
             StoreBus warehouse = new StoreBus("warehouse", server.url())) {
            List<String> reserved = Collections.synchronizedList(new java.util.ArrayList<>());
            List<String> failures = Collections.synchronizedList(new java.util.ArrayList<>());
            CountDownLatch emailTried = new CountDownLatch(1);
            CountDownLatch warehouseDone = new CountDownLatch(1);

            email.onEvent(ORDER_PLACED, event -> {
                try {
                    throw new IllegalStateException("mail server timed out");
                } catch (RuntimeException e) {
                    failures.add(event + ": " + e.getMessage());
                    emailTried.countDown();
                    throw e;
                }
            });
            warehouse.onEvent(ORDER_PLACED, event -> {
                reserved.add("warehouse reserved " + event.substring(event.indexOf(' ') + 1));
                warehouseDone.countDown();
            });

            checkout.publish(ORDER_PLACED, "OrderPlaced ORD-1");
            checkout.settle();

            await(emailTried, "the email service to react");
            await(warehouseDone, "the warehouse to react");

            System.out.println("  email's handler threw. recorded: " + failures + ".");
            System.out.println("  the warehouse, on a connection of its own, still reacted: " + reserved + ".");
            System.out.println("  checkout was never told. publishing had already returned before either of them ran.");
        }
    }

    private static void five(NatsServer server) throws Exception {
        System.out.println("FIVE. An event nobody hears.");
        try (StoreBus checkout = new StoreBus("checkout", server.url());
             StoreBus warehouse = new StoreBus("warehouse", server.url())) {
            checkout.publish(ORDER_PLACED, "OrderPlaced ORD-1");
            checkout.settle();
            System.out.println("  nobody was listening. checkout published OrderPlaced ORD-1 and the bus dropped it: no error, no record, and nowhere to read it back from.");

            StoreSubscriber late = warehouse.subscribe("warehouse", ORDER_PLACED);
            checkout.publish(ORDER_PLACED, "OrderPlaced ORD-2");
            checkout.settle();

            String first = late.waitForNext();
            System.out.println("  the warehouse then started listening, and checkout published OrderPlaced ORD-2.");
            System.out.println("  the first event the warehouse ever received was " + first + ". this bus delivers a name in order, so ORD-1 was never coming.");
            System.out.println("  2 orders published, " + late.received() + " received.");

            System.out.println("  telling this bus is never confirmed. asking is: a request on " + ORDER_CANCELLED + " with nobody listening came back at once with " + checkout.ask(ORDER_CANCELLED, "did anybody hear that?") + ".");
        }
    }

    private static void six(NatsServer server) throws Exception {
        System.out.println("SIX. The bill.");
        ServerView view = new ServerView(server.monitorUrl(), "store.");
        view.waitUntilStoreListeners(n -> n == 0);
        try (StoreBus email = new StoreBus("email", server.url());
             StoreBus warehouse = new StoreBus("warehouse", server.url());
             StoreBus analytics = new StoreBus("analytics", server.url())) {
            email.subscribe("email", ORDER_PLACED);
            warehouse.subscribe("warehouse", ALL_ORDER_EVENTS);
            StoreSubscriber analyticsListener = analytics.subscribe("analytics", EVERYTHING);

            System.out.println("  who reacts to an order being placed? nothing in checkout says, and checkout cannot find out. only the server knows, and it has to be asked on a second port: " + view.storeListeners() + " listeners for store events.");

            analyticsListener.stopListening();
            analytics.settle();
            System.out.println("  analytics stopped listening but left its connection open: " + view.waitUntilStoreListeners(n -> n == 2) + " listeners.");
        }
        System.out.println("  after the three services closed their connections: " + view.waitUntilStoreListeners(n -> n == 0) + " listeners. a connection closing takes every listener on it with it.");
        System.out.println("  and the bus is now a program of its own to run and to watch: this demo needed 1 container.");
        System.out.println("  and it keeps nothing. a subscriber that is down when an event is published has missed it for good.");
    }

    /**
     * The container library narrates what it is doing, and so does the client. None of that is the lesson,
     * so it is turned down to leave the six acts on their own. It also keeps the message printed when there
     * is no container runtime from being buried under a page of logging.
     */
    static void quietLogging() {
        System.setProperty("org.slf4j.simpleLogger.defaultLogLevel", "error");
        System.setProperty("org.slf4j.simpleLogger.log.org.testcontainers", "off");
        System.setProperty("org.slf4j.simpleLogger.log.tc", "off");
        System.setProperty("org.slf4j.simpleLogger.log.com.github.dockerjava", "off");
    }

    private static void await(CountDownLatch latch, String what) throws InterruptedException {
        if (!latch.await(20, TimeUnit.SECONDS)) {
            throw new IllegalStateException("waited 20 seconds for " + what + " and it did not happen");
        }
    }
}
