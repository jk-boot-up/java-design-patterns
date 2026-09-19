package com.jk.explore.bluegreen;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.Test;

class BlueGreenTest {

    @Test
    void inPlaceUpgradeFailsRequestsWhileDown() {
        assertEquals(10, new InPlaceUpgrade(10).run(100));
    }

    @Test
    void aGoodSwitchFailsNothing() {
        Router r = new Router(Version.good("v1"), Version.good("v2"));
        r.setGreenPercent(100);
        for (int i = 0; i < 100; i++) {
            r.route(i, Router.orderCents(i));
        }
        assertEquals(0, r.failures());
        assertEquals(100, r.green().served());
    }

    @Test
    void goingBackStopsTheFailures() {
        Router r = new Router(Version.good("v1"), Version.buggy("v2"));
        r.setGreenPercent(100);
        for (int i = 0; i < 50; i++) {
            r.route(i, Router.orderCents(i));
        }
        assertEquals(5, r.failures());
        r.setGreenPercent(0);
        for (int i = 50; i < 100; i++) {
            r.route(i, Router.orderCents(i));
        }
        assertEquals(5, r.failures());
    }

    @Test
    void aCanarySeesFewFailures() {
        Router r = new Router(Version.good("v1"), Version.buggy("v2"));
        r.setGreenPercent(5);
        for (int i = 0; i < 200; i++) {
            r.route(i, Router.orderCents(i));
        }
        assertEquals(10, r.green().served());
        assertEquals(2, r.failures());
    }

    @Test
    void theGateHaltsABadReleaseAndPromotesAGoodOne() {
        Router bad = new Router(Version.good("v1"), Version.buggy("v2"));
        CanaryRollout a = new CanaryRollout(bad, 5);
        a.run(List.of(5, 25, 50, 100), 100);
        assertTrue(a.halted());
        assertEquals(1, a.stepsDone());
        assertEquals(0, bad.greenPercent());
        Router good = new Router(Version.good("v1"), Version.good("v2"));
        CanaryRollout b = new CanaryRollout(good, 5);
        b.run(List.of(5, 25, 50, 100), 100);
        assertFalse(b.halted());
        assertEquals(100, good.greenPercent());
    }
}
