package com.jk.explore.boundedcontext;

import com.jk.explore.boundedcontext.naive.GodCustomer;
import com.jk.explore.boundedcontext.sales.Buyer;
import com.jk.explore.boundedcontext.sales.SalesContext;
import com.jk.explore.boundedcontext.shared.CustomerId;
import com.jk.explore.boundedcontext.shared.EventBus;
import com.jk.explore.boundedcontext.shipping.Recipient;
import com.jk.explore.boundedcontext.shipping.ShippingContext;
import com.jk.explore.boundedcontext.support.Contact;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.time.LocalDate;

import static com.jk.explore.boundedcontext.BoundedContextDemo.ADA;
import static com.jk.explore.boundedcontext.BoundedContextDemo.TODAY;
import static org.junit.jupiter.api.Assertions.*;

class BoundedContextTest {

    @Test
    void theSameCustomerIsActiveInOneContextAndNotInAnother() {
        assertTrue(new Buyer(ADA, "Ada", 1, LocalDate.of(2026, 8, 1)).isActive(TODAY));
        assertFalse(new Buyer(ADA, "Ada", 1, LocalDate.of(2026, 5, 1)).isActive(TODAY));
        assertTrue(new Recipient(ADA, "Ada", "x", 1).isActive());
        assertFalse(new Contact(ADA, "Ada", "0", 0).isActive());
    }

    @Test
    void theNinetyDayBoundaryIsInclusive() {
        assertTrue(new Buyer(ADA, "Ada", 1, TODAY.minusDays(90)).isActive(TODAY));
        assertFalse(new Buyer(ADA, "Ada", 1, TODAY.minusDays(91)).isActive(TODAY));
    }

    @Test
    void aRenameReachesShippingOnlyWhenTheEventIsDelivered() {
        EventBus bus = new EventBus();
        SalesContext sales = new SalesContext(bus);
        ShippingContext shipping = new ShippingContext(bus);
        sales.register(new Buyer(ADA, "Ada Lovelace", 1, TODAY));
        shipping.register(new Recipient(ADA, "Ada Lovelace", "12 Byron Road", 0));
        sales.rename(ADA, "Ada King");
        assertEquals("Ada King", sales.buyer(ADA).name());
        assertEquals("Ada Lovelace", shipping.recipient(ADA).name());
        assertEquals(1, bus.waiting());
        bus.deliver();
        assertEquals("Ada King", shipping.recipient(ADA).name());
        assertEquals("12 Byron Road", shipping.recipient(ADA).address());
    }

    @Test
    void anEventForAnUnknownCustomerIsIgnored() {
        EventBus bus = new EventBus();
        SalesContext sales = new SalesContext(bus);
        new ShippingContext(bus);
        sales.register(new Buyer(new CustomerId("bo"), "Bo", 1, TODAY));
        sales.rename(new CustomerId("bo"), "Bo Peep");
        assertDoesNotThrow(bus::deliver);
    }

    @Test
    void noContextImportsAnothersTypes() throws IOException {
        assertEquals(0, BoundedContextDemo.crossImports());
    }

    @Test
    void theCompanyWideClassIsWide() {
        assertEquals(12, GodCustomer.fieldCount());
    }
}
