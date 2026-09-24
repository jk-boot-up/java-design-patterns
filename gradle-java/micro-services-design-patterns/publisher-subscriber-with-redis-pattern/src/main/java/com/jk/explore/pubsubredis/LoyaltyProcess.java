package com.jk.explore.pubsubredis;

import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPubSub;

/**
 * The loyalty-points service, as a program of its own.
 *
 * <p>The demo starts this class in a second Java process, with its own memory and its own
 * process number, the way a real service would run on another machine. It shares nothing
 * with the order service except the address of the Redis server. It listens for a fixed
 * number of placed orders, prints each one on its own output, and exits.
 *
 * <p>Arguments: the Redis host, the Redis port, and how many orders to wait for.
 */
public final class LoyaltyProcess {

    /** Printed once Redis has confirmed the subscription, so the parent knows it may publish. */
    public static final String READY = "loyalty listening";

    /** Printed before each order this process receives. */
    public static final String GOT = "loyalty got ";

    private LoyaltyProcess() {
    }

    public static void main(String[] args) {
        String host = args[0];
        int port = Integer.parseInt(args[1]);
        int wanted = Integer.parseInt(args[2]);
        try (Jedis redis = new Jedis(host, port)) {
            redis.clientSetname("loyalty");
            redis.subscribe(new JedisPubSub() {
                private int seen;

                @Override
                public void onSubscribe(String channel, int count) {
                    System.out.println(READY);
                    System.out.flush();
                }

                @Override
                public void onMessage(String channel, String message) {
                    System.out.println(GOT + OrderEvent.read(message).orderId());
                    System.out.flush();
                    if (++seen == wanted) {
                        unsubscribe();
                    }
                }
            }, OrderService.PLACED);
        }
    }
}
