package com.jk.explore.externalisedconfig;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * What externalising a value costs you, written down as tests rather than as a
 * warning in a document.
 *
 * <p>Both of these pass. That is the uncomfortable part. Neither of them
 * describes a bug in the pattern or a bug in this code — they describe the
 * pattern working exactly as designed, with a value somebody typed wrongly, and
 * they are the reason {@link GuardedSettings} exists.
 */
class TheBillTest {

    private static final String KEY = "delivery.freeOver";

    private final ChangeLog log = new ChangeLog();
    private final ConfigServer server =
            new ConfigServer(LocalDateTime.of(2025, 3, 8, 9, 12), log);
    private final Checkout checkout = new ConfiguredCheckout(new TrustingSettings(server));

    private static final List<Basket> BASKETS = List.of(
            new Basket("ORD-7101", Money.pounds(62)),
            new Basket("ORD-7102", Money.pounds(48)),
            new Basket("ORD-7103", Money.pence(3150)));

    @Test
    @DisplayName("a threshold of -1 gives every basket in the shop free delivery, silently")
    void minusOneGivesEverythingAway() {
        server.set(KEY, "-1", "marketing");

        for (Basket basket : BASKETS) {
            DeliveryQuote quote = checkout.quote(basket);
            assertTrue(quote.isFree(), basket.orderId() + " should have shipped free");
            // No exception, no warning, nothing in any log. The shop is simply
            // giving delivery away and the only symptom is the margin.
            assertTrue(quote.thresholdApplied().isNegative());
        }
    }

    @Test
    @DisplayName("a threshold that is not a number takes checkout down for every customer")
    void notANumberTakesTheShopDown() {
        server.set(KEY, "fifty", "marketing");

        for (Basket basket : BASKETS) {
            assertThrows(InvalidSettingException.class, () -> checkout.quote(basket),
                    basket.orderId() + " should have failed to quote");
        }
    }

    @Test
    @DisplayName("both bad values were in force four seconds after somebody typed them")
    void theBillArrivesInSeconds() {
        LocalDateTime before = server.now();
        ConfigChange change = server.set(KEY, "-1", "marketing");

        assertTrue(change.at().equals(before.plusSeconds(4)));
        // Four seconds, with no compiler, no reviewer and no test suite in the way.
        // The release pipeline the pattern replaced would have taken 2h15m of work.
        assertTrue(ReleasePipeline.typical().totalWork().toMinutes() == 135);
    }
}
