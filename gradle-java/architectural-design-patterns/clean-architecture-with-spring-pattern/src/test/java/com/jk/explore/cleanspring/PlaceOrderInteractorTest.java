package com.jk.explore.cleanspring;

import com.jk.explore.cleanspring.adapters.gateway.InMemoryNotificationGateway;
import com.jk.explore.cleanspring.adapters.gateway.InMemoryOrderRepository;
import com.jk.explore.cleanspring.adapters.gateway.InMemoryPaymentGateway;
import com.jk.explore.cleanspring.adapters.gateway.InMemoryProductRepository;
import com.jk.explore.cleanspring.entities.Money;
import com.jk.explore.cleanspring.usecases.PlaceOrderInput;
import com.jk.explore.cleanspring.usecases.PlaceOrderInput.RequestedLine;
import com.jk.explore.cleanspring.usecases.PlaceOrderInteractor;
import com.jk.explore.cleanspring.usecases.PlaceOrderOutput;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The use case itself, constructed by hand here rather than by Spring — it
 * is the identical class {@code clean-architecture-pattern} already tests
 * in full, so this file only pins the behaviour this project's README and
 * narration quote, rather than repeating that project's whole suite.
 */
class PlaceOrderInteractorTest {

    @Test
    void threeLinesPriceToTheExpectedTotal() {
        PlaceOrderInteractor interactor = new PlaceOrderInteractor(
                InMemoryProductRepository.seeded(), new InMemoryOrderRepository(),
                InMemoryPaymentGateway.working(), new InMemoryNotificationGateway());

        PlaceOrderOutput output = interactor.execute(PlaceOrderInput.of(
                "cust-8801", "ada@example.com",
                new RequestedLine("ESP-001", 1),
                new RequestedLine("GRD-014", 1),
                new RequestedLine("BNS-220", 2)));

        assertTrue(output.placed());
        assertEquals(Money.pounds(382, 50), output.total());
    }

    @Test
    void notEnoughStockIsRefused() {
        PlaceOrderInteractor interactor = new PlaceOrderInteractor(
                InMemoryProductRepository.seeded(), new InMemoryOrderRepository(),
                InMemoryPaymentGateway.working(), new InMemoryNotificationGateway());

        PlaceOrderOutput output = interactor.execute(PlaceOrderInput.of(
                "cust-8801", "ada@example.com", new RequestedLine("GRD-014", 3)));

        assertFalse(output.placed());
        assertEquals("only 2 of GRD-014 left", output.reason());
    }
}
