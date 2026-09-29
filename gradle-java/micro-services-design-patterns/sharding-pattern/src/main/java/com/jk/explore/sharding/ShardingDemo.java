package com.jk.explore.sharding;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: one database at its limit, shards by customer, one-shard questions, all-shard questions, and the bill.
 */
public final class ShardingDemo {

    static final int CUSTOMERS = 2500;

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** One Black Friday minute: every customer places one order; every 100th order is a big one. */
    static List<Order> blackFridayMinute() {
        List<Order> orders = new ArrayList<>();
        for (int c = 1; c <= CUSTOMERS; c++) {
            orders.add(new Order("ORD-" + c, c, c % 100 == 0 ? 60000 : 2500));
        }
        return orders;
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. One database for every order.");
        List<Order> minute = blackFridayMinute();
        int waiting = Math.max(0, minute.size() - OrderDatabase.PER_MINUTE);
        out.add("  Black Friday: " + minute.size() + " orders a minute; one database takes "
                + OrderDatabase.PER_MINUTE + " a minute");
        out.add("  orders left waiting every minute: " + waiting + ", and the queue keeps growing");

        out.add("");
        out.add("TWO. Three shards, split by customer number.");
        ShardedOrders sharded = new ShardedOrders(3);
        minute.forEach(sharded::insert);
        for (OrderDatabase s : sharded.shards()) {
            out.add("  " + s.name() + ": " + s.size() + " orders this minute"
                    + (s.size() <= OrderDatabase.PER_MINUTE ? " (within its limit)" : " (over its limit)"));
        }
        out.add("  customer 17 lives on shard-" + sharded.shardOf(17) + ", customer 42 on shard-" + sharded.shardOf(42));

        out.add("");
        out.add("THREE. A question about one customer asks one shard.");
        int before = sharded.shards().stream().mapToInt(OrderDatabase::queriesAnswered).sum();
        out.add("  customer 17's orders: " + sharded.ordersOf(17).stream().map(Order::id).toList());
        int after = sharded.shards().stream().mapToInt(OrderDatabase::queriesAnswered).sum();
        out.add("  shards asked: " + (after - before));

        out.add("");
        out.add("FOUR. A question about everyone asks every shard.");
        int b2 = sharded.shards().stream().mapToInt(OrderDatabase::queriesAnswered).sum();
        List<Order> big = sharded.everywhere(o -> o.pence() > 50000);
        int a2 = sharded.shards().stream().mapToInt(OrderDatabase::queriesAnswered).sum();
        out.add("  \"orders over £500 this minute\": " + big.size() + " found, shards asked: " + (a2 - b2));
        out.add("  the answers come back in three pieces and must be merged");

        out.add("");
        out.add("FIVE. The bill: changing the number of shards moves customers.");
        int moved = 0;
        for (int c = 1; c <= CUSTOMERS; c++) {
            if (c % 3 != c % 4) {
                moved++;
            }
        }
        out.add("  add a fourth shard (customer number modulo 4): " + moved + " of " + CUSTOMERS
                + " customers now belong on a different shard");
        out.add("  their orders must be copied across, and one very busy customer still overloads their one shard");
        return out;
    }

    private ShardingDemo() {
    }
}
