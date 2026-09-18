package com.jk.explore.externalisedconfig;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The declared setting is the replacement for the compiler, so these tests are
 * the replacement for "it would not have compiled".
 */
class MoneySettingTest {

    private final MoneySetting setting = ConfiguredCheckout.FREE_DELIVERY_OVER;

    @Test
    @DisplayName("a sensible value in range is accepted")
    void aSensibleValueIsAccepted() {
        assertEquals(Money.pounds(35), setting.read("35"));
        assertEquals(Money.pounds(5), setting.read("5"));
        assertEquals(Money.pounds(200), setting.read("200"));
        assertTrue(setting.accepts("35.00"));
    }

    @Test
    @DisplayName("text that is not a number is refused, and the message says what was wanted")
    void notANumberIsRefused() {
        InvalidSettingException thrown =
                assertThrows(InvalidSettingException.class, () -> setting.read("fifty"));

        assertEquals("delivery.freeOver", thrown.key());
        assertEquals("fifty", thrown.offendingValue());
        assertTrue(thrown.getMessage().contains("expected an amount of money"));
        assertFalse(setting.accepts("fifty"));
    }

    @Test
    @DisplayName("minus one parses fine and is refused anyway, because it is out of range")
    void minusOneIsRefusedByTheRange() {
        // This is the case a type alone would not catch. -1 is money; it is just
        // not a threshold any shop means.
        assertTrue(Money.parse("-1").isPresent());

        InvalidSettingException thrown =
                assertThrows(InvalidSettingException.class, () -> setting.read("-1"));

        assertTrue(thrown.getMessage().contains("expected between £5.00 and £200.00"));
        assertFalse(setting.accepts("-1"));
    }

    @Test
    @DisplayName("a value above the top of the range is refused too")
    void tooLargeIsRefused() {
        assertFalse(setting.accepts("5000"));
        assertThrows(InvalidSettingException.class, () -> setting.read("201"));
    }

    @Test
    @DisplayName("the setting can describe its own range for a schema document")
    void theSettingDescribesItself() {
        assertEquals("£5.00 to £200.00", setting.describeRange());
        assertEquals(Money.pounds(50), setting.fallback());
    }
}
