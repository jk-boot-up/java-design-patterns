package com.jk.explore.deadletterrabbit;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    @Test
    void allSixActsRunInOrder() throws Exception {
        assumeTrue(Broker.dockerAvailable(), "needs a container runtime and the RabbitMQ image");
        String out = Demo.output();
        int at = -1;
        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            int next = out.indexOf(act);
            assertTrue(next > at, "act " + act + " is missing or out of order:\n" + out);
            at = next;
        }
    }

    @Test
    void allThreeReasonsTheBrokerRecordsAreShown() throws Exception {
        assumeTrue(Broker.dockerAvailable(), "needs a container runtime and the RabbitMQ image");
        String out = Demo.output();
        for (String reason : new String[]{"reason rejected", "reason expired", "reason maxlen"}) {
            assertTrue(out.contains(reason), reason + " is missing:\n" + out);
        }
    }
}
