package com.jk.explore.competingconsumersrabbitmq;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.MessageProperties;
import java.io.IOException;
import java.nio.charset.StandardCharsets;

/**
 * The one queue of pick orders that every picker shares, as checkout sees it.
 *
 * <p>Checkout puts orders in and can ask the broker two questions: how many orders are waiting
 * to be handed to somebody, and how many pickers are listening. Neither answer is kept by this
 * program; both are asked of the broker every time.
 */
public class OrderQueue implements AutoCloseable {

    private final String name;
    private final Connection connection;
    private final Channel amqp;

    public OrderQueue(Broker broker, String name) {
        this.name = name;
        this.connection = broker.connect();
        try {
            this.amqp = connection.createChannel();
            // Written down, so a broker restart would keep it. Not exclusive to this
            // connection, and not deleted when the last picker leaves.
            amqp.queueDeclare(name, true, false, false, null);
        } catch (IOException e) {
            throw new IllegalStateException("could not create the queue " + name, e);
        }
    }

    public String name() {
        return name;
    }

    public void send(PickOrder order) {
        try {
            amqp.basicPublish("", name, MessageProperties.PERSISTENT_TEXT_PLAIN,
                    order.text().getBytes(StandardCharsets.UTF_8));
        } catch (IOException e) {
            throw new IllegalStateException("could not send to " + name, e);
        }
    }

    /** Sends ORD-first to ORD-last, in that order. */
    public void sendOrders(int first, int last) {
        for (int n = first; n <= last; n++) {
            send(PickOrder.of(n));
        }
    }

    /**
     * How many orders are waiting to be handed to a picker, as the broker counts them. An order
     * already handed to a picker, and not yet said done, is not waiting: it is held.
     */
    public int waiting() {
        try (Channel ask = connection.createChannel()) {
            return (int) ask.messageCount(name);
        } catch (Exception e) {
            throw new IllegalStateException("could not count " + name, e);
        }
    }

    /** How many pickers the broker believes are listening on this queue right now. */
    public int pickersListening() {
        try (Channel ask = connection.createChannel()) {
            return (int) ask.consumerCount(name);
        } catch (Exception e) {
            throw new IllegalStateException("could not count the pickers on " + name, e);
        }
    }

    @Override
    public void close() {
        try {
            connection.close();
        } catch (Exception e) {
            // Closing a connection twice is not a failure.
        }
    }
}
