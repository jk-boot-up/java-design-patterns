package com.jk.explore.guaranteedrabbit;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import org.junit.jupiter.api.Test;

/** The whole demo against a real broker; skipped, not failed, when no container runtime is running. */
class DemoRunsTest {

    @Test
    void acts() throws Exception {
        assumeTrue(Broker.containerRuntimeAvailable(), "needs a container runtime");
        String all = String.join("\n", RabbitGuaranteedDeliveryDemo.run());
        assertTrue(all.contains("10 emails queued: waiting 10"), all);
        assertTrue(all.contains("the queue is still there, waiting 0"), all);
        assertTrue(all.contains("the broker restarts: waiting 10"), all);
        assertTrue(all.contains("still waiting: 4"), all);
        assertTrue(all.contains("sent 10 of 10, each once; waiting now 0"), all);
        assertTrue(all.contains("marked as redelivered: [MAIL-11]"), all);
        assertTrue(all.contains("the customer gets MAIL-11 2 times"), all);
    }

    @Test
    void adviceIsASentenceNotAStackTrace() {
        assertTrue(Broker.NO_RUNTIME_ADVICE.contains("Start Docker Desktop"));
    }
}
