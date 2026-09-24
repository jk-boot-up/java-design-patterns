package com.jk.explore.messagechannelrabbitmq;

import com.rabbitmq.client.AMQP;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.DeliverCallback;
import com.rabbitmq.client.GetResponse;
import com.rabbitmq.client.MessageProperties;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;
import java.util.function.Consumer;

/**
 * One message channel, on a real broker.
 *
 * <p>The pattern's channel is a named place messages are put into at one end and taken out of
 * at the other. On RabbitMQ that place is called a queue, and this class is the whole of the
 * pattern: a name, a way to put a message in, a way to take one out, and a way to ask how
 * many are waiting.
 *
 * <p>One warning about words. The RabbitMQ client also has a type called {@code Channel}, and
 * it means something completely different: a lightweight conversation over one network
 * connection. This project needed a name for the pattern and a name for that conversation, so
 * the pattern keeps the name {@code Channel} and the conversation is held in a field called
 * {@code amqp}.
 */
public class Channel implements AutoCloseable {

    /** What the broker hands back when a message is taken but not yet acknowledged. */
    public record Taken(PickOrder order, boolean seenBefore, long receipt) {
    }

    private final String name;
    private final Connection connection;
    private final com.rabbitmq.client.Channel amqp;

    public Channel(String name, Connection connection) {
        this.name = name;
        this.connection = connection;
        try {
            this.amqp = connection.createChannel();
        } catch (IOException e) {
            throw new IllegalStateException("could not open a conversation with the broker", e);
        }
    }

    public String name() {
        return name;
    }

    /**
     * A channel the broker writes down, so it is still there after the broker is restarted.
     * The broker's word for written down is durable.
     */
    public Channel openWrittenDown() {
        return declare(true, Map.of());
    }

    /**
     * A channel with a limit on how many messages may wait in it, and an instruction to turn
     * a sender away rather than quietly throw an older message out. The broker's words for
     * those two settings are max length and overflow.
     */
    public Channel openWithRoomFor(int messages) {
        Map<String, Object> limits = new HashMap<>();
        limits.put("x-max-length", messages);
        limits.put("x-overflow", "reject-publish");
        return declare(true, limits);
    }

    private Channel declare(boolean writtenDown, Map<String, Object> limits) {
        try {
            amqp.queueDeclare(name, writtenDown, false, false, limits);
            return this;
        } catch (IOException e) {
            throw new IllegalStateException("could not create the channel " + name, e);
        }
    }

    /**
     * Puts a message in and returns. The sender does not wait for anybody to take it out.
     * The message is marked as one the broker should write down rather than only remember.
     */
    public void send(PickOrder order) {
        publish(order, MessageProperties.PERSISTENT_TEXT_PLAIN);
    }

    /**
     * Puts a message in and asks the broker only to hold it in memory, never to write it to
     * disk. It is quicker, and it is gone if the broker stops.
     */
    public void sendWithoutWritingDown(PickOrder order) {
        publish(order, MessageProperties.TEXT_PLAIN);
    }

    private void publish(PickOrder order, AMQP.BasicProperties properties) {
        try {
            amqp.basicPublish("", name, properties, order.text().getBytes(StandardCharsets.UTF_8));
        } catch (IOException e) {
            throw new IllegalStateException("could not send to " + name, e);
        }
    }

    /**
     * Turns on the broker's receipts for this conversation, so that every later send waits to
     * hear whether the broker took the message or turned it away. RabbitMQ calls these
     * receipts publisher confirms.
     */
    public Channel askForReceipts() {
        try {
            amqp.confirmSelect();
            return this;
        } catch (IOException e) {
            throw new IllegalStateException("could not turn on receipts", e);
        }
    }

    /** Sends one message and reports whether the broker accepted it or turned it away. */
    public boolean sendAndHearBack(PickOrder order) {
        try {
            send(order);
            return amqp.waitForConfirms(10_000);
        } catch (Exception e) {
            return false;
        }
    }

    /** How many messages are waiting in this channel right now, as the broker counts them. */
    public int waiting() {
        try (com.rabbitmq.client.Channel ask = connection.createChannel()) {
            return (int) ask.messageCount(name);
        } catch (Exception e) {
            throw new IllegalStateException("could not count " + name, e);
        }
    }

    /**
     * Takes one message out but does not tell the broker it was handled. Until somebody does,
     * the broker keeps its own copy and will hand the message to somebody else if this
     * receiver disappears.
     */
    public Taken takeWithoutSayingDone() {
        try {
            GetResponse response = amqp.basicGet(name, false);
            if (response == null) {
                return null;
            }
            PickOrder order = PickOrder.read(new String(response.getBody(), StandardCharsets.UTF_8));
            return new Taken(order, response.getEnvelope().isRedeliver(), response.getEnvelope().getDeliveryTag());
        } catch (IOException e) {
            throw new IllegalStateException("could not take from " + name, e);
        }
    }

    /**
     * Tells the broker the message was handled, so it may forget it. The broker's word for
     * this is an acknowledgement.
     */
    public void sayDone(Taken taken) {
        try {
            amqp.basicAck(taken.receipt(), false);
        } catch (IOException e) {
            throw new IllegalStateException("could not acknowledge on " + name, e);
        }
    }

    /**
     * Tells the broker how many unfinished orders it may hand this receiver before it waits
     * for the receiver to say done with one. Without this there is no limit, and the broker
     * hands out everything it has at once. RabbitMQ calls this limit prefetch. It has to be
     * set before the receiver starts listening.
     */
    public Channel handAtMost(int unfinished) {
        try {
            amqp.basicQos(unfinished);
            return this;
        } catch (IOException e) {
            throw new IllegalStateException("could not set the prefetch limit on " + name, e);
        }
    }

    /**
     * Registers a receiver that is handed every message as it arrives, and that says it is
     * done with each one only after the work has finished.
     */
    public void receiveEachInto(Consumer<PickOrder> receiver) {
        DeliverCallback onMessage = (tag, delivery) -> {
            receiver.accept(PickOrder.read(new String(delivery.getBody(), StandardCharsets.UTF_8)));
            amqp.basicAck(delivery.getEnvelope().getDeliveryTag(), false);
        };
        try {
            amqp.basicConsume(name, false, onMessage, tag -> {
            });
        } catch (IOException e) {
            throw new IllegalStateException("could not listen on " + name, e);
        }
    }

    /** Ends the conversation and the connection behind it, as a process exiting would. */
    @Override
    public void close() {
        try {
            connection.close();
        } catch (Exception e) {
            // Closing twice, or closing a connection the broker already dropped, is not a failure.
        }
    }

    /**
     * Ends the connection the way a crash does: no goodbye to the broker. Anything taken but
     * not acknowledged goes back into the channel.
     */
    public void crash() {
        try {
            connection.abort(0);
        } catch (Exception e) {
            // A crash has no error path.
        }
    }
}
