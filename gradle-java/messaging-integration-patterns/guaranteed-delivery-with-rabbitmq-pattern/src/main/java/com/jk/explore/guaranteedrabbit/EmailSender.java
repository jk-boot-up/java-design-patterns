package com.jk.explore.guaranteedrabbit;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.GetResponse;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

/**
 * The receiver: takes emails off the queue, sends them, and only then acknowledges each one.
 */
public final class EmailSender {

    private final List<String> sent = new ArrayList<>();
    private final List<String> redelivered = new ArrayList<>();

    /**
     * Takes up to {@code count} emails and sends them. With {@code crashBeforeAck}, it sends the last
     * one and then dies before acknowledging it.
     */
    public void take(Broker broker, String queue, int count, boolean crashBeforeAck) throws Exception {
        Connection connection = broker.connect();
        Channel channel = connection.createChannel();
        for (int i = 0; i < count; i++) {
            GetResponse r = channel.basicGet(queue, false);   // false: we will acknowledge ourselves
            if (r == null) {
                break;
            }
            String mail = new String(r.getBody(), StandardCharsets.UTF_8);
            sent.add(mail);
            if (r.getEnvelope().isRedeliver()) {
                redelivered.add(mail);
            }
            boolean last = i == count - 1;
            if (crashBeforeAck && last) {
                connection.abort();   // the process dies: no acknowledgement is ever written
                return;
            }
            channel.basicAck(r.getEnvelope().getDeliveryTag(), false);
        }
        connection.close();
    }

    public List<String> sent() {
        return sent;
    }

    public List<String> redelivered() {
        return redelivered;
    }

    public long timesSent(String mail) {
        return sent.stream().filter(mail::equals).count();
    }
}
