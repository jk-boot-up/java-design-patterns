package com.jk.explore.guaranteedrabbit;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.MessageProperties;
import java.nio.charset.StandardCharsets;

/**
 * Checkout's side: puts confirmation emails on a queue. How the queue and messages are declared
 * decides whether they survive.
 */
public final class Outbox implements AutoCloseable {

    private final Connection connection;
    private final Channel channel;
    private final String queue;
    private final boolean guaranteed;

    public Outbox(Broker broker, String queue, boolean guaranteed) throws Exception {
        this.connection = broker.connect();
        this.channel = connection.createChannel();
        this.queue = queue;
        this.guaranteed = guaranteed;
        // Durable: the queue itself is written to disk. RabbitMQ 4 no longer allows shared queues
        // that are not, so what varies here is only how each message is sent.
        channel.queueDeclare(queue, true, false, false, null);
        if (guaranteed) {
            channel.confirmSelect();   // the broker will confirm each message once it is safely stored
        }
    }

    public void send(String mail) throws Exception {
        channel.basicPublish("", queue,
                guaranteed ? MessageProperties.PERSISTENT_TEXT_PLAIN : MessageProperties.TEXT_PLAIN,
                mail.getBytes(StandardCharsets.UTF_8));
        if (guaranteed) {
            channel.waitForConfirmsOrDie(10_000);
        }
    }

    @Override
    public void close() throws Exception {
        connection.close();
    }
}
