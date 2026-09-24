package com.jk.explore.ratelimiterredis;

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
        assumeTrue(Redis.containerRuntimeAvailable(), "needs a container runtime");
        String out = runTheDemo();

        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        assertTrue(out.contains("3 servers, each with its own bucket: 30 allowed, not 10."), out);
        assertTrue(out.contains("scaled out to 6 servers, the same 90: 60 allowed."), out);
        assertTrue(out.contains("client-42 sends 90: 10 allowed, 80 refused."), out);
        assertTrue(out.contains("client-77 sends 90: 10 allowed. Redis holds 2 keys"), out);
        assertTrue(out.contains("client-42's next search: refused. retry after 60 minutes."), out);
        assertTrue(out.contains("all 90 released at the same instant on 90 threads: 10 allowed, 80 refused."), out);
        assertTrue(out.contains("server-1 reads 1. server-2 reads 1. both write back 0 and serve: 2 searches from 1 token. Redis now says 0."), out);
        assertTrue(out.contains("finds 0, and refuses. 1 search from 1 token, 1 refused, 1 retry."), out);
        assertTrue(out.contains("client-42 spends 10 searches through them. the next: refused."), out);
        assertTrue(out.contains("client-42 sends 20 through it: 10 allowed."), out);
        assertTrue(out.contains("Redis holds 1000 keys. each is set to delete itself in 60 minutes"), out);
        assertTrue(out.contains("5 searches: 5 errors from the limiter"), out);
        assertTrue(out.contains("1 container for 6 servers."), out);
    }

    private static String runTheDemo() {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            RedisRateLimiterDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        return captured.toString(StandardCharsets.UTF_8);
    }
}
