package com.jk.explore.deadletterrabbit;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.GetResponse;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * The parked queue, read the way an operator reads it.
 *
 * <p>Every order the broker parks arrives with a note attached, written by the broker. The note says which
 * queue the order died in, how many times it has died, and the broker's one-word reason. Those words are
 * rejected, when a worker refused it for good; expired, when it sat past its time limit; and maxlen,
 * when the queue was full and the oldest order was pushed out.
 */
public class ParkedOrders implements AutoCloseable {

    private static final String BROKERS_NOTE = "x-death";

    private final Channel channel;
    private final String queue;

    public ParkedOrders(Connection connection, String queue) throws IOException {
        this.channel = connection.createChannel();
        this.queue = queue;
    }

    public int waiting() {
        try {
            return channel.queueDeclarePassive(queue).getMessageCount();
        } catch (IOException e) {
            throw new IllegalStateException("cannot read the depth of " + queue, e);
        }
    }

    /** Takes every parked order off the queue, with the broker's note read out of its headers. */
    public List<DeadLetter> takeAll() throws IOException {
        List<DeadLetter> parked = new ArrayList<>();
        while (true) {
            GetResponse got = channel.basicGet(queue, false);
            if (got == null) {
                return parked;
            }
            Order order = Order.fromBody(got.getBody());
            Map<String, Object> note = firstNote(got);
            parked.add(new DeadLetter(
                    order.id(),
                    order.body(),
                    text(note.get("reason")),
                    text(note.get("queue")),
                    ((Number) note.getOrDefault("count", 0L)).longValue()));
            channel.basicAck(got.getEnvelope().getDeliveryTag(), false);
        }
    }

    /** Puts every parked order back on a working queue, as an operator does once the cause is fixed. */
    public int replayTo(OrderChannel orders, String workingQueue) throws IOException {
        List<DeadLetter> parked = takeAll();
        for (DeadLetter letter : parked) {
            orders.publish(workingQueue, new Order(letter.id(), letter.body()));
        }
        return parked.size();
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> firstNote(GetResponse got) {
        Map<String, Object> headers = got.getProps().getHeaders();
        if (headers == null || !(headers.get(BROKERS_NOTE) instanceof List<?> deaths) || deaths.isEmpty()) {
            return Map.of();
        }
        return (Map<String, Object>) deaths.get(0);
    }

    private static String text(Object value) {
        return value == null ? "none" : value.toString();
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
