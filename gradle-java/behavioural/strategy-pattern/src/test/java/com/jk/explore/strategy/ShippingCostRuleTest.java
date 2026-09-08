package com.jk.explore.strategy;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Each rule tested on its own, which is the practical benefit the pattern
 * buys: none of these tests has to go through checkout, and none of them has
 * to supply the fields its rule does not read.
 */
class ShippingCostRuleTest {

    /** Weight and distance vary per test; only the field under test matters. */
    private static Shipment shipment(double kg, int miles, double subtotal) {
        return new Shipment("Cardiff", kg, miles, Money.pounds(subtotal));
    }

    @Nested
    class FlatRate {

        private final ShippingCostRule rule = new FlatRateRule(Money.pounds(4.99));

        @Test
        @DisplayName("charges the same whatever the parcel")
        void ignoresEveryField() {
            assertEquals(Money.pounds(4.99), rule.costFor(shipment(0.1, 5, 10)));
            assertEquals(Money.pounds(4.99), rule.costFor(shipment(30.0, 900, 500)));
        }
    }

    @Nested
    class WeightBanded {

        private final ShippingCostRule rule = WeightBandedRule.standard();

        @Test
        @DisplayName("prices each band")
        void pricesEachBand() {
            assertEquals(Money.pounds(3.50), rule.costFor(shipment(0.4, 0, 0.01)));
            assertEquals(Money.pounds(6.00), rule.costFor(shipment(3.0, 0, 0.01)));
            assertEquals(Money.pounds(12.00), rule.costFor(shipment(15.0, 0, 0.01)));
            assertEquals(Money.pounds(25.00), rule.costFor(shipment(24.0, 0, 0.01)));
        }

        @Test
        @DisplayName("a band's upper limit is inclusive")
        void upperLimitIsInclusive() {
            assertEquals(Money.pounds(3.50), rule.costFor(shipment(1.0, 0, 0.01)));
            assertNotEquals(Money.pounds(3.50), rule.costFor(shipment(1.01, 0, 0.01)));
        }
    }

    @Nested
    class DistanceBased {

        private final ShippingCostRule rule = DistanceBasedRule.standard();

        @Test
        @DisplayName("charges the base fee plus one unit per hundred miles")
        void chargesPerHundredMiles() {
            assertEquals(Money.pounds(3.50), rule.costFor(shipment(1, 100, 0.01)));
            assertEquals(Money.pounds(5.00), rule.costFor(shipment(1, 200, 0.01)));
        }

        @Test
        @DisplayName("a part-hundred rounds up to a whole unit")
        void roundsPartUnitsUp() {
            // 101 miles and 200 miles cost the same. That is a deliberate
            // decision, and having it in its own test is the point: inside a
            // shared switch it would be an unexplained `+ 99`.
            assertEquals(rule.costFor(shipment(1, 200, 0.01)),
                    rule.costFor(shipment(1, 101, 0.01)));
        }

        @Test
        @DisplayName("zero miles costs only the base fee")
        void zeroMilesIsBaseFeeOnly() {
            assertEquals(Money.pounds(2.00), rule.costFor(shipment(1, 0, 0.01)));
        }
    }

    @Nested
    class FreeOverThreshold {

        private final ShippingCostRule rule = FreeOverThresholdRule.standard();

        @Test
        @DisplayName("free at and above the threshold, charged below it")
        void freeAboveThreshold() {
            assertTrue(rule.costFor(shipment(1, 10, 50.00)).isZero(), "exactly at threshold");
            assertTrue(rule.costFor(shipment(1, 10, 64.00)).isZero(), "above threshold");
            assertEquals(Money.pounds(4.99), rule.costFor(shipment(1, 10, 49.99)));
        }

        @Test
        @DisplayName("reads the order value, not the parcel")
        void ignoresWeightAndDistance() {
            assertEquals(rule.costFor(shipment(0.1, 1, 20.00)),
                    rule.costFor(shipment(30.0, 900, 20.00)));
        }
    }
}
