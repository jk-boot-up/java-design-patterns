package com.jk.explore.deadletterrabbit;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.MessageProperties;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

/**
 * The shop's side of the broker. It declares the queues orders wait in, declares the one exchange that
 * parked orders are sent to, and publishes orders. It never moves an order aside itself: the rules it
 * writes on a queue are what the broker acts on later.
 */
public class OrderChannel implements AutoCloseable {

    /** The exchange every parked order is delivered to. In RabbitMQ's words, the dead letter exchange. */
    public static final String PARKED_EXCHANGE = "orders.parked";

    private final Channel channel;
    private int queuesDeclared;
    private int exchangesDeclared;

    public OrderChannel(Connection connection) throws IOException {
        this.channel = connection.createChannel();
        channel.exchangeDeclare(PARKED_EXCHANGE, "direct", true);
        exchangesDeclared++;
    }

    /** A working queue with no rule at all. An order the worker cannot handle has nowhere else to go. */
    public void workingQueue(String name) throws IOException {
        channel.queueDeclare(name, true, false, false, null);
        queuesDeclared++;
    }

    /** A working queue that names where the broker should send an order that dies in it. */
    public void workingQueueWithParking(String name, String parkedKey) throws IOException {
        channel.queueDeclare(name, true, false, false, parking(parkedKey));
        queuesDeclared++;
    }

    /** A working queue where an order that is not read within the time limit dies of old age. */
    public void workingQueueWithTimeLimit(String name, String parkedKey, int milliseconds) throws IOException {
        Map<String, Object> rules = parking(parkedKey);
        rules.put("x-message-ttl", milliseconds);
        channel.queueDeclare(name, true, false, false, rules);
        queuesDeclared++;
    }

    /** A working queue that holds only so many orders. When it is full the oldest one is pushed out. */
    public void workingQueueWithSizeLimit(String name, String parkedKey, int howMany) throws IOException {
        Map<String, Object> rules = parking(parkedKey);
        rules.put("x-max-length", howMany);
        channel.queueDeclare(name, true, false, false, rules);
        queuesDeclared++;
    }

    /** The queue parked orders land in, tied to the parked exchange by a key. */
    public void parkedQueue(String name, String parkedKey) throws IOException {
        channel.queueDeclare(name, true, false, false, null);
        channel.queueBind(name, PARKED_EXCHANGE, parkedKey);
        queuesDeclared++;
    }

    public void publish(String queue, Order order) throws IOException {
        channel.basicPublish("", queue, MessageProperties.PERSISTENT_TEXT_PLAIN, order.bytes());
    }

    /** How many orders are sitting in a queue waiting to be read. */
    public int waiting(String queue) {
        try {
            return channel.queueDeclarePassive(queue).getMessageCount();
        } catch (IOException e) {
            throw new IllegalStateException("cannot read the depth of " + queue, e);
        }
    }

    public int queuesDeclared() {
        return queuesDeclared;
    }

    public int exchangesDeclared() {
        return exchangesDeclared;
    }

    public Channel raw() {
        return channel;
    }

    private static Map<String, Object> parking(String parkedKey) {
        Map<String, Object> rules = new HashMap<>();
        rules.put("x-dead-letter-exchange", PARKED_EXCHANGE);
        rules.put("x-dead-letter-routing-key", parkedKey);
        return rules;
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
