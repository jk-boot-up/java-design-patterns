package com.jk.explore.pollingrabbit;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import org.junit.jupiter.api.Test;

/** The whole demo against a real broker; skipped, not failed, when no container runtime is running. */
class DemoRunsTest {

    @Test
    void acts() throws Exception {
        assumeTrue(Broker.containerRuntimeAvailable(), "needs a container runtime");
        String all = String.join("\n", RabbitPollingConsumerDemo.run());
        assertTrue(all.contains("the broker pushed 50 at once"), all);
        assertTrue(all.contains("after the crash: back on the queue 50"), all);
        assertTrue(all.contains("printed 50 of 50 in 10 ticks"), all);
        assertTrue(all.contains("printed 5; safely waiting on the queue: 15"), all);
        assertTrue(all.contains("printed 20 of 20, none lost"), all);
        assertTrue(all.contains("600 requests to the broker, all empty"), all);
        assertTrue(all.contains("the printer holds 5"), all);
    }

    @Test
    void adviceIsASentenceNotAStackTrace() {
        assertTrue(Broker.NO_RUNTIME_ADVICE.contains("Start Docker Desktop"));
    }
}
