package com.jk.explore.bff;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class WebBffTest {

    private final CallLog log = new CallLog();
    private final WebBff web = new WebBff(new Shop(log), log);

    @Test
    @DisplayName("it sends exactly the fields the desktop page draws")
    void sendsWhatTheDesktopPageDraws() {
        assertEquals(Screens.DESKTOP, web.productScreen("SKU-4417").names());
    }

    @Test
    @DisplayName("it calls all five services, because this page shows all five")
    void callsEveryService() {
        web.productScreen("SKU-4417");

        assertEquals(1, log.countFrom(CallLog.Origin.DEVICE));
        assertEquals(5, log.countFrom(CallLog.Origin.INTERNAL));
    }

    @Test
    @DisplayName("the two backends disagree about what a product is, which is the pattern working")
    void disagreesWithThePhonesBackend() {
        CallLog phoneLog = new CallLog();
        Doc phoneScreen = new MobileBff(new Shop(phoneLog), phoneLog).productScreen("SKU-4417");
        Doc page = web.productScreen("SKU-4417");

        assertNotEquals(phoneScreen.names(), page.names());
        assertTrue(page.bytes() > phoneScreen.bytes() * 3);
    }

    @Test
    @DisplayName("it claims no saving, because the higher price is too recent to quote")
    void makesNoSavingClaimItIsNotEntitledTo() {
        assertEquals("", web.productScreen("SKU-4417").get("saving"));
        assertEquals("", web.savingLabel("SKU-4417"));
    }

    @Test
    @DisplayName("both prices are formatted here, not on the page")
    void formatsBothPrices() {
        Doc page = web.productScreen("SKU-4417");

        assertEquals("£47.99", page.get("price"));
        assertEquals("£59.99", page.get("wasPrice"));
    }
}
