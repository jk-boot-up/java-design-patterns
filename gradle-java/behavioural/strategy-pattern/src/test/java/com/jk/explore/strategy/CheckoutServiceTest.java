package com.jk.explore.strategy;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

/**
 * The interaction tests.
 *
 * <p>These are the ones that would still fail if somebody replaced the four
 * rule classes with a {@code switch} inside {@link CheckoutService}. Tests
 * that only check the arithmetic would not: "a 6.5 kg parcel costs £12.00" is
 * true of the naive design too, so on its own it proves nothing about whether
 * the pattern was applied.
 */
class CheckoutServiceTest {

    private static final Shipment PARCEL =
            new Shipment("Cardiff", 6.5, 180, Money.pounds(64.00));

    @Test
    @DisplayName("a rule the production code has never heard of works unchanged")
    void acceptsARuleDefinedEntirelyInThisTest() {
        // Nothing in src/main knows this rule exists. If CheckoutService
        // branched on a known set of methods, this could not compile or could
        // not pass -- which is exactly the property being asserted.
        ShippingCostRule pricePerKilo = new ShippingCostRule() {
            @Override
            public String name() {
                return "Per kilo";
            }

            @Override
            public Money costFor(Shipment shipment) {
                return Money.pounds(shipment.weightKg());
            }
        };

        Quote quote = new CheckoutService(pricePerKilo).quote(PARCEL);

        assertEquals("Per kilo", quote.ruleName());
        assertEquals(Money.pounds(6.50), quote.delivery());
    }

    @Test
    @DisplayName("the rule is consulted exactly once per quote")
    void callsTheRuleExactlyOnce() {
        AtomicInteger calls = new AtomicInteger();
        ShippingCostRule counting = new ShippingCostRule() {
            @Override
            public String name() {
                return "Counting";
            }

            @Override
            public Money costFor(Shipment shipment) {
                calls.incrementAndGet();
                return Money.pounds(1.00);
            }
        };

        new CheckoutService(counting).quote(PARCEL);

        assertEquals(1, calls.get(), "a rule called twice would double-charge a stateful rule");
    }

    @Test
    @DisplayName("every registered rule is substitutable for every other")
    void allRulesAreInterchangeable() {
        for (String key : ShippingRules.names()) {
            CheckoutService checkout = new CheckoutService(ShippingRules.byName(key));

            Quote quote = checkout.quote(PARCEL);

            assertEquals(PARCEL.orderSubtotal(), quote.subtotal(), key);
            assertEquals(quote.subtotal().plus(quote.delivery()), quote.total(), key);
        }
    }

    @Test
    @DisplayName("the quote carries the name of the rule that priced it")
    void reportsWhichRuleApplied() {
        CheckoutService checkout = new CheckoutService(WeightBandedRule.standard());

        assertEquals("Weight banded", checkout.quote(PARCEL).ruleName());
        assertEquals("Weight banded", checkout.ruleName());
    }

    @Test
    @DisplayName("a null rule is refused at construction, not at first use")
    void refusesANullRule() {
        assertThrows(NullPointerException.class, () -> new CheckoutService(null));
    }

    @Test
    @DisplayName("a null shipment is refused")
    void refusesANullShipment() {
        CheckoutService checkout = new CheckoutService(new FlatRateRule(Money.pounds(4.99)));

        assertThrows(NullPointerException.class, () -> checkout.quote(null));
    }
}
