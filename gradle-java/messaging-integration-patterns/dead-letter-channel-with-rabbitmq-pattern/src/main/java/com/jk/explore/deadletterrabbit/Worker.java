package com.jk.explore.deadletterrabbit;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.GetResponse;
import java.io.IOException;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Consumer;

/**
 * Asks the queue for one order at a time and hands it to shipping.
 *
 * <p>When the order goes through, the worker tells the broker it is done with it. When it fails, the worker
 * either asks for it back, which returns it to the head of the queue, or refuses it for good. Refusing it for
 * good is the only decision the worker makes: what happens to the order next is the broker's to decide,
 * from the rules written on the queue.
 *
 * <p>RabbitMQ does not count how many times a classic queue has handed the same order back, so the worker
 * keeps its own tally.
 */
public class Worker implements AutoCloseable {

    private final Channel channel;
    private final String queue;
    private final Consumer<Order> shipping;
    private final int deliveriesAllowed;

    private final List<String> handled = new ArrayList<>();
    private final Map<String, Integer> deliveries = new LinkedHashMap<>();
    private int totalDeliveries;
    private String lastError = "";

    private Worker(Connection connection, String queue, Consumer<Order> shipping, int deliveriesAllowed) throws IOException {
        this.channel = connection.createChannel();
        this.queue = queue;
        this.shipping = shipping;
        this.deliveriesAllowed = deliveriesAllowed;
    }

    /** A worker that always asks for a failed order back, however many times it has already failed. */
    public static Worker neverGivingUp(Connection connection, String queue, Consumer<Order> shipping) throws IOException {
        return new Worker(connection, queue, shipping, Integer.MAX_VALUE);
    }

    /** A worker that asks for a failed order back until it has had that many deliveries, then refuses it for good. */
    public static Worker givingUpAfter(int deliveries, Connection connection, String queue, Consumer<Order> shipping) throws IOException {
        return new Worker(connection, queue, shipping, deliveries);
    }

    /** Works through the queue, stopping when it is empty or when it has taken this many orders. */
    public void work(int atMost) throws IOException {
        for (int i = 0; i < atMost; i++) {
            GetResponse got = channel.basicGet(queue, false);
            if (got == null) {
                return;
            }
            Order order = Order.fromBody(got.getBody());
            totalDeliveries++;
            int timesSeen = deliveries.merge(order.id(), 1, Integer::sum);
            long tag = got.getEnvelope().getDeliveryTag();
            try {
                shipping.accept(order);
                channel.basicAck(tag, false);
                handled.add(order.id());
            } catch (RuntimeException e) {
                lastError = e.getMessage();
                channel.basicReject(tag, timesSeen < deliveriesAllowed);
            }
        }
    }

    public List<String> handled() {
        return handled;
    }

    public int deliveriesOf(String orderId) {
        return deliveries.getOrDefault(orderId, 0);
    }

    public int totalDeliveries() {
        return totalDeliveries;
    }

    public String lastError() {
        return lastError;
    }

    @Override
    public void close() throws IOException {
        try {
            channel.close();
        } catch (Exception e) {
            throw new IOException(e);
        }
    }
}
