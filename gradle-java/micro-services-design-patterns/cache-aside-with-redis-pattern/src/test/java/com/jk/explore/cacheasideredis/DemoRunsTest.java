package com.jk.explore.cacheasideredis;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.Test;

/**
 * The demo is the document. Every number quoted in the README, in the slides and in the
 * narration is asserted here, so a change to the code that changes a figure fails the build
 * instead of quietly making the documents wrong.
 */
class DemoRunsTest {

    @Test
    void theSixActsRunAgainstARealRedisAndPrintTheFiguresTheDocumentsQuote() {
        assumeTrue(RedisServer.containerRuntimeAvailable(), "needs a container runtime");
        String out = runTheDemo();

        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        assertTrue(out.contains("1000 product page views over 10 popular products: 1000 database reads."), out);
        assertTrue(out.contains("the same 1000 views: 10 database reads, 990 cache hits, 10 misses."), out);
        assertTrue(out.contains("Redis now holds 10 keys, each written with a 60 second expiry."), out);
        assertTrue(out.contains("with its cache in its own memory, its first 10 views: 10 database reads, 0 cache hits."), out);
        assertTrue(out.contains("with its cache in Redis, its first 10 views: 0 database reads, 10 cache hits."), out);
        assertTrue(out.contains("asks for product:SKU-0 and is told: 1000."), out);
        assertTrue(out.contains("deletes the key once. copies left for any process: 0."), out);
        assertTrue(out.contains("SKU-0 is cached for 2 seconds. another system changes the price to 2000. a customer sees 1000."), out);
        assertTrue(out.contains("Redis removes the key itself when the time is up. a customer then sees 2000."), out);
        assertTrue(out.contains("seconds to live, as Redis reports it: -1, which means never."), out);
        assertTrue(out.contains("the price changes to 2100. 2 seconds later a customer still sees 2000."), out);
        assertTrue(out.contains("50 requests arrive together, across 2 shop instances"), out);
        assertTrue(out.contains("a database read takes 500 milliseconds."), out);
        assertTrue(out.contains("database reads: more than 40, for one price."), out);
        assertTrue(out.contains("requests share a read inside each instance: 2 database reads, one per instance."), out);
        assertTrue(out.contains("requests share a lock kept in Redis: 1 database read."), out);
        assertTrue(out.contains("expires by itself after 5 seconds if its holder dies."), out);
        assertTrue(out.contains("the first 10 views: 10 database reads."), out);
        assertTrue(out.contains("maxmemory 0, which means no limit, and maxmemory-policy noeviction."), out);
        assertTrue(out.contains("Redis holds SKU-0 as the string 1000."), out);
        assertTrue(out.contains("1 container for 2 shop processes."), out);
    }

    private static String runTheDemo() {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            RedisCacheAsideDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        return captured.toString(StandardCharsets.UTF_8);
    }
}
