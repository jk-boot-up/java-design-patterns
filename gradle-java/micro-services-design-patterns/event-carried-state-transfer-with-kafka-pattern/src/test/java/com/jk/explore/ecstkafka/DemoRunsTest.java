package com.jk.explore.ecstkafka;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import org.junit.jupiter.api.Test;

/** The whole demo against a real Kafka broker; skipped, not failed, when no container runtime is running. */
class DemoRunsTest {

    @Test
    void acts() throws Exception {
        assumeTrue(Kafka.containerRuntimeAvailable(), "needs a container runtime");
        String all = String.join("\n", KafkaEventCarriedDemo.run());
        assertTrue(all.contains("100 labels: 100 printed, 100 calls to the customer service"), all);
        assertTrue(all.contains("customer service down: 0 of 100 printed"), all);
        assertTrue(all.contains("customer service still down: 100 of 100 labels printed, 0 calls"), all);
        assertTrue(all.contains("11 events, 10 customers"), all);
        assertTrue(all.contains("C1's label: ORD-1 -> 9 Mill Lane, York"), all);
        assertTrue(all.contains("read partition 1 first: ORD-2 -> 1 Park Road, Hull"), all);
        assertTrue(all.contains("in order: ORD-2 -> 4 Quay Street, Bristol"), all);
        assertTrue(all.contains("the copy now holds 9 addresses; C3 now has no label: true"), all);
    }

    @Test
    void adviceIsASentenceNotAStackTrace() {
        assertTrue(Kafka.NO_RUNTIME_ADVICE.contains("Start Docker Desktop"));
    }
}
