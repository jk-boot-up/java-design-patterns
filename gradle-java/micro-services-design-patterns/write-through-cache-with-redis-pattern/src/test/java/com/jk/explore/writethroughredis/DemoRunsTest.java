package com.jk.explore.writethroughredis;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import org.junit.jupiter.api.Test;

/** The whole demo against real Redis and PostgreSQL; skipped, not failed, without a container runtime. */
class DemoRunsTest {

    @Test
    void acts() throws Exception {
        assumeTrue(Infra.containerRuntimeAvailable(), "needs a container runtime");
        String all = String.join("\n", RedisWriteThroughDemo.run());
        assertTrue(all.contains("product page (Redis): £30.00; checkout (PostgreSQL): £27.00"), all);
        assertTrue(all.contains("a second app instance reading the same Redis: £27.00"), all);
        assertTrue(all.contains("100 page views: 0 database reads; Redis counted 100 cache hits"), all);
        assertTrue(all.contains("page £27.00, database £27.00: still agree"), all);
        assertTrue(all.contains("PostgreSQL saved £25.00, Redis written: false"), all);
        assertTrue(all.contains("when Redis returns: page £27.00, database £25.00"), all);
        assertTrue(all.contains("Redis now holds 1000 more prices"), all);
    }

    @Test
    void adviceIsASentenceNotAStackTrace() {
        assertTrue(Infra.NO_RUNTIME_ADVICE.contains("Start Docker Desktop"));
    }
}
