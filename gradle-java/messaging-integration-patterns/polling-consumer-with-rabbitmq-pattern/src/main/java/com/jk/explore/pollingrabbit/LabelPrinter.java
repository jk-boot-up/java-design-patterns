package com.jk.explore.pollingrabbit;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.GetResponse;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * The warehouse label printer, as a RabbitMQ consumer. It can be pushed to, or it can poll.
 */
public final class LabelPrinter implements AutoCloseable {

    private final Connection connection;
    private final Channel channel;
    private final List<Long> inHand = new CopyOnWriteArrayList<>();
    private final AtomicInteger printed = new AtomicInteger();
    private int polls;
    private int emptyPolls;

    public LabelPrinter(Broker broker) throws Exception {
        connection = broker.connect();
        channel = connection.createChannel();
        channel.queueDeclare(Orders.QUEUE, true, false, false, null);
    }

    /** Push: the broker sends messages as fast as it can; {@code prefetch} 0 means no limit. */
    public void subscribe(int prefetch) throws Exception {
        channel.basicQos(prefetch);
        channel.basicConsume(Orders.QUEUE, false, (tag, d) -> inHand.add(d.getEnvelope().getDeliveryTag()), tag -> { });
    }

    /** Prints and acknowledges everything in hand. */
    public void printInHand() throws Exception {
        for (Long tag : inHand) {
            channel.basicAck(tag, false);
            printed.incrementAndGet();
        }
        inHand.clear();
    }

    /** Poll: ask for up to {@code max} orders now, print and acknowledge each. */
    public int poll(int max) throws Exception {
        int took = 0;
        for (int i = 0; i < max; i++) {
            polls++;
            GetResponse r = channel.basicGet(Orders.QUEUE, false);
            if (r == null) {
                emptyPolls++;
                break;
            }
            channel.basicAck(r.getEnvelope().getDeliveryTag(), false);
            printed.incrementAndGet();
            took++;
        }
        return took;
    }

    public int inHand() {
        return inHand.size();
    }

    public int printed() {
        return printed.get();
    }

    public int polls() {
        return polls;
    }

    public int emptyPolls() {
        return emptyPolls;
    }

    @Override
    public void close() throws Exception {
        connection.abort();
    }
}
