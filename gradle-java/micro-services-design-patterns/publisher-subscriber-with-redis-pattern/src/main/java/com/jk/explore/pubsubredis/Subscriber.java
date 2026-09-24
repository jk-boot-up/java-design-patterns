package com.jk.explore.pubsubredis;

import java.util.ArrayList;
import java.util.List;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPubSub;
import redis.clients.jedis.exceptions.JedisConnectionException;

/**
 * One service listening to Redis, on a connection of its own and a thread of its own.
 *
 * <p>A Redis connection that is listening can do nothing else, so each subscriber holds its
 * own, exactly as a separate service would. Listening by exact channel name is Redis's
 * SUBSCRIBE; listening by a name with a star in it is PSUBSCRIBE, where the P stands for
 * pattern.
 *
 * <p>A subscriber can be told to stop reading for a while, which is how the demo stages a
 * service that has fallen behind. While it is stopped, Redis keeps the messages it could not
 * deliver in a pile for this one connection, up to a size limit.
 */
public class Subscriber implements AutoCloseable {

    private final String name;
    private final Jedis connection;
    private final List<String> received = new ArrayList<>();
    private final Object gate = new Object();
    private final Thread reader;
    private final boolean byPattern;

    private volatile boolean listening;
    private volatile boolean cutOff;
    private boolean paused;

    private final JedisPubSub handler = new JedisPubSub() {
        @Override
        public void onSubscribe(String channel, int count) {
            listening = true;
        }

        @Override
        public void onPSubscribe(String pattern, int count) {
            listening = true;
        }

        @Override
        public void onMessage(String channel, String message) {
            take(message);
        }

        @Override
        public void onPMessage(String pattern, String channel, String message) {
            take(message);
        }
    };

    private Subscriber(RedisServer server, String name, boolean byPattern, String... names) {
        this.name = name;
        this.byPattern = byPattern;
        this.connection = server.connect();
        connection.clientSetname(name);
        this.reader = new Thread(() -> {
            try {
                if (byPattern) {
                    connection.psubscribe(handler, names);
                } else {
                    connection.subscribe(handler, names);
                }
            } catch (JedisConnectionException e) {
                // Redis closed this connection. Nothing more will arrive on it.
                cutOff = true;
            } finally {
                listening = false;
            }
        }, name + "-listener");
        reader.setDaemon(true);
        reader.start();
        // Asking Redis to start sending is a message that has to arrive. Publishing before
        // Redis has confirmed it would lose the event, so wait for the confirmation.
        Poll.until(name + " to be listening", () -> listening);
    }

    /** Listens on exact channel names, and returns once Redis has confirmed it. */
    public static Subscriber listen(RedisServer server, String name, String... channels) {
        return new Subscriber(server, name, false, channels);
    }

    /** Listens on every channel whose name matches, such as orders.* for every order event. */
    public static Subscriber listenToPattern(RedisServer server, String name, String pattern) {
        return new Subscriber(server, name, true, pattern);
    }

    public String name() {
        return name;
    }

    private void take(String message) {
        synchronized (gate) {
            while (paused) {
                try {
                    gate.wait();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    return;
                }
            }
            received.add(OrderEvent.read(message).toString());
        }
    }

    /** The listener stops reading. Whatever Redis sends it now has to wait somewhere. */
    public void stopReading() {
        synchronized (gate) {
            paused = true;
        }
    }

    /** The listener starts reading again. */
    public void startReading() {
        synchronized (gate) {
            paused = false;
            gate.notifyAll();
        }
    }

    /** Every event this subscriber has handled, in the order it handled them. */
    public List<String> received() {
        synchronized (gate) {
            return List.copyOf(received);
        }
    }

    /** Just the order numbers, which is all most acts need to show. */
    public List<String> orders() {
        return received().stream().map(text -> text.substring(text.indexOf(' ') + 1)).toList();
    }

    public int count() {
        synchronized (gate) {
            return received.size();
        }
    }

    /** True once Redis has closed this subscriber's connection from its own side. */
    public boolean wasCutOff() {
        return cutOff;
    }

    /** True once the listening thread has ended, for whatever reason. */
    public boolean finished() {
        return !reader.isAlive();
    }

    /** Stops listening and closes the connection, as a service shutting down would. */
    @Override
    public void close() {
        startReading();
        try {
            if (handler.isSubscribed()) {
                if (byPattern) {
                    handler.punsubscribe();
                } else {
                    handler.unsubscribe();
                }
            }
        } catch (Exception e) {
            // A connection Redis already closed has nothing to unsubscribe from.
        }
        Poll.until(name + " to stop listening", () -> !reader.isAlive());
        connection.close();
    }
}
