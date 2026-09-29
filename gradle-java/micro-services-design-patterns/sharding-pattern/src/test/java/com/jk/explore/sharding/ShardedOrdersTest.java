package com.jk.explore.sharding;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class ShardedOrdersTest {

    @Test
    void customerAlwaysMapsToTheSameShard() {
        ShardedOrders s = new ShardedOrders(3);
        assertEquals(s.shardOf(17), s.shardOf(17));
        assertEquals(2, s.shardOf(17));
    }

    @Test
    void ordersLandOnTheirCustomersShard() {
        ShardedOrders s = new ShardedOrders(3);
        s.insert(new Order("A", 17, 100));
        assertEquals(1, s.shards().get(2).size());
        assertEquals(0, s.shards().get(0).size());
    }

    @Test
    void oneCustomerAsksOneShard() {
        ShardedOrders s = new ShardedOrders(3);
        ShardingDemo.blackFridayMinute().forEach(s::insert);
        s.ordersOf(5);
        assertEquals(1, s.shards().stream().mapToInt(OrderDatabase::queriesAnswered).sum());
    }

    @Test
    void everywhereAsksAllAndMerges() {
        ShardedOrders s = new ShardedOrders(3);
        ShardingDemo.blackFridayMinute().forEach(s::insert);
        assertEquals(25, s.everywhere(o -> o.pence() > 50000).size());
        assertEquals(3, s.shards().stream().mapToInt(OrderDatabase::queriesAnswered).sum());
    }
}
