package com.jk.explore.routingslipcamel;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class SlipWriterTest {

    @Test
    void slipIsCamelEndpointList() {
        assertEquals("direct:validate,direct:charge,direct:pack",
                new SlipWriter().slip(new Order("X", false, false, 30, false, 100)));
    }

    @Test
    void fraudCheckOnlyAfterItIsAdded() {
        SlipWriter w = new SlipWriter();
        Order big = new Order("X", false, false, 30, false, 90000);
        assertEquals(3, w.steps(big).size());
        w.addFraudCheck();
        assertEquals("fraud-check", w.steps(big).get(1));
    }
}
