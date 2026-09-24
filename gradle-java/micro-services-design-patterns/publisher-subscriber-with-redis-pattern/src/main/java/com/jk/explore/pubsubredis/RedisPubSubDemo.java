package com.jk.explore.pubsubredis;

import java.util.ArrayList;
import java.util.List;

/**
 * Six acts against a real Redis server, started and stopped by this program.
 *
 * <p>The order service has news that several other services want: an order was placed. The
 * first act calls each of them by name. The rest publish the news once through Redis and show
 * what a real server does that a topic inside one program did not: it reaches another process,
 * it tells the publisher how many heard, it keeps nothing for a latecomer, and it cuts off a
 * listener that falls too far behind.
 */
public class RedisPubSubDemo {

    /** How many orders the fifth act publishes in one go. */
    static final int ROUND = 1_000;

    /** A bound on the fifth act, so a Redis that never acts fails the run rather than hanging it. */
    static final int MAX_ROUNDS = 2_000;

    /** The limit the fifth act puts on how far one listener may fall behind. */
    static final String LIMIT = "1mb";

    public static void main(String[] args) {
        if (!RedisServer.containerRuntimeAvailable()) {
            System.out.println(RedisServer.NO_RUNTIME_ADVICE);
            return;
        }
        try (RedisServer server = new RedisServer()) {
            try {
                server.start();
            } catch (RuntimeException e) {
                System.out.println(RedisServer.WOULD_NOT_START_ADVICE);
                return;
            }
            one();
            two(server);
            three(server);
            four(server);
            five(server);
            six(server);
        }
    }

    /** The order service calls every interested service by name. */
    private static void one() {
        System.out.println("ONE. The order service calls each one.");
        DirectOrderService direct = new DirectOrderService();
        direct.placeOrder(OrderEvent.placed(1));
        System.out.println("  inventory " + direct.handledBy("inventory") + ", email " + direct.handledBy("email")
                + ", analytics " + direct.handledBy("analytics") + ".");
        System.out.println("  the order service knows " + direct.servicesKnownByName()
                + " services by name. a fourth, loyalty points, means editing it.");
    }

    /** Publish once. Redis copies the message to every listener, including one in another process. */
    private static void two(RedisServer server) {
        System.out.println("TWO. Publish once, and Redis fans it out.");
        try (OrderService orders = new OrderService(server);
             Subscriber inventory = Subscriber.listen(server, "inventory", OrderService.PLACED);
             Subscriber email = Subscriber.listen(server, "email", OrderService.PLACED);
             Subscriber analytics = Subscriber.listen(server, "analytics", OrderService.PLACED)) {
            long reached = orders.publish(OrderEvent.placed(1));
            Poll.until("all three to hear about ORD-1",
                    () -> inventory.count() == 1 && email.count() == 1 && analytics.count() == 1);
            System.out.println("  the order service published OrderPlaced ORD-1 once. Redis answered: " + reached + " receivers.");
            System.out.println("  inventory " + inventory.orders() + ", email " + email.orders()
                    + ", analytics " + analytics.orders() + ". each on a connection of its own.");

            try (SeparateProcess loyalty = new SeparateProcess(server, 1)) {
                long reachedNow = orders.publish(OrderEvent.placed(2));
                int exit = loyalty.awaitExit();
                System.out.println("  loyalty points starts as a separate Java process"
                        + ". ORD-2 is published: "
                        + reachedNow + " receivers.");
                System.out.println("  the loyalty process printed " + loyalty.ordersReceived() + " and exited with code " + exit
                        + ". the order service was not changed.");
            }
        }
    }

    /** Redis keeps nothing for a subscriber that was not listening when the message went out. */
    private static void three(RedisServer server) {
        System.out.println("THREE. A subscriber that arrives late.");
        try (OrderService orders = new OrderService(server);
             Subscriber email = Subscriber.listen(server, "email", OrderService.PLACED)) {
            List<Long> early = new ArrayList<>();
            for (int i = 1; i <= 3; i++) {
                early.add(orders.publish(OrderEvent.placed(i)));
            }
            Poll.until("email to hear all three", () -> email.count() == 3);
            System.out.println("  3 orders published while only email listened. Redis answered: " + early + ".");
            try (Subscriber loyalty = Subscriber.listen(server, "loyalty", OrderService.PLACED)) {
                long reached = orders.publish(OrderEvent.placed(4));
                Poll.until("email and loyalty to hear ORD-4", () -> email.count() == 4 && loyalty.count() == 1);
                System.out.println("  loyalty starts listening, and ORD-4 is published: " + reached + " receivers.");
                System.out.println("  email saw " + email.orders() + ". loyalty saw " + loyalty.orders() + ".");
            }
            System.out.println("  there is no reading from the start. Redis stored none of the 4 orders: keys in the database: "
                    + server.keysStored() + ".");
        }
    }

    /** A subscriber chooses by name, or by a name with a star in it. */
    private static void four(RedisServer server) {
        System.out.println("FOUR. Each takes what it wants.");
        try (OrderService orders = new OrderService(server);
             Subscriber email = Subscriber.listen(server, "email", OrderService.PLACED);
             Subscriber analytics = Subscriber.listenToPattern(server, "analytics", "orders.*")) {
            long placed = orders.publish(OrderEvent.placed(1));
            long cancelled = orders.publish(OrderEvent.cancelled(1));
            Poll.until("analytics to hear both", () -> analytics.count() == 2);
            Poll.until("email to hear the placed order", () -> email.count() == 1);
            System.out.println("  OrderPlaced ORD-1 reached " + placed + " receivers. OrderCancelled ORD-1 reached " + cancelled + ".");
            System.out.println("  email listened to orders.placed: " + email.received() + ".");
            System.out.println("  analytics listened to orders.*: " + analytics.received() + ".");
        }
    }

    /** A subscriber that stops reading is not waited for. Past a size limit, Redis cuts it off. */
    private static void five(RedisServer server) {
        System.out.println("FIVE. A subscriber that cannot keep up.");
        String shipped = server.listenerLimit();
        server.limitEachListenerTo(LIMIT);
        server.resetCounts();
        try (OrderService orders = new OrderService(server);
             Subscriber email = Subscriber.listen(server, "email", OrderService.PLACED);
             Subscriber analytics = Subscriber.listen(server, "analytics", OrderService.PLACED)) {
            analytics.stopReading();
            List<Long> reached = new ArrayList<>();
            int rounds = 0;
            while (server.listenersCutOff() == 0) {
                if (++rounds > MAX_ROUNDS) {
                    throw new IllegalStateException("Redis never cut the stalled listener off");
                }
                reached.addAll(orders.publishPlaced(reached.size() + 1, ROUND));
            }
            int published = reached.size();
            Poll.until("email to hear every order", () -> email.count() == published);
            System.out.println("  Redis keeps a pile of unsent messages for each listener, with a limit. out of the box: " + shipped + ".");
            System.out.println("  this demo lowers it to " + LIMIT + ". analytics stops reading, and orders are published in rounds of "
                    + ROUND + " until Redis acts.");
            System.out.println("  " + describePublished(published) + " later, Redis cut analytics off. listeners cut off for falling behind: "
                    + server.listenersCutOff() + ".");
            System.out.println("  the first order reached " + reached.get(0) + " receivers, the last reached "
                    + reached.get(published - 1) + ". email kept up and received " + (email.count() == published ? "every one" : "some")
                    + ".");
            analytics.startReading();
            Poll.until("analytics to reach the end of what it was sent", analytics::finished);
            System.out.println("  analytics started reading again and got " + describe(analytics.count(), published)
                    + ", then its connection ended.");
            System.out.println("  the publisher was never slowed down, and never told. the orders analytics missed are gone.");
            if (System.getenv("PUBSUB_DEBUG") != null) {
                System.out.println("  [debug] published " + published + ", analytics got " + analytics.count());
            }
        }
    }

    static String describePublished(int published) {
        return published > 10_000 ? "more than 10,000 orders" : "fewer than 10,000 orders";
    }

    static String describe(int got, int published) {
        if (got == 0) {
            return "none of them";
        }
        if (got < published) {
            return "some of them, not all";
        }
        return "all of them";
    }

    /** The bill. */
    private static void six(RedisServer server) {
        System.out.println("SIX. The bill.");
        try (OrderService orders = new OrderService(server)) {
            long reached = orders.publish(OrderEvent.placed(1));
            try (Subscriber email = Subscriber.listen(server, "email", OrderService.PLACED)) {
                System.out.println("  email was down when ORD-1 was placed. Redis told the order service: " + reached + " receivers.");
                System.out.println("  email came back and got: " + email.orders() + ". there is nothing to catch up from.");
            }
        }
        System.out.println("  the count says how many connections were listening. not which ones, and not whether any finished the work.");
        System.out.println("  and Redis is a separate program to run and watch: this demo needed 1 container and 2 Java processes.");
    }
}
