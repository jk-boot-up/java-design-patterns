package com.jk.explore.idempotentconsumer;

/**
 * The broker, and the one thing you need to know about it: it delivers <b>at least once</b>.
 *
 * That is not a defect in this class or in any real broker. It is the only honest guarantee
 * available once a message has to cross a network and be acknowledged. The sender publishes
 * and waits for an acknowledgement; if the acknowledgement is lost the sender cannot tell
 * whether the message arrived, and it has exactly two choices — send again, or not. Sending
 * again risks a duplicate. Not sending again risks losing the message forever. Every
 * production system chooses the duplicate.
 *
 * <p>So {@link #deliverTwice} is not this project being unfair to the consumers. It is a
 * Tuesday.
 */
public final class MessageBroker {

    public static final long LATENCY_MILLIS = 10;

    private final SimulatedClock clock;
    private final CallLog log;

    public MessageBroker(SimulatedClock clock, CallLog log) {
        this.clock = clock;
        this.log = log;
    }

    /** Delivers the message once, over the network, to one consumer. */
    public void deliver(Message message, MessageConsumer consumer) {
        new RemoteCall<Message, String>(consumer.name(), LATENCY_MILLIS, m -> {
            consumer.handle(m);
            return "delivered " + m.messageId();
        }, clock, log).invoke(message);
    }

    /**
     * Delivers the same message twice, which is what at-least-once means in practice.
     *
     * The consumer is not told which delivery is which, because the broker does not know
     * either. Both deliveries are identical, down to the message id.
     */
    public void deliverTwice(Message message, MessageConsumer consumer) {
        deliver(message, consumer);
        log.note("Broker", "REDELIVERY", message.messageId()
                + " -- the acknowledgement was lost, so it goes again");
        deliver(message, consumer);
    }
}
