package com.jk.explore.requestreplyrabbit;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import org.junit.jupiter.api.Test;

/** The whole demo against a real broker; skipped, not failed, when no container runtime is running. */
class DemoRunsTest {

    @Test
    void acts() throws Exception {
        assumeTrue(Broker.containerRuntimeAvailable(), "needs a container runtime");
        String all = String.join("\n", RabbitRequestReplyDemo.run());
        assertTrue(all.contains("reserve KETTLE-1 x 5 -> RESERVED 2 x MUG-1"), all);
        assertTrue(all.contains("WEB-1 reserve KETTLE-1 x 5 -> REFUSED 5 x KETTLE-1"), all);
        assertTrue(all.contains("WEB-2 reserve MUG-1 x 2    -> RESERVED 2 x MUG-1"), all);
        assertTrue(all.contains("phone app APP-1 -> RESERVED 1 x TEAPOT-1"), all);
        assertTrue(all.contains("web checkout WEB-3 -> RESERVED 2 x TEAPOT-1"), all);
        assertTrue(all.contains("the service handled 20"), all);
        assertTrue(all.contains("requests still waiting: 0"), all);
        assertTrue(all.contains("WEB-24: no reply after 0.5 s"), all);
        assertTrue(all.contains("when the service returns it handles 0"), all);
    }

    @Test
    void adviceIsASentenceNotAStackTrace() {
        assertTrue(Broker.NO_RUNTIME_ADVICE.contains("Start Docker Desktop"));
    }
}
