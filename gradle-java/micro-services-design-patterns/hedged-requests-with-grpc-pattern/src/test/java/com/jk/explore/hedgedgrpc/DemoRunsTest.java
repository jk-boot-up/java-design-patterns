package com.jk.explore.hedgedgrpc;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

/** The whole demo, against a real gRPC server on a local port. */
class DemoRunsTest {

    @Test
    void acts() throws Exception {
        String all = String.join("\n", GrpcHedgedRequestsDemo.run());
        assertTrue(all.contains("100 price lookups: 3 took about a second"), all);
        assertTrue(all.contains("100 lookups: 0 took over 0.2 s; extra calls sent by gRPC: 3"), all);
        assertTrue(all.contains("cancelled, and never replied: 3"), all);
        assertTrue(all.contains("100 lookups sent 200 calls"), all);
        assertTrue(all.contains("the server placed 2 orders"), all);
    }
}
