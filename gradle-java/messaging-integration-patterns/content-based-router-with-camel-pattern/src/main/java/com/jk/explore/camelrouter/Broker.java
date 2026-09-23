package com.jk.explore.camelrouter;

import com.rabbitmq.client.BuiltinExchangeType;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.GetResponse;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.function.BooleanSupplier;
import org.testcontainers.rabbitmq.RabbitMQContainer;
import org.testcontainers.utility.DockerImageName;

/**
 * A real RabbitMQ broker, running in a container that this demo starts and removes again.
 *
 * <p>Three words are used throughout and are worth saying in plain language first. A <em>queue</em> is a
 * named line that messages wait in until somebody takes them. An <em>exchange</em> is the post box a
 * sender drops a message into; it never keeps anything, it only hands the message on. A
 * <em>routing key</em> is the short label written on the message when it is posted, and the broker uses
 * it to decide which queue the message is put in. This demo uses one exchange, called shop, and every
 * queue is reached by a routing key that is simply the queue's own name.
 */
public class Broker implements AutoCloseable {

    /** The broker image. Pinned, so that two runs on two machines are the same broker. */
    public static final String IMAGE = "rabbitmq:4.3.6-alpine";

    /** The one exchange this shop posts through. */
    public static final String EXCHANGE = "shop";

    /** Where orders arrive, and where the router reads from. */
    public static final String ORDERS = "orders";

    /** The queues the router can choose between, plus the two that catch what goes wrong. */
    public static final List<String> DESTINATIONS = List.of(
            "express-shipping",
            "standard-shipping",
            "digital-delivery",
            "fraud-review",
            "manual-review",
            "eu-vat-check",
            "unclaimed",
            "router-errors",
            "warehouse-inbox");

    private RabbitMQContainer container;
    private Connection connection;

    /** True when a container runtime is up and can be talked to. */
    public static boolean dockerAvailable() {
        try {
            return org.testcontainers.DockerClientFactory.instance().isDockerAvailable();
        } catch (RuntimeException | LinkageError e) {
            return false;
        }
    }

    /** Starts the broker and declares the exchange and every queue. */
    public void start() {
        container = new RabbitMQContainer(DockerImageName.parse(IMAGE).asCompatibleSubstituteFor("rabbitmq"));
        container.start();
        ConnectionFactory factory = connectionFactory();
        try {
            connection = factory.newConnection("content-based-router-demo");
        } catch (Exception e) {
            throw new IllegalStateException("could not connect to the broker that was just started", e);
        }
        declare();
    }

    /** A factory pointed at the running container. Camel is handed one of these too. */
    public ConnectionFactory connectionFactory() {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost(container.getHost());
        factory.setPort(container.getAmqpPort());
        factory.setUsername(container.getAdminUsername());
        factory.setPassword(container.getAdminPassword());
        return factory;
    }

    private void declare() {
        withChannel(channel -> {
            channel.exchangeDeclare(EXCHANGE, BuiltinExchangeType.DIRECT, true);
            List<String> all = new ArrayList<>(DESTINATIONS);
            all.add(ORDERS);
            for (String queue : all) {
                channel.queueDeclare(queue, true, false, false, null);
                channel.queueBind(queue, EXCHANGE, queue);
            }
            return null;
        });
    }

    /** Empties every queue, so that each act starts from nothing. */
    public void clear() {
        withChannel(channel -> {
            channel.queuePurge(ORDERS);
            for (String queue : DESTINATIONS) {
                channel.queuePurge(queue);
            }
            return null;
        });
    }

    /** Posts an order to the exchange with the given routing key, which lands it on that queue. */
    public void post(String routingKey, Order order) {
        post(routingKey, order.body());
    }

    /** Posts a raw body, for the act where the sender has changed the wording of a field. */
    public void post(String routingKey, String body) {
        withChannel(channel -> {
            channel.basicPublish(EXCHANGE, routingKey, null, body.getBytes(StandardCharsets.UTF_8));
            return null;
        });
    }

    /** How many messages are sitting on a queue right now, as the broker counts them. */
    public int waiting(String queue) {
        return withChannel(channel -> (int) channel.messageCount(queue));
    }

    /** How many messages are sitting on the queues the router can send to, added up. */
    public int waitingOnDestinations() {
        int total = 0;
        for (String queue : DESTINATIONS) {
            total += waiting(queue);
        }
        return total;
    }

    /** How many messages are sitting anywhere in the shop, the orders queue included. */
    public int waitingEverywhere() {
        return waiting(ORDERS) + waitingOnDestinations();
    }

    /** Takes everything off a queue and returns the orders that were on it, oldest first. */
    public List<Order> take(String queue) {
        List<Order> taken = new ArrayList<>();
        for (String body : takeBodies(queue)) {
            taken.add(Order.parse(body));
        }
        return taken;
    }

    /** Takes everything off a queue and returns the raw bodies. */
    public List<String> takeBodies(String queue) {
        return withChannel(channel -> {
            List<String> bodies = new ArrayList<>();
            GetResponse got;
            while ((got = channel.basicGet(queue, true)) != null) {
                bodies.add(new String(got.getBody(), StandardCharsets.UTF_8));
            }
            return bodies;
        });
    }

    /**
     * Waits until the orders queue is empty and the destination queues hold the number of messages
     * expected between them, and then keeps checking for a moment longer so that a message still on its
     * way would be noticed. There is no fixed pause standing in for the work: the loop asks the broker how
     * many messages it is holding, and gives up with an error rather than hanging for ever.
     */
    public void settleRouted(int expected) {
        BooleanSupplier reached = () -> waiting(ORDERS) == 0 && waitingOnDestinations() == expected;
        String what = "the orders queue to empty and " + expected + " message(s) to arrive at their destinations";
        holdUntilSteady(reached, what);
    }

    /** Waits until one queue is holding exactly this many messages, and stays there. */
    public void settleQueue(String queue, int expected) {
        holdUntilSteady(() -> waiting(queue) == expected, expected + " message(s) on " + queue);
    }

    private void holdUntilSteady(BooleanSupplier reached, String what) {
        waitUntil(reached, what);
        long end = System.nanoTime() + Duration.ofMillis(500).toNanos();
        while (System.nanoTime() < end) {
            if (!reached.getAsBoolean()) {
                waitUntil(reached, what);
                end = System.nanoTime() + Duration.ofMillis(500).toNanos();
            }
            pause();
        }
    }

    /** Polls the condition until it is true, or fails with a sentence saying what was being waited for. */
    public static void waitUntil(BooleanSupplier condition, String what) {
        long end = System.nanoTime() + Duration.ofSeconds(60).toNanos();
        while (System.nanoTime() < end) {
            if (condition.getAsBoolean()) {
                return;
            }
            pause();
        }
        throw new IllegalStateException("gave up after 60 seconds: " + what);
    }

    private static void pause() {
        try {
            Thread.sleep(25);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException("interrupted while waiting for the broker");
        }
    }

    private <T> T withChannel(ChannelWork<T> work) {
        try (Channel channel = connection.createChannel()) {
            return work.apply(channel);
        } catch (Exception e) {
            throw new IllegalStateException("the broker refused the request", e);
        }
    }

    @FunctionalInterface
    private interface ChannelWork<T> {
        T apply(Channel channel) throws Exception;
    }

    @Override
    public void close() {
        if (connection != null) {
            try {
                connection.close();
            } catch (Exception e) {
                // The container is going away next, so a connection that is already gone is not a problem.
            }
        }
        if (container != null) {
            container.stop();
        }
    }
}
