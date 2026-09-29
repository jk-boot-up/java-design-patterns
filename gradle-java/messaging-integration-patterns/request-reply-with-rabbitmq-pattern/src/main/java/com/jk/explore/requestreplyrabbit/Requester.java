package com.jk.explore.requestreplyrabbit;

import com.rabbitmq.client.AMQP;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;

/**
 * A caller of the inventory service: sends requests with a return address and a correlation ID, and
 * matches each reply to its request by that ID.
 */
public final class Requester implements AutoCloseable {

    /** RabbitMQ's built-in pseudo-queue for replies: no reply queue has to be declared at all. */
    public static final String DIRECT_REPLY_TO = "amq.rabbitmq.reply-to";

    private final Connection connection;
    private final Channel channel;
    private final String replyTo;
    private final Map<String, String> replies = new ConcurrentHashMap<>();
    private final Map<String, String> waiting = new ConcurrentHashMap<>();
    private final List<String> arrivals = new CopyOnWriteArrayList<>();

    /** With {@code direct}, uses direct reply-to; otherwise its own exclusive, server-named queue. */
    public Requester(Broker broker, boolean direct) throws Exception {
        connection = broker.connect();
        channel = connection.createChannel();
        replyTo = direct ? DIRECT_REPLY_TO : channel.queueDeclare().getQueue();
        channel.basicConsume(replyTo, true, (tag, d) -> {
            String body = new String(d.getBody(), StandardCharsets.UTF_8);
            arrivals.add(body);
            String id = d.getProperties().getCorrelationId();
            if (id != null) {
                replies.put(id, body);
                waiting.remove(id);
            }
        }, tag -> { });
    }

    /** Sends a request. {@code expiresMillis} above 0 lets the broker drop it if nobody takes it in time. */
    public void send(String id, String request, long expiresMillis) throws Exception {
        AMQP.BasicProperties.Builder props = new AMQP.BasicProperties.Builder().replyTo(replyTo);
        if (id != null) {
            props.correlationId(id);
            waiting.put(id, request);
        }
        if (expiresMillis > 0) {
            props.expiration(Long.toString(expiresMillis));
        }
        channel.basicPublish("", InventoryService.QUEUE, props.build(), request.getBytes(StandardCharsets.UTF_8));
    }

    public List<String> arrivals() {
        return arrivals;
    }

    public String reply(String id) {
        return replies.get(id);
    }

    public int waitingCount() {
        return waiting.size();
    }

    /** Waits for a reply to {@code id}, up to a limit. Returns null if none came. */
    public String await(String id, long timeoutMillis) throws InterruptedException {
        long deadline = System.currentTimeMillis() + timeoutMillis;
        while (!replies.containsKey(id) && System.currentTimeMillis() < deadline) {
            Thread.sleep(10);
        }
        return replies.get(id);
    }

    public String replyTo() {
        return replyTo;
    }

    public void forget(String id) {
        waiting.remove(id);
    }

    public List<String> ids(int n, String prefix) {
        List<String> out = new ArrayList<>();
        for (int i = 1; i <= n; i++) {
            out.add(prefix + i);
        }
        return out;
    }

    @Override
    public void close() throws Exception {
        connection.close();
    }
}
