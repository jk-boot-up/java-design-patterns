package com.jk.explore.wiretapcamel;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    @Test
    void acts() throws Exception {
        String all = String.join("\n", CamelWireTapDemo.run());
        assertTrue(all.contains("audit: REFUND ORD-1 £30.00 card **** 1234"));
        assertTrue(all.contains("4 of 4 copied, the refund included; payment handled 4"));
        assertTrue(all.contains("checkout's own ORD-1 message now says: CHARGE ORD-1 £63.44 card **** 1234"));
        assertTrue(all.contains("audit lines: 4; checkout's ORD-1 message still says: CHARGE ORD-1 £63.44 card 4929123412341234"));
        assertTrue(all.contains("ORD-4: charged ORD-4"));
        assertTrue(all.contains("4 payments took under 0.3 s"));
        assertTrue(all.contains("caught up only later: 4 of 4"));
    }
}
