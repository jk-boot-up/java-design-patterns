package com.jk.explore.filtercamel;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    @Test
    void acts() throws Exception {
        String all = String.join("\n", CamelFilterDemo.run());
        assertTrue(all.contains("gift-wrap service handed 10 orders"));
        assertTrue(all.contains("gift-wrap service receives: [ORD-2, ORD-4]; the filter dropped 8"));
        assertTrue(all.contains("loyalty service receives: [ORD-1, ORD-4, ORD-6]"));
        assertTrue(all.contains("threshold raised to £60: [ORD-1, ORD-4]"));
        assertTrue(all.contains("kept on direct:discard: 8 [ORD-2, ORD-3, ORD-5, ORD-6, ORD-7, ORD-8, ORD-9, ORD-10]"));
        assertTrue(all.contains("more than 10 library files"));
    }
}
