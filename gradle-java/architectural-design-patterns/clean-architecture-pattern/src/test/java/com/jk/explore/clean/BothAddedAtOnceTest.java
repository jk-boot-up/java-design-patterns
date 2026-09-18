package com.jk.explore.clean;

import com.jk.explore.clean.adapters.controller.BatchOrderController;
import com.jk.explore.clean.adapters.controller.CheckoutController;
import com.jk.explore.clean.adapters.gateway.FileBackedOrderRepository;
import com.jk.explore.clean.adapters.gateway.InMemoryNotificationGateway;
import com.jk.explore.clean.adapters.gateway.InMemoryOrderRepository;
import com.jk.explore.clean.adapters.gateway.InMemoryPaymentGateway;
import com.jk.explore.clean.adapters.gateway.InMemoryProductRepository;
import com.jk.explore.clean.usecases.OrderRepository;
import com.jk.explore.clean.usecases.PlaceOrderInputBoundary;
import com.jk.explore.clean.usecases.PlaceOrderInteractor;

import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The forced change's claim, proven rather than narrated: the original
 * HTTP-and-map path and the new batch-and-file path both work, at the same
 * time, from the same {@code PlaceOrderInteractor} class — one instance
 * per path, but neither instance's class was edited to add the other.
 */
class BothAddedAtOnceTest {

    @Test
    void theOriginalPathStillWorks() {
        PlaceOrderInteractor interactor = new PlaceOrderInteractor(
                InMemoryProductRepository.seeded(), new InMemoryOrderRepository(),
                InMemoryPaymentGateway.working(), new InMemoryNotificationGateway());
        CheckoutController checkout = new CheckoutController(interactor);

        Map<String, Object> body = Map.of(
                "customerId", "cust-8801", "email", "ada@example.com",
                "lines", List.of(Map.of("sku", "BNS-220", "quantity", 1)));

        String response = checkout.post(body);
        assertTrue(response.contains("\"status\":201"));
    }

    @Test
    void theNewPathWorksTooWithNoInteractorClassChange() {
        OrderRepository fileStore = new FileBackedOrderRepository();
        PlaceOrderInputBoundary interactor = new PlaceOrderInteractor(
                InMemoryProductRepository.seeded(), fileStore,
                InMemoryPaymentGateway.working(), new InMemoryNotificationGateway());
        BatchOrderController batch = new BatchOrderController(interactor);

        List<String> results = batch.importBatch(List.of("cust-9001,ops@example.com,BNS-220:1"));

        assertTrue(results.get(0).startsWith("IMPORTED"));
        assertTrue(fileStore.count() == 1);
    }
}
