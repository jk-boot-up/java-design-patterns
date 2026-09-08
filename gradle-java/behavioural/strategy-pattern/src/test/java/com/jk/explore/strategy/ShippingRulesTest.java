package com.jk.explore.strategy;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ShippingRulesTest {

    @Test
    @DisplayName("every registered name resolves to a rule")
    void resolvesEveryRegisteredName() {
        assertEquals(4, ShippingRules.names().size());
        for (String key : ShippingRules.names()) {
            assertNotNull(ShippingRules.byName(key), key);
        }
    }

    @Test
    @DisplayName("an unknown name is refused rather than defaulted")
    void refusesUnknownNames() {
        // The naive design's `default` branch charged nothing for an
        // unrecognised method. Failing loudly is the difference between a
        // deployment that breaks and a shop that quietly ships for free.
        IllegalArgumentException thrown = assertThrows(IllegalArgumentException.class,
                () -> ShippingRules.byName("second-class"));

        assertTrue(thrown.getMessage().contains("second-class"),
                "the message must name the value that was not recognised");
        assertTrue(thrown.getMessage().contains("flat"),
                "and should list what was available");
    }

    @Test
    @DisplayName("the rule set cannot be modified through the exposed names")
    void namesAreNotAWayIn() {
        assertThrows(UnsupportedOperationException.class,
                () -> ShippingRules.names().add("smuggled"));
    }
}
