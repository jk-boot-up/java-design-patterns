package com.jk.explore.priorityrabbit;

import com.rabbitmq.client.AMQP;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.GetResponse;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CopyOnWriteArrayList;

/**
 * Order queues on the real broker, and pickers who take ten orders a minute.
 */
public final class Warehouse implements AutoCloseable {

    public static final int SAME_DAY = 9;
    public static final int STANDARD = 1;

    private final Broker broker;
    private final Connection connection;
    private final Channel channel;

    public Warehouse(Broker broker) throws Exception {
        this.broker = broker;
        this.connection = broker.connect();
        this.channel = connection.createChannel();
    }

    /** A plain first-in-first-out queue, or a priority queue with priorities 0 to 10. */
    public void declare(String queue, boolean priority) throws Exception {
        channel.queueDelete(queue);
        Map<String, Object> args = priority ? Map.of("x-max-priority", 10) : null;
        channel.queueDeclare(queue, true, false, false, args);
    }

    public void place(String queue, String prefix, int count, int priority) throws Exception {
        for (int i = 1; i <= count; i++) {
            AMQP.BasicProperties props = new AMQP.BasicProperties.Builder().priority(priority).deliveryMode(2).build();
            channel.basicPublish("", queue, props, (prefix + "-" + i).getBytes(StandardCharsets.UTF_8));
        }
    }

    public void settle(String queue, int expected) {
        Poll.until(expected + " orders on " + queue, () -> broker.waiting(queue) == expected);
    }

    /** One minute of picking: take up to {@code n} orders from the queue. */
    public List<String> pickMinute(String queue, int n) throws Exception {
        List<String> picked = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            GetResponse r = channel.basicGet(queue, true);
            if (r == null) {
                break;
            }
            picked.add(new String(r.getBody(), StandardCharsets.UTF_8));
        }
        return picked;
    }

    /** The minute (1 = 9:01, the first minute) in which the last order with {@code prefix} is picked. */
    public int minuteLastPicked(String queue, String prefix, int count, int perMinute) throws Exception {
        int seen = 0;
        for (int minute = 1; minute <= 500; minute++) {
            for (String o : pickMinute(queue, perMinute)) {
                if (o.startsWith(prefix + "-")) {
                    seen++;
                }
            }
            if (seen == count) {
                return minute;
            }
        }
        return -1;
    }

    /**
     * A picker's handheld that the broker pushes orders to. With no prefetch limit, every order waiting is
     * pushed into it at once.
     */
    public List<String> subscribe(String queue, int prefetch) throws Exception {
        List<String> handheld = new CopyOnWriteArrayList<>();
        Channel c = connection.createChannel();
        c.basicQos(prefetch);
        c.basicConsume(queue, false, (tag, d) -> handheld.add(new String(d.getBody(), StandardCharsets.UTF_8)), tag -> { });
        return handheld;
    }

    @Override
    public void close() throws Exception {
        connection.abort();
    }
}
