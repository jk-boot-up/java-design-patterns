package com.jk.explore.remotefacade;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

class OrderFacadeTest {

    @Test
    void summaryHasTheWholeScreen() {
        assertEquals("ORD-1 | Priya | kettle, 2 x mug | £46.00 | 4 Mill Lane, Leeds | Mon 9-12",
                OrderFacade.summary(new Order()));
    }

    @Test
    void badSlotChangesNothing() {
        Order o = new Order();
        assertThrows(IllegalArgumentException.class, () -> OrderFacade.changeDelivery(o, "York", "Sun 9-12"));
        assertEquals("4 Mill Lane, Leeds", o.address());
        assertEquals("Mon 9-12", o.slot());
    }

    @Test
    void goodChangeChangesBoth() {
        Order o = new Order();
        OrderFacade.changeDelivery(o, "York", "Tue 9-12");
        assertEquals("York", o.address());
        assertEquals("Tue 9-12", o.slot());
    }
}
