package com.jk.explore.bff;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class MobileBffTest {

    private final CallLog log = new CallLog();
    private final MobileBff phone = new MobileBff(new Shop(log), log);

    @Test
    @DisplayName("it sends exactly the fields the screen draws, and nothing else")
    void sendsOnlyWhatIsDrawn() {
        Doc screen = phone.productScreen("SKU-4417");

        assertEquals(Screens.PHONE, screen.paths());
    }

    @Test
    @DisplayName("one call from the phone, four inside the data centre")
    void oneRoundTripForTheCustomer() {
        phone.productScreen("SKU-4417");

        assertEquals(1, log.countFrom(CallLog.Origin.DEVICE));
        assertEquals(4, log.countFrom(CallLog.Origin.INTERNAL));
    }

    @Test
    @DisplayName("it does not call recommendations, because this screen does not show them")
    void skipsTheServiceItDoesNotNeed() {
        phone.productScreen("SKU-4417");

        assertTrue(!log.targetsFrom(CallLog.Origin.INTERNAL).contains("recommendations"));
    }

    @Test
    @DisplayName("the price arrives formatted, so the app decides nothing about money")
    void formatsThePrice() {
        assertEquals("£47.99", phone.productScreen("SKU-4417").get("price"));
    }

    @Test
    @DisplayName("delivery is one sentence, joined here from stock and a date")
    void joinsTheDeliveryPromise() {
        assertEquals("Free delivery, arrives 2026-09-18",
                phone.productScreen("SKU-4417").get("delivery"));
    }

    @Test
    @DisplayName("it is a fraction of the size of the shared endpoint's document")
    void isMuchSmallerThanTheSharedDocument() {
        CallLog sharedLog = new CallLog();
        Doc shared = new SharedApi(new Shop(sharedLog), sharedLog).product("SKU-4417");

        assertTrue(phone.productScreen("SKU-4417").bytes() * 5 < shared.bytes());
    }
}
