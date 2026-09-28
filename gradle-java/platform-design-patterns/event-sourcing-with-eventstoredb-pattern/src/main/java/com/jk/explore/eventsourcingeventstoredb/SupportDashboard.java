package com.jk.explore.eventsourcingeventstoredb;

import io.kurrent.dbclient.KurrentDBClient;
import io.kurrent.dbclient.Position;
import io.kurrent.dbclient.ResolvedEvent;
import io.kurrent.dbclient.SubscribeToAllOptions;
import io.kurrent.dbclient.Subscription;
import io.kurrent.dbclient.SubscriptionFilter;
import io.kurrent.dbclient.SubscriptionListener;
import java.time.Instant;
import java.util.Map;
import java.util.TreeMap;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * The support team's screen: every customer's balance, kept in memory, built only by reading the
 * log. This second copy of the data, shaped for one screen, is what event sourcing calls a
 * projection or a read model.
 *
 * <p>It is fed by a catch-up subscription. The dashboard asks KurrentDB for every event in every
 * stream whose name starts with loyalty-, starting from the very first. The server sends the old
 * events first, as fast as it can, then says "you have caught up", and from then on sends each
 * new event as it is written. Starting late loses nothing.
 */
public final class SupportDashboard implements AutoCloseable {

    private final KurrentDBClient client;
    private final Map<String, Integer> balances = new ConcurrentHashMap<>();
    private final AtomicInteger eventsSeen = new AtomicInteger();
    private final AtomicInteger eventsWhenCaughtUp = new AtomicInteger(-1);
    private volatile Subscription subscription;

    public SupportDashboard(KurrentDBClient client) {
        this.client = client;
    }

    public void start() {
        SubscriptionFilter loyaltyStreamsOnly = SubscriptionFilter.newBuilder().addStreamNamePrefix("loyalty-").build();
        SubscriptionListener listener = new SubscriptionListener() {
            @Override
            public void onEvent(Subscription s, ResolvedEvent resolved) {
                LoyaltyEvent event = EventJson.fromRecorded(resolved.getOriginalEvent());
                balances.merge(event.customerId(), event.effectOnBalance(), Integer::sum);
                eventsSeen.incrementAndGet();
            }

            @Override
            public void onCaughtUp(Subscription s, Instant timestamp, Long streamRevision, Position position) {
                eventsWhenCaughtUp.compareAndSet(-1, eventsSeen.get());
            }
        };
        try {
            subscription = client.subscribeToAll(listener,
                    SubscribeToAllOptions.get().fromStart().filter(loyaltyStreamsOnly)).get();
        } catch (Exception e) {
            throw new IllegalStateException("could not subscribe", e);
        }
    }

    public boolean caughtUp() {
        return eventsWhenCaughtUp.get() >= 0;
    }

    /** How many events had arrived when the server said the dashboard had caught up. */
    public int eventsWhenCaughtUp() {
        return eventsWhenCaughtUp.get();
    }

    public int eventsSeen() {
        return eventsSeen.get();
    }

    /** The balance the screen shows, or null if the customer has never appeared. */
    public Integer balanceOf(String customerId) {
        return balances.get(customerId);
    }

    public Map<String, Integer> balances() {
        return new TreeMap<>(balances);
    }

    @Override
    public void close() {
        if (subscription != null) {
            subscription.stop();
        }
        try {
            client.shutdown().get();
        } catch (Exception e) {
            // closing quietly is fine
        }
    }
}
