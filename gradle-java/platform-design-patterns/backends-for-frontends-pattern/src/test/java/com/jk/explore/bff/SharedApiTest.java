package com.jk.explore.bff;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class SharedApiTest {

    private final CallLog log = new CallLog();
    private final SharedApi api = new SharedApi(new Shop(log), log);

    @Test
    @DisplayName("it does fix the round trips: one call from the device, five inside")
    void movesTheCallsOffTheCustomersConnection() {
        api.product("SKU-4417");

        assertEquals(1, log.countFrom(CallLog.Origin.DEVICE));
        assertEquals(5, log.countFrom(CallLog.Origin.INTERNAL));
    }

    @Test
    @DisplayName("most of what the phone downloads from it is never drawn")
    void sendsFarMoreThanThePhoneDraws() {
        Doc union = api.product("SKU-4417");
        Doc drawn = union.select(Screens.PHONE_ON_SHARED_API);

        assertTrue(drawn.bytes() * 4 < union.bytes(),
                "drawn " + drawn.bytes() + " bytes of " + union.bytes());
    }

    @Test
    @DisplayName("a fields parameter genuinely fixes the size, and that is worth admitting")
    void fieldFilteringWorks() {
        Doc trimmed = api.product("SKU-4417", Screens.PHONE_ON_SHARED_API);

        assertEquals(Screens.PHONE_ON_SHARED_API.size(), trimmed.paths().size());
        assertTrue(trimmed.bytes() < api.product("SKU-4417").bytes() / 4);
    }

    @Test
    @DisplayName("what it cannot give is a field that belongs to one client")
    void cannotServeAClientSpecificField() {
        assertTrue(SharedApi.joinedDelivery().startsWith("not available"));
    }
}
