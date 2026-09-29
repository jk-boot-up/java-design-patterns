package com.jk.explore.priorityrabbit;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import org.junit.jupiter.api.Test;

/** The whole demo against a real broker; skipped, not failed, when no container runtime is running. */
class DemoRunsTest {

    @Test
    void acts() throws Exception {
        assumeTrue(Broker.containerRuntimeAvailable(), "needs a container runtime");
        String all = String.join("\n", RabbitPriorityQueueDemo.run());
        assertTrue(all.contains("the last same-day order is picked at 9:11"), all);
        assertTrue(all.contains("all 5 same-day orders picked by 9:01"), all);
        assertTrue(all.contains("1000 standard orders ahead of them: same-day still picked by 9:01"), all);
        assertTrue(all.contains("positions 101 to 105 of 105"), all);
        assertTrue(all.contains("the next order the queue will hand out: [SAME-1]"), all);
        assertTrue(all.contains("standard orders picked in 10 minutes: 0 of 20"), all);
        assertTrue(all.contains("2 picks a minute kept for standard: 20 of 20"), all);
    }

    @Test
    void adviceIsASentenceNotAStackTrace() {
        assertTrue(Broker.NO_RUNTIME_ADVICE.contains("Start Docker Desktop"));
    }
}
