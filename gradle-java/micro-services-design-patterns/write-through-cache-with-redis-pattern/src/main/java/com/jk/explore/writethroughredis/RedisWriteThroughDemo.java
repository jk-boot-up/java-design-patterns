package com.jk.explore.writethroughredis;

import java.util.ArrayList;
import java.util.List;
import redis.clients.jedis.Jedis;

/**
 * The five acts, against a real Redis and a real PostgreSQL started and stopped by this program.
 */
public final class RedisWriteThroughDemo {

    public static void main(String[] args) throws Exception {
        if (!Infra.containerRuntimeAvailable()) {
            System.out.println(Infra.NO_RUNTIME_ADVICE);
            return;
        }
        for (String line : run()) {
            System.out.println(line);
        }
    }

    static String money(int pence) {
        return String.format("£%.2f", pence / 100.0);
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();
        try (Infra infra = new Infra()) {
            try {
                infra.start();
            } catch (RuntimeException e) {
                out.add(Infra.WOULD_NOT_START_ADVICE);
                return out;
            }
            PriceDb db = new PriceDb(infra);
            PriceStore store = new PriceStore(db, infra, 3600);
            store.put("KETTLE-1", 3000, false);

            out.add("ONE. A price change goes round the cache.");
            db.write("KETTLE-1", 2700, false);
            out.add("  the nightly job writes £27.00 straight into PostgreSQL");
            out.add("  product page (Redis): " + money(store.get("KETTLE-1")) + "; checkout (PostgreSQL): " + money(db.read("KETTLE-1")));
            out.add("  the customer sees one price and pays another");

            out.add("");
            out.add("TWO. Write-through: every write goes through PriceStore.");
            store.put("KETTLE-1", 2700, false);
            PriceStore otherInstance = new PriceStore(db, infra, 3600);
            out.add("  store.put(KETTLE-1, £27.00): PostgreSQL written, then Redis, before it returns");
            out.add("  product page: " + money(store.get("KETTLE-1")) + "; checkout: " + money(db.read("KETTLE-1"))
                    + "; a second app instance reading the same Redis: " + money(otherInstance.get("KETTLE-1")));

            out.add("");
            out.add("THREE. Reads come from Redis.");
            long hitsBefore = hits(infra);
            int dbReadsBefore = db.reads();
            for (int i = 0; i < 100; i++) {
                store.get("KETTLE-1");
            }
            out.add("  100 page views: " + (db.reads() - dbReadsBefore) + " database reads; Redis counted "
                    + (hits(infra) - hitsBefore) + " cache hits");

            out.add("");
            out.add("FOUR. When one of the two refuses.");
            try {
                store.put("KETTLE-1", 2500, true);
            } catch (Exception refused) {
                out.add("  PostgreSQL is read-only for maintenance: the write fails, Redis is never touched");
            }
            out.add("  page " + money(store.get("KETTLE-1")) + ", database " + money(db.read("KETTLE-1")) + ": still agree");
            infra.pauseRedis();
            boolean cached = store.put("KETTLE-1", 2500, false);
            infra.unpauseRedis();
            out.add("  now Redis is unreachable during a write: PostgreSQL saved £25.00, Redis written: " + cached);
            out.add("  when Redis returns: page " + money(store.get("KETTLE-1")) + ", database " + money(db.read("KETTLE-1"))
                    + ": two systems, and no transaction spans both");
            out.add("  a time-to-live on each cached price bounds how long they can disagree");

            out.add("");
            out.add("FIVE. The bill: every write waits twice, and the cache fills.");
            long keysBefore = keys(infra);
            for (int i = 1; i <= 1000; i++) {
                store.put("SKU-" + i, 1000 + i, false);
            }
            out.add("  the nightly job updates 1000 prices: 1000 PostgreSQL writes and 1000 Redis writes");
            out.add("  Redis now holds " + (keys(infra) - keysBefore) + " more prices, though most will never be viewed");
        }
        return out;
    }

    private static long hits(Infra infra) {
        try (Jedis r = infra.redis()) {
            String info = r.info("stats");
            for (String line : info.split("\r\n")) {
                if (line.startsWith("keyspace_hits:")) {
                    return Long.parseLong(line.substring("keyspace_hits:".length()).trim());
                }
            }
            return -1;
        }
    }

    private static long keys(Infra infra) {
        try (Jedis r = infra.redis()) {
            return r.dbSize();
        }
    }

    private RedisWriteThroughDemo() {
    }
}
