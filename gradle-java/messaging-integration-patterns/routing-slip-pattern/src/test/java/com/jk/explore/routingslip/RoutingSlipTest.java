package com.jk.explore.routingslip;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import org.junit.jupiter.api.Test;

class RoutingSlipTest {

    private final RoutingSlip r = new RoutingSlip();

    @Test
    void plainOrder() {
        assertEquals(List.of("validate", "charge", "pack"), r.slipFor(new OrderMessage("A", 1, false, false, "UK")));
    }

    @Test
    void giftAbroadAgeRestricted() {
        assertEquals(List.of("validate", "age-check", "customs", "charge", "gift-wrap", "pack"),
                r.slipFor(new OrderMessage("B", 1, true, true, "FR")));
    }

    @Test
    void routeVisitsTheSlipInOrder() {
        OrderMessage m = new OrderMessage("C", 1, true, false, "UK");
        assertEquals("done", r.route(m));
        assertEquals(List.of("validate", "charge", "gift-wrap", "pack"), m.visitedSteps());
    }

    @Test
    void failedStepStopsTheRoute() {
        OrderMessage m = new OrderMessage("D", 1, false, true, "UK");
        m.failAgeCheck();
        assertEquals("stopped at age-check; still on the slip: [charge, pack]", r.route(m));
    }
}
