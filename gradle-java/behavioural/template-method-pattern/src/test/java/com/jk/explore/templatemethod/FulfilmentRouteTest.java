package com.jk.explore.templatemethod;

import java.util.List;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Tests the three shipped routes — what each one does differently, and the
 * one thing they all do the same.
 */
@DisplayName("The three routes")
class FulfilmentRouteTest {

    private static final List<String> THE_SEQUENCE =
            List.of("validate", "reserve", "charge", "pack", "dispatch", "notify");

    private static StockLedger stock() {
        return new StockLedger().stock("H-100", 10).stock("C-220", 4);
    }

    @Nested
    @DisplayName("WarehouseFulfilment")
    class Warehouse {

        private final StockLedger ledger = stock();
        private final FulfilmentProcess route = new WarehouseFulfilment(ledger, "Reading");

        private Order order(int quantity) {
            return Order.shipped("A-1", "grace@example.com", "4 Blackfriars Road, London",
                    List.of(new OrderLine("H-100", "Headphones", Money.pounds(89.99), quantity)));
        }

        @Test
        @DisplayName("holds the stock it reserved")
        void reservesStock() {
            route.fulfil(order(3));
            assertEquals(3, ledger.reservedFor("H-100"));
            assertEquals(7, ledger.available("H-100"));
        }

        @Test
        @DisplayName("refuses an order it cannot cover, and charges nothing")
        void refusesWhenShort() {
            assertThrows(FulfilmentException.class, () -> route.fulfil(order(11)));
            assertEquals(0, ledger.reservedFor("H-100"));
        }

        @Test
        @DisplayName("charges the subtotal")
        void chargesTheSubtotal() {
            assertEquals(Money.pounds(179.98), route.fulfil(order(2)).charged());
        }

        @Test
        @DisplayName("gives the customer a courier consignment to chase")
        void issuesAConsignment() {
            assertEquals("CON-A-1", route.fulfil(order(1)).dispatchReference());
        }

        @Test
        @DisplayName("uses the base class's packing and emailing unchanged")
        void keepsTheDefaults() {
            FulfilmentReport report = route.fulfil(order(2));
            assertEquals("2 item(s) boxed and labelled", report.steps().get(3).detail());
            assertTrue(report.notifications().get(0).contains("is on its way"));
        }

        @Test
        @DisplayName("runs the sequence")
        void runsTheSequence() {
            assertEquals(THE_SEQUENCE, route.fulfil(order(1)).stepNames());
        }
    }

    @Nested
    @DisplayName("MarketplaceFulfilment")
    class Marketplace {

        private final SellerApi seller = new SellerApi("Acme Optics").willConfirm("L-900");
        private final FulfilmentProcess route = new MarketplaceFulfilment(seller);

        private Order order(String sku) {
            return Order.shipped("M-1", "priya@example.com", "12 Mill Lane, Bath",
                    List.of(new OrderLine(sku, "Macro lens", Money.pounds(129.00), 1)));
        }

        @Test
        @DisplayName("asks the seller to confirm every line")
        void asksTheSeller() {
            route.fulfil(order("L-900"));
            assertEquals(1, seller.callCount());
        }

        @Test
        @DisplayName("stops before charging if the seller refuses")
        void stopsWhenTheSellerRefuses() {
            FulfilmentException e = assertThrows(FulfilmentException.class,
                    () -> route.fulfil(order("T-410")));
            assertTrue(e.getMessage().contains("will not confirm"));
        }

        @Test
        @DisplayName("charges the customer the full subtotal")
        void chargesTheSubtotal() {
            assertEquals(Money.pounds(129.00), route.fulfil(order("L-900")).charged());
        }

        @Test
        @DisplayName("records the commission it kept")
        void recordsTheCommission() {
            assertTrue(route.fulfil(order("L-900")).steps().get(2).detail()
                    .contains("£15.48 commission"));
        }

        @Test
        @DisplayName("replaces packing rather than skipping it")
        void replacesPacking() {
            FulfilmentReport report = route.fulfil(order("L-900"));
            assertEquals("pack", report.steps().get(3).name());
            assertTrue(report.steps().get(3).detail().contains("packs their own"));
        }

        @Test
        @DisplayName("posts the commission from the afterFulfilment hook")
        void usesTheHook() {
            assertEquals(List.of("seller ledger: £15.48 commission posted against Acme Optics"),
                    route.fulfil(order("L-900")).notes());
        }

        @Test
        @DisplayName("runs the sequence")
        void runsTheSequence() {
            assertEquals(THE_SEQUENCE, route.fulfil(order("L-900")).stepNames());
        }
    }

    @Nested
    @DisplayName("DigitalFulfilment")
    class Digital {

        private final FulfilmentProcess route = new DigitalFulfilment();

        private Order order() {
            return Order.addressless("D-1", "sam@example.com",
                    List.of(new OrderLine("E-777", "Recipe e-book", Money.pounds(9.99), 1)));
        }

        @Test
        @DisplayName("fulfils an order that has no shipping address")
        void needsNoAddress() {
            assertEquals(THE_SEQUENCE, route.fulfil(order()).stepNames());
        }

        @Test
        @DisplayName("issues a licence key as its dispatch reference")
        void issuesAKey() {
            assertEquals("KEY-D-1-E-777", route.fulfil(order()).dispatchReference());
        }

        @Test
        @DisplayName("emails the key, because dispatch has already run")
        void emailsTheKey() {
            FulfilmentReport report = route.fulfil(order());
            assertEquals(List.of("sam@example.com: Order D-1 is ready to download. "
                    + "Key: KEY-D-1-E-777"), report.notifications());
        }

        @Test
        @DisplayName("records reserve and pack as having nothing to do")
        void recordsTheEmptySteps() {
            FulfilmentReport report = route.fulfil(order());
            assertTrue(report.steps().get(1).detail().contains("nothing to reserve"));
            assertEquals("nothing to pack", report.steps().get(3).detail());
        }

        @Test
        @DisplayName("charges the subtotal")
        void chargesTheSubtotal() {
            assertEquals(Money.pounds(9.99), route.fulfil(order()).charged());
        }
    }

    @Nested
    @DisplayName("all three together")
    class Together {

        @Test
        @DisplayName("produce identical step names from unrelated implementations")
        void identicalSequences() {
            FulfilmentReport warehouse = new WarehouseFulfilment(stock(), "Reading")
                    .fulfil(Order.shipped("A-9", "grace@example.com", "London",
                            List.of(new OrderLine("H-100", "Headphones", Money.pounds(89.99), 1))));
            FulfilmentReport marketplace = new MarketplaceFulfilment(
                    new SellerApi("Acme Optics").willConfirm("L-900"))
                    .fulfil(Order.shipped("M-9", "priya@example.com", "Bath",
                            List.of(new OrderLine("L-900", "Lens", Money.pounds(129.00), 1))));
            FulfilmentReport digital = new DigitalFulfilment()
                    .fulfil(Order.addressless("D-9", "sam@example.com",
                            List.of(new OrderLine("E-777", "E-book", Money.pounds(9.99), 1))));

            assertEquals(warehouse.stepNames(), marketplace.stepNames());
            assertEquals(marketplace.stepNames(), digital.stepNames());
            assertEquals(THE_SEQUENCE, digital.stepNames());
        }
    }
}
