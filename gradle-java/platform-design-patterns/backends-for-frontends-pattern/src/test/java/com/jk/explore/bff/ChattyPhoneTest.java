package com.jk.explore.bff;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class ChattyPhoneTest {

    private final CallLog log = new CallLog();
    private final ChattyPhone phone = new ChattyPhone(new Shop(log), log);

    @Test
    @DisplayName("one product screen costs five round trips over the customer's connection")
    void makesFiveCallsFromTheDevice() {
        phone.productScreen("SKU-4417");

        assertEquals(5, log.countFrom(CallLog.Origin.DEVICE));
        assertEquals(
                List.of("catalog", "pricing", "inventory", "reviews", "recommendations"),
                log.targetsFrom(CallLog.Origin.DEVICE));
    }

    @Test
    @DisplayName("far more arrives than the screen has room to draw")
    void downloadsMuchMoreThanItDraws() {
        Doc everything = phone.productScreen("SKU-4417");

        assertTrue(everything.paths().size() > Screens.PHONE.size() * 4,
                "the phone draws " + Screens.PHONE.size() + " fields and received "
                        + everything.paths().size());
    }
}
