package com.jk.explore.wiretap;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.Test;

class WireTapTest {

    @Test
    void tapCopiesWithoutChangingDelivery() {
        PaymentService p = new PaymentService(null);
        Channel c = new Channel(p);
        WireTaps.AuditLog a = new WireTaps.AuditLog(true);
        c.attach(a);
        WireTapDemo.TRAFFIC.forEach(c::send);
        assertEquals(4, a.lines().size());
        assertEquals(List.of("charged ORD-1", "charged ORD-2", "refunded ORD-1", "charged ORD-3"), p.handled());
    }

    @Test
    void cardNumbersAreMasked() {
        WireTaps.AuditLog a = new WireTaps.AuditLog(true);
        a.accept(WireTapDemo.TRAFFIC.get(0));
        assertTrue(a.lines().get(0).endsWith("card **** 1234"));
    }

    @Test
    void meterAddsChargesAndSubtractsRefunds() {
        WireTaps.SalesMeter m = new WireTaps.SalesMeter();
        WireTapDemo.TRAFFIC.forEach(m);
        assertEquals(6344 + 1999 - 3000 + 499, m.net());
    }

    @Test
    void detachedTapSeesNothing() {
        Channel c = new Channel(new PaymentService(null));
        WireTaps.AuditLog a = new WireTaps.AuditLog(true);
        c.attach(a);
        c.detach(a);
        c.send(WireTapDemo.TRAFFIC.get(0));
        assertEquals(0, a.lines().size());
    }
}
