package com.jk.explore.pubsubredis;

import java.util.List;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.Pipeline;

/**
 * The publisher. It knows one thing: the Redis server. It does not know who is listening.
 *
 * <p>Publishing hands one message to Redis under a channel name. Redis copies it to every
 * connection listening on that name at that instant, and answers with how many that was.
 * That number is all the order service ever learns.
 */
public class OrderService implements AutoCloseable {

    /** The channel an order being placed is published on. */
    public static final String PLACED = "orders.placed";

    /** The channel an order being cancelled is published on. */
    public static final String CANCELLED = "orders.cancelled";

    private final Jedis redis;

    public OrderService(RedisServer server) {
        this.redis = server.connect();
    }

    /** Publishes the event and returns how many listeners Redis handed it to. */
    public long publish(OrderEvent event) {
        return redis.publish(event.channel(), event.text());
    }

    /**
     * Publishes a run of placed orders in one go, the way a flash sale arrives, and returns
     * how many listeners Redis handed each one to.
     *
     * <p>The orders are sent without waiting for each answer in between. Redis's word for
     * that is a pipeline. It changes nothing about what Redis does with each order; it only
     * saves the round trip per order.
     */
    public List<Long> publishPlaced(int firstOrder, int howMany) {
        Pipeline pipeline = redis.pipelined();
        for (int n = firstOrder; n < firstOrder + howMany; n++) {
            OrderEvent event = OrderEvent.placed(n);
            pipeline.publish(event.channel(), event.text());
        }
        return pipeline.syncAndReturnAll().stream().map(answer -> (Long) answer).toList();
    }

    @Override
    public void close() {
        redis.close();
    }
}
