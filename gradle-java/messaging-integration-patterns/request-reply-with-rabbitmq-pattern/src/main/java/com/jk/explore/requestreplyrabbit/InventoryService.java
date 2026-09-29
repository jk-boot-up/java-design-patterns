package com.jk.explore.requestreplyrabbit;

import com.rabbitmq.client.AMQP;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.GetResponse;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * The inventory service: reads reservation requests from its queue and replies to whatever address
 * each request names, copying the request's correlation ID. Items it keeps in a local cache are
 * answered first, so replies can come back in a different order from the requests.
 */
public final class InventoryService implements AutoCloseable {

    public static final String QUEUE = "inventory.requests";

    private final Connection connection;
    private final Channel channel;
    private final Map<String, Integer> stock = new HashMap<>(Map.of("KETTLE-1", 4, "MUG-1", 10, "TEAPOT-1", 5));

    public InventoryService(Broker broker) throws Exception {
        connection = broker.connect();
        channel = connection.createChannel();
        channel.queueDeclare(QUEUE, true, false, false, null);
    }

    /** Takes every request now waiting and replies to each. Returns how many were handled. */
    public int handleWaiting() throws Exception {
        List<GetResponse> batch = new ArrayList<>();
        GetResponse r;
        while ((r = channel.basicGet(QUEUE, false)) != null) {
            batch.add(r);
        }
        batch.sort(Comparator.comparing((GetResponse g) -> body(g).contains("MUG") ? 0 : 1));   // cached items first
        for (GetResponse g : batch) {
            String reply = reserve(body(g));
            AMQP.BasicProperties props = new AMQP.BasicProperties.Builder()
                    .correlationId(g.getProps().getCorrelationId()).build();
            String replyTo = g.getProps().getReplyTo();
            channel.basicPublish("", replyTo, props, reply.getBytes(StandardCharsets.UTF_8));
            channel.basicAck(g.getEnvelope().getDeliveryTag(), false);
        }
        return batch.size();
    }

    private String reserve(String request) {
        String[] p = request.split(" ");   // "reserve KETTLE-1 x 5"
        String sku = p[1];
        int qty = Integer.parseInt(p[3]);
        if (stock.getOrDefault(sku, 0) >= qty) {
            stock.merge(sku, -qty, Integer::sum);
            return "RESERVED " + qty + " x " + sku;
        }
        return "REFUSED " + qty + " x " + sku;
    }

    private static String body(GetResponse g) {
        return new String(g.getBody(), StandardCharsets.UTF_8);
    }

    @Override
    public void close() throws Exception {
        connection.close();
    }
}
