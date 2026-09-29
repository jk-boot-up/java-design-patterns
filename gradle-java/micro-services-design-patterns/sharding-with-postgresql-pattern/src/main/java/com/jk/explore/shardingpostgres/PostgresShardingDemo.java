package com.jk.explore.shardingpostgres;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts, against real PostgreSQL databases started and stopped by this program.
 */
public final class PostgresShardingDemo {

    static final int CUSTOMERS = 2500;

    /** Each customer's order total, in pence: fixed, so every run gives the same answers. */
    static int pence(int customer) {
        return (customer * 37 % 1000) * 100;
    }

    public static void main(String[] args) throws Exception {
        if (!Shards.containerRuntimeAvailable()) {
            System.out.println(Shards.NO_RUNTIME_ADVICE);
            return;
        }
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();

        out.add("ONE. One database for every order.");
        try (Shards one = new Shards(1)) {
            try {
                one.start();
            } catch (RuntimeException e) {
                out.add(Shards.WOULD_NOT_START_ADVICE);
                return out;
            }
            ShardRouter single = new ShardRouter(one);
            single.placeOrders(CUSTOMERS);
            out.add("  one PostgreSQL holds all " + single.count(0) + " orders; every read and write of Black Friday lands on it");
        }

        try (Shards shards = new Shards(3)) {
            shards.start();
            ShardRouter router = new ShardRouter(shards);

            out.add("");
            out.add("TWO. Three PostgreSQL shards, split by customer number modulo 3.");
            router.placeOrders(CUSTOMERS);
            for (int s = 0; s < 3; s++) {
                out.add("  shard-" + s + " (its own database): " + router.count(s) + " orders");
            }
            out.add("  customer 17 lives on shard-" + router.shardFor(17) + ", customer 42 on shard-" + router.shardFor(42));

            out.add("");
            out.add("THREE. A question about one customer asks one shard.");
            out.add("  customer 17's orders: " + router.ordersOf(17) + "; shards asked: " + router.shardsAsked());

            out.add("");
            out.add("FOUR. A question about everyone asks every shard.");
            out.add("  orders over £500: " + router.countOver(50000) + ", from " + router.shardsAsked()
                    + " databases, added up by the application");
            boolean first = router.redeem("WELCOME10", 17);
            boolean second = router.redeem("WELCOME10", 42);
            out.add("  one-use coupon WELCOME10, UNIQUE in every shard: customer 17 accepted " + first
                    + ", customer 42 accepted " + second);
            out.add("  each database only knows its own rows: a rule across shards is the application's job");

            out.add("");
            out.add("FIVE. The bill: changing the number of shards moves customers.");
            int moved = 0;
            int movedConsistent = 0;
            for (int c = 1; c <= CUSTOMERS; c++) {
                if (c % 3 != c % 4) {
                    moved++;
                }
                if (jump(c, 3) != jump(c, 4)) {
                    movedConsistent++;
                }
            }
            out.add("  a fourth shard with customer modulo 4: " + moved + " of " + CUSTOMERS + " customers must move");
            out.add("  with consistent hashing (jump hash) instead: " + movedConsistent + " must move");
            out.add("  and no transaction spans two shards; one very busy customer still overloads their one shard");
        }
        return out;
    }

    /** Jump consistent hash (Lamping and Veach): adding a bucket moves only about 1 in n keys. */
    static int jump(long key, int buckets) {
        long b = -1;
        long j = 0;
        while (j < buckets) {
            b = j;
            key = key * 2862933555777941757L + 1;
            j = (long) ((b + 1) * ((double) (1L << 31) / (double) ((key >>> 33) + 1)));
        }
        return (int) b;
    }

    private PostgresShardingDemo() {
    }
}
