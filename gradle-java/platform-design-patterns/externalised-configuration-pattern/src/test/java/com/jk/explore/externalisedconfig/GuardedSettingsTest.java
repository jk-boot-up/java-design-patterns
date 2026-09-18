package com.jk.explore.externalisedconfig;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** The bill, paid. The same two bad values, and a shop that keeps trading. */
class GuardedSettingsTest {

    private static final MoneySetting SETTING = ConfiguredCheckout.FREE_DELIVERY_OVER;
    private static final String KEY = SETTING.key();

    private final ChangeLog log = new ChangeLog();
    private final ConfigServer server =
            new ConfigServer(LocalDateTime.of(2025, 3, 8, 9, 12), log);
    private final GuardedSettings guarded = new GuardedSettings(server);

    @Test
    @DisplayName("a good value is used and says it came from the server")
    void aGoodValueIsUsed() {
        server.set(KEY, "35", "marketing");

        SettingValue value = guarded.money(SETTING);

        assertEquals(Money.pounds(35), value.amount());
        assertEquals("the config server", value.origin());
        assertFalse(guarded.hasRejected());
    }

    @Test
    @DisplayName("minus one is refused and the last good value is kept instead")
    void minusOneIsRefusedAndTheLastGoodValueKept() {
        server.set(KEY, "35", "marketing");
        assertEquals(Money.pounds(35), guarded.money(SETTING).amount());

        server.set(KEY, "-1", "ops");
        SettingValue value = guarded.money(SETTING);

        // Not the default. The promotion is still running, because reverting a
        // good promotion over an unrelated typo would be its own kind of wrong.
        assertEquals(Money.pounds(35), value.amount());
        assertTrue(value.origin().contains("last value that passed validation"));
    }

    @Test
    @DisplayName("the word fifty is refused too, and checkout does not throw")
    void notANumberIsRefusedWithoutThrowing() {
        server.set(KEY, "35", "marketing");
        guarded.money(SETTING);
        server.set(KEY, "fifty", "marketing");

        Checkout checkout = new ConfiguredCheckout(guarded);
        DeliveryQuote quote = checkout.quote(new Basket("ORD-7102", Money.pounds(48)));

        assertTrue(quote.isFree());
        assertEquals(Money.pounds(35), quote.thresholdApplied());
    }

    @Test
    @DisplayName("with no good value ever seen it falls back to the compiled-in default")
    void withNoGoodValueEverItUsesTheDefault() {
        server.set(KEY, "fifty", "marketing");

        SettingValue value = guarded.money(SETTING);

        assertEquals(SETTING.fallback(), value.amount());
        assertTrue(value.origin().contains("default compiled into the code"));
    }

    @Test
    @DisplayName("every rejection is recorded, naming the key and quoting the value")
    void everyRejectionIsRecorded() {
        server.set(KEY, "-1", "ops");
        guarded.money(SETTING);
        server.set(KEY, "fifty", "marketing");
        guarded.money(SETTING);

        assertTrue(guarded.hasRejected());
        assertEquals(2, guarded.rejections().size());
        assertTrue(guarded.rejections().get(0).contains("\"-1\""));
        assertTrue(guarded.rejections().get(0).contains(KEY));
        assertTrue(guarded.rejections().get(1).contains("\"fifty\""));
    }

    @Test
    @DisplayName("an unreachable server keeps the last good value rather than the default")
    void anOutageKeepsTheLastGoodValue() {
        server.set(KEY, "35", "marketing");
        guarded.money(SETTING);
        server.goOffline("the network link to it dropped");

        SettingValue value = guarded.money(SETTING);

        assertEquals(Money.pounds(35), value.amount());
        assertTrue(value.origin().contains("could not be reached"));
        // An outage is not a rejection; nobody typed anything wrong.
        assertFalse(guarded.hasRejected());
    }

    @Test
    @DisplayName("a missing key falls back without being treated as an error")
    void aMissingKeyFallsBackQuietly() {
        SettingValue value = guarded.money(SETTING);

        assertEquals(SETTING.fallback(), value.amount());
        assertTrue(value.origin().contains("has no value for " + KEY));
        assertFalse(guarded.hasRejected());
    }

    @Test
    @DisplayName("the guarded reader describes itself as validating")
    void theReadersDescribeThemselves() {
        assertTrue(guarded.describe().contains("validating"));
        assertTrue(new TrustingSettings(server).describe().contains("no validation"));
    }
}
