package com.jk.explore.pollingrabbit;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.MessageProperties;
import java.nio.charset.StandardCharsets;

/**
 * Checkout's side: puts orders on the printing queue.
 */
public final class Orders {

    public static final String QUEUE = "labels";

    public static void send(Broker broker, int count) throws Exception {
        try (Connection c = broker.connect(); Channel ch = c.createChannel()) {
            ch.queueDeclare(QUEUE, true, false, false, null);
            for (int i = 1; i <= count; i++) {
                ch.basicPublish("", QUEUE, MessageProperties.PERSISTENT_TEXT_PLAIN,
                        ("ORD-" + i).getBytes(StandardCharsets.UTF_8));
            }
        }
        Poll.until(count + " orders on the queue", () -> broker.waiting(QUEUE) >= count);
    }

    private Orders() {
    }
}
