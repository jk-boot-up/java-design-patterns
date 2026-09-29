package com.jk.explore.sharding;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Predicate;

/**
 * The pattern: orders are split across several databases by a shard key, the customer number, so each holds only its share.
 *
 * <p>The router picks the shard from the key alone. A question about one
 * customer goes to one shard; a question about everyone must go to all of
 * them and the answers be merged.
 */
public final class ShardedOrders {

    private final List<OrderDatabase> shards = new ArrayList<>();

    public ShardedOrders(int count) {
        for (int i = 0; i < count; i++) {
            shards.add(new OrderDatabase("shard-" + i));
        }
    }

    /** Which shard a customer lives on: their number modulo the number of shards. */
    public int shardOf(int customer) {
        return customer % shards.size();
    }

    public void insert(Order o) {
        shards.get(shardOf(o.customer())).insert(o);
    }

    public List<Order> ordersOf(int customer) {
        return shards.get(shardOf(customer)).find(o -> o.customer() == customer);
    }

    /** A question about everyone: ask every shard and merge. */
    public List<Order> everywhere(Predicate<Order> test) {
        List<Order> all = new ArrayList<>();
        shards.forEach(s -> all.addAll(s.find(test)));
        return all;
    }

    public List<OrderDatabase> shards() {
        return shards;
    }
}
