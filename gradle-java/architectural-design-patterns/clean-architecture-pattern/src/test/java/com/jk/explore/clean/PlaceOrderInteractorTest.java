package com.jk.explore.clean;

import com.jk.explore.clean.adapters.gateway.InMemoryNotificationGateway;
import com.jk.explore.clean.adapters.gateway.InMemoryOrderRepository;
import com.jk.explore.clean.adapters.gateway.InMemoryPaymentGateway;
import com.jk.explore.clean.adapters.gateway.InMemoryProductRepository;
import com.jk.explore.clean.entities.Money;
import com.jk.explore.clean.usecases.PlaceOrderInput;
import com.jk.explore.clean.usecases.PlaceOrderInput.RequestedLine;
import com.jk.explore.clean.usecases.PlaceOrderInteractor;
import com.jk.explore.clean.usecases.PlaceOrderOutput;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The use case, tested through its input boundary, against nothing but
 * gateways it never names by type in its own source.
 */
class PlaceOrderInteractorTest {

    private PlaceOrderInteractor interactorWith(InMemoryPaymentGateway payments) {
        return new PlaceOrderInteractor(InMemoryProductRepository.seeded(),
                new InMemoryOrderRepository(), payments, new InMemoryNotificationGateway());
    }

    @Test
    void threeLinesPriceToTheExpectedTotal() {
        PlaceOrderOutput output = interactorWith(InMemoryPaymentGateway.working()).execute(
                PlaceOrderInput.of("cust-8801", "ada@example.com",
                        new RequestedLine("ESP-001", 1),
                        new RequestedLine("GRD-014", 1),
                        new RequestedLine("BNS-220", 2)));

        assertTrue(output.placed());
        assertEquals(Money.pounds(382, 50), output.total());
    }

    @Test
    void notEnoughStockIsRefusedBeforeAnyCharge() {
        InMemoryPaymentGateway payments = InMemoryPaymentGateway.working();
        PlaceOrderOutput output = interactorWith(payments).execute(
                PlaceOrderInput.of("cust-8801", "ada@example.com",
                        new RequestedLine("GRD-014", 3)));

        assertFalse(output.placed());
        assertEquals("only 2 of GRD-014 left", output.reason());
        assertTrue(payments.charges().isEmpty());
    }

    @Test
    void unknownProductIsRefused() {
        PlaceOrderOutput output = interactorWith(InMemoryPaymentGateway.working()).execute(
                PlaceOrderInput.of("cust-8801", "ada@example.com",
                        new RequestedLine("XXX-999", 1)));

        assertFalse(output.placed());
        assertEquals("no such product: XXX-999", output.reason());
    }

    @Test
    void aDeclinedPaymentLeavesNoOrderBehind() {
        InMemoryProductRepository products = InMemoryProductRepository.seeded();
        InMemoryOrderRepository orders = new InMemoryOrderRepository();
        PlaceOrderInteractor interactor = new PlaceOrderInteractor(products, orders,
                InMemoryPaymentGateway.declining(), new InMemoryNotificationGateway());

        PlaceOrderOutput output = interactor.execute(PlaceOrderInput.of(
                "cust-8801", "ada@example.com", new RequestedLine("BNS-220", 2)));

        assertFalse(output.placed());
        assertEquals(40, products.stockOf("BNS-220"));
        assertEquals(0, orders.count());
    }

    @Test
    void exactlyOneChargeAndOneConfirmationPerPlacedOrder() {
        InMemoryNotificationGateway notifications = new InMemoryNotificationGateway();
        PlaceOrderInteractor interactor = new PlaceOrderInteractor(
                InMemoryProductRepository.seeded(), new InMemoryOrderRepository(),
                InMemoryPaymentGateway.working(), notifications);

        interactor.execute(PlaceOrderInput.of("cust-8801", "ada@example.com",
                new RequestedLine("BNS-220", 1)));

        assertEquals(1, notifications.sent().size());
        assertEquals("ada@example.com", notifications.sent().get(0).to());
    }
}
