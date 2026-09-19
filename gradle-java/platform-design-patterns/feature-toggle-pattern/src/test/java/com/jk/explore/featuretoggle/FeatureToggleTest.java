package com.jk.explore.featuretoggle;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import java.util.Set;
import org.junit.jupiter.api.Test;

class FeatureToggleTest {

    @Test
    void aSwitchChangesBehaviourWithoutANewCheckout() {
        Toggles t = new Toggles();
        t.define("gift-wrap", new Rule.Off(), 1);
        Checkout c = new Checkout(t, false);
        assertEquals(5000, c.total("c1", 5000));
        t.set("gift-wrap", new Rule.On());
        assertEquals(5300, c.total("c1", 5000));
    }

    @Test
    void percentAndNamedRules() {
        Toggles t = new Toggles();
        t.define("gift-wrap", new Rule.Percent(10), 1);
        assertEquals(10, FeatureToggleDemo.gotIt(t, 100));
        t.set("gift-wrap", new Rule.Only(Set.of("c1", "c2")));
        assertEquals(2, FeatureToggleDemo.gotIt(t, 100));
    }

    @Test
    void theKillSwitchStopsTheFailures() {
        Toggles t = new Toggles();
        t.define("gift-wrap", new Rule.Percent(20), 1);
        Checkout c = new Checkout(t, true);
        assertEquals(20, FeatureToggleDemo.failures(c, 100));
        t.set("gift-wrap", new Rule.Off());
        assertEquals(0, FeatureToggleDemo.failures(c, 100));
    }

    @Test
    void anUnreachableTableOrAnUnknownToggleMeansOff() {
        Toggles t = new Toggles();
        t.define("gift-wrap", new Rule.On(), 1);
        assertTrue(t.isOn("gift-wrap", "c1"));
        t.storeDown();
        assertFalse(t.isOn("gift-wrap", "c1"));
        t.storeUp();
        assertFalse(t.isOn("nothing", "c1"));
    }

    @Test
    void settledOldTogglesAreStale() {
        Toggles t = new Toggles();
        t.define("a", new Rule.On(), 10);
        t.define("b", new Rule.Percent(30), 10);
        t.define("c", new Rule.Off(), 190);
        assertEquals(List.of("a"), t.stale(200, 90));
    }
}
