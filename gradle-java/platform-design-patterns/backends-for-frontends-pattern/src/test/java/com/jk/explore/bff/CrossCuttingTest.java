package com.jk.explore.bff;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class CrossCuttingTest {

    @Test
    @DisplayName("doing the shared jobs in each backend multiplies them by the client count")
    void copiesGrowWithTheNumberOfBackends() {
        assertEquals(8, CrossCutting.copiesWhenEachBackendDoesIt(2));
        assertEquals(24, CrossCutting.copiesWhenEachBackendDoesIt(6));
    }

    @Test
    @DisplayName("behind a gateway the count does not depend on the number of backends at all")
    void copiesBehindAGatewayAreConstant() {
        assertEquals(CrossCutting.JOBS.size(), CrossCutting.copiesBehindAGateway());
        assertTrue(CrossCutting.copiesBehindAGateway()
                < CrossCutting.copiesWhenEachBackendDoesIt(2));
    }
}
