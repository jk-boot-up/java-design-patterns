package com.jk.explore.eventbusnats;

import static java.nio.charset.StandardCharsets.UTF_8;

import io.nats.client.Message;
import io.nats.client.Subscription;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;

/**
 * One store concern listening to the bus: the email service, the warehouse, the analytics tally.
 *
 * <p>Every wait here has a deadline. If the event does not arrive, the run fails and says which listener
 * was waiting for what. It never waits a fixed amount of time and then assumes.
 */
public class StoreSubscriber {

    private static final Duration DEADLINE = Duration.ofSeconds(20);

    private final String listener;
    private final Subscription subscription;
    private final List<String> heard = new ArrayList<>();
    private final List<String> events = new ArrayList<>();

    StoreSubscriber(String listener, Subscription subscription) {
        this.listener = listener;
        this.subscription = subscription;
    }

    /** Waits for the next event, and fails rather than hanging if it never comes. */
    public String waitForNext() {
        return waitForNext(DEADLINE);
    }

    /** The same, with a deadline of its own. */
    public String waitForNext(Duration deadline) {
        try {
            Message message = subscription.nextMessage(deadline);
            if (message == null) {
                throw new IllegalStateException(
                        listener + " waited " + deadline.toSeconds() + " seconds on " + subscription.getSubject()
                                + " and nothing arrived");
            }
            String event = new String(message.getData(), UTF_8);
            heard.add(listener + " saw " + event);
            events.add(event);
            return event;
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(e);
        }
    }

    /** Waits for a known number of events, in the order the server sends them. */
    public List<String> waitFor(int count) {
        for (int i = 0; i < count; i++) {
            waitForNext();
        }
        return heard;
    }

    public List<String> heard() {
        return heard;
    }

    /** The events themselves, without the listener's name in front of them. */
    public List<String> events() {
        return events;
    }

    /** Stops listening, without closing this service's connection to the bus. */
    public void stopListening() {
        subscription.unsubscribe();
    }

    /** How many events the server has handed this listener since it started listening. */
    public long received() {
        return subscription.getDeliveredCount();
    }

    public String subject() {
        return subscription.getSubject();
    }
}
