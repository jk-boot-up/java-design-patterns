package com.jk.explore.hexagonal;

import com.jk.explore.hexagonal.adapter.notification.InMemoryNotifier;
import com.jk.explore.hexagonal.adapter.payment.InMemoryPaymentGateway;
import com.jk.explore.hexagonal.adapter.persistence.InMemoryOrderStore;
import com.jk.explore.hexagonal.adapter.persistence.InMemoryProductCatalog;
import com.jk.explore.hexagonal.core.PlaceOrderRequest;
import com.jk.explore.hexagonal.core.PlaceOrderRequest.RequestedLine;
import com.jk.explore.hexagonal.core.PlaceOrderResult;
import com.jk.explore.hexagonal.core.PlaceOrderService;
import com.jk.explore.hexagonal.core.domain.Money;
import com.jk.explore.hexagonal.core.port.OrderStore;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The core's use case, tested against nothing but ports — no adapter
 * needs to be constructed with any concrete behaviour beyond the in-memory
 * ones the core cannot tell apart from a real database.
 */
class PlaceOrderServiceTest {

    private PlaceOrderService serviceWith(InMemoryPaymentGateway payments) {
        return new PlaceOrderService(InMemoryProductCatalog.seeded(),
                new InMemoryOrderStore(), payments, new InMemoryNotifier());
    }

    @Test
    void threeLinesPriceToTheExpectedTotal() {
        PlaceOrderResult result = serviceWith(InMemoryPaymentGateway.working()).place(
                PlaceOrderRequest.of("cust-8801",
                        new RequestedLine("ESP-001", 1),
                        new RequestedLine("GRD-014", 1),
                        new RequestedLine("BNS-220", 2)),
                "ada@example.com");

        assertTrue(result.placed());
        assertEquals(Money.pounds(382, 50), result.total());
    }

    @Test
    void notEnoughStockIsRefusedBeforeAnyCharge() {
        InMemoryPaymentGateway payments = InMemoryPaymentGateway.working();
        PlaceOrderResult result = serviceWith(payments).place(
                PlaceOrderRequest.of("cust-8801", new RequestedLine("GRD-014", 3)),
                "ada@example.com");

        assertFalse(result.placed());
        assertEquals("only 2 of GRD-014 left", result.reason());
        assertTrue(payments.charges().isEmpty());
    }

    @Test
    void unknownProductIsRefused() {
        PlaceOrderResult result = serviceWith(InMemoryPaymentGateway.working()).place(
                PlaceOrderRequest.of("cust-8801", new RequestedLine("XXX-999", 1)),
                "ada@example.com");

        assertFalse(result.placed());
        assertEquals("no such product: XXX-999", result.reason());
    }

    @Test
    void aDeclinedPaymentLeavesNoOrderBehind() {
        InMemoryProductCatalog catalog = InMemoryProductCatalog.seeded();
        OrderStore orders = new InMemoryOrderStore();
        PlaceOrderService service = new PlaceOrderService(
                catalog, orders, InMemoryPaymentGateway.declining(), new InMemoryNotifier());

        PlaceOrderResult result = service.place(
                PlaceOrderRequest.of("cust-8801", new RequestedLine("BNS-220", 2)),
                "ada@example.com");

        assertFalse(result.placed());
        assertEquals(40, catalog.stockOf("BNS-220"));
        assertEquals(0, orders.count());
    }

    @Test
    void exactlyOneChargeAndOneConfirmationPerPlacedOrder() {
        InMemoryNotifier notifier = new InMemoryNotifier();
        PlaceOrderService service = new PlaceOrderService(InMemoryProductCatalog.seeded(),
                new InMemoryOrderStore(), InMemoryPaymentGateway.working(), notifier);

        service.place(PlaceOrderRequest.of("cust-8801", new RequestedLine("BNS-220", 1)),
                "ada@example.com");

        assertEquals(1, notifier.sent().size());
        assertEquals("ada@example.com", notifier.sent().get(0).to());
    }
}
