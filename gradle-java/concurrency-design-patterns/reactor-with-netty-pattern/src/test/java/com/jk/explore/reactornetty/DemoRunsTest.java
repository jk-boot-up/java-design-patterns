package com.jk.explore.reactornetty;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

/** The whole demo, with a real Netty server on a local port and real TCP clients. */
class DemoRunsTest {

    @Test
    void acts() throws Exception {
        String all = String.join("\n", NettyReactorDemo.run());
        assertTrue(all.contains("till 1 asks \"stock KETTLE-1\": 4"), all);
        assertTrue(all.contains("threads running handlers: 1"), all);
        assertTrue(all.contains("two separate writes: answer 800"), all);
        assertTrue(all.contains("100 tills ask at once: 100 correct answers; threads running handlers: 1"), all);
        assertTrue(all.contains("spread over 4 threads"), all);
        assertTrue(all.contains("it waited over 0.2 s"), all);
        assertTrue(all.contains("with the handler on its own executor group: answered in under 0.2 s"), all);
    }
}
