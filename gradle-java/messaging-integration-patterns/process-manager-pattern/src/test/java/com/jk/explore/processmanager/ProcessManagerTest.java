package com.jk.explore.processmanager;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.Map;
import java.util.Set;
import org.junit.jupiter.api.Test;

class ProcessManagerTest {

    private final Services.Warehouse main = new Services.Warehouse("main", Map.of("KETTLE-1", 1, "SOFA-1", 0, "LAMP-1", 0));
    private final Services.Warehouse partner = new Services.Warehouse("partner", Map.of("SOFA-1", 1));
    private final Services.Emails emails = new Services.Emails();
    private final ProcessManager pm = new ProcessManager(main, partner, new Services.Payments(Set.of("BAD")),
            new Services.Shipping(), emails);

    @Test
    void happyPath() {
        pm.start(new Order("A", "KETTLE-1", "OK"));
        assertEquals("DONE", pm.state("A"));
        assertEquals(0, main.stock("KETTLE-1"));
    }

    @Test
    void fallsBackToPartner() {
        pm.start(new Order("B", "SOFA-1", "OK"));
        assertEquals("DONE", pm.state("B"));
        assertEquals(0, partner.stock("SOFA-1"));
    }

    @Test
    void declinedPaymentReleasesStock() {
        pm.start(new Order("C", "KETTLE-1", "BAD"));
        assertEquals(1, main.stock("KETTLE-1"));
        assertEquals("C: your card was declined", emails.sent().get(0));
    }

    @Test
    void noStockAnywhereCancels() {
        pm.start(new Order("D", "LAMP-1", "OK"));
        assertEquals("CANCELLED: no stock anywhere", pm.state("D"));
    }
}
