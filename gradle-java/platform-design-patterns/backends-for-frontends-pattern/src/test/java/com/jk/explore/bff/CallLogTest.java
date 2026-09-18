package com.jk.explore.bff;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class CallLogTest {

    @Test
    @DisplayName("calls from the device and calls inside the data centre are counted apart")
    void countsTheTwoNetworksSeparately() {
        CallLog log = new CallLog();
        log.record(CallLog.Origin.DEVICE, "mobile-bff");
        log.record(CallLog.Origin.INTERNAL, "catalog");
        log.record(CallLog.Origin.INTERNAL, "pricing");

        assertEquals(1, log.countFrom(CallLog.Origin.DEVICE));
        assertEquals(2, log.countFrom(CallLog.Origin.INTERNAL));
    }

    @Test
    @DisplayName("calls are kept in the order they happened")
    void keepsOrder() {
        CallLog log = new CallLog();
        log.record(CallLog.Origin.INTERNAL, "catalog");
        log.record(CallLog.Origin.INTERNAL, "pricing");

        assertEquals(List.of("catalog", "pricing"), log.targetsFrom(CallLog.Origin.INTERNAL));
    }
}
