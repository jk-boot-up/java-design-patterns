package com.jk.explore.transactionaloutbox;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;

/**
 * The broker: another process, on the other side of a network, that carries messages to
 * whoever is listening.
 *
 * It is a separate system, and that is the entire problem this pattern exists to solve. The
 * Orders database cannot include it in a transaction. There is no commit that covers both a
 * row in a table here and a message accepted over there, so any code that writes one and then
 * the other has a moment in the middle where only half of it has happened.
 */
public final class MessageBroker {

    public static final long LATENCY_MILLIS = 15;

    private final List<OutboxMessage> delivered = new ArrayList<>();
    private final List<Consumer<OutboxMessage>> subscribers = new ArrayList<>();
    private final RemoteCall<OutboxMessage, String> publish;

    public MessageBroker(SimulatedClock clock, CallLog log) {
        this.publish = new RemoteCall<>("Broker", LATENCY_MILLIS, this::doPublish, clock, log);
    }

    public void subscribe(Consumer<OutboxMessage> subscriber) {
        subscribers.add(subscriber);
    }

    public String publish(OutboxMessage message) {
        return publish.invoke(message);
    }

    /** Scripts the broker being down, which is a normal Tuesday. */
    public void failNext(int count) {
        publish.failNext(count);
    }

    /** Everything the broker accepted, including anything it accepted twice. */
    public List<OutboxMessage> delivered() {
        return List.copyOf(delivered);
    }

    public int deliveredCount() {
        return delivered.size();
    }

    /** How many times one particular message was accepted. Should be one. Often is not. */
    public long timesDelivered(String messageId) {
        return delivered.stream().filter(m -> m.messageId().equals(messageId)).count();
    }

    private String doPublish(OutboxMessage message) {
        delivered.add(message);
        for (Consumer<OutboxMessage> subscriber : subscribers) {
            subscriber.accept(message);
        }
        return "accepted " + message.messageId();
    }
}
