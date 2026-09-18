package com.jk.explore.hexagonal;

import com.jk.explore.hexagonal.adapter.driving.cli.CliCheckoutAdapter;
import com.jk.explore.hexagonal.adapter.driving.http.HttpCheckoutAdapter;
import com.jk.explore.hexagonal.adapter.notification.InMemoryNotifier;
import com.jk.explore.hexagonal.adapter.payment.InMemoryPaymentGateway;
import com.jk.explore.hexagonal.adapter.persistence.AppendOnlyOrderStore;
import com.jk.explore.hexagonal.adapter.persistence.InMemoryOrderStore;
import com.jk.explore.hexagonal.adapter.persistence.InMemoryProductCatalog;
import com.jk.explore.hexagonal.core.PlaceOrderService;
import com.jk.explore.hexagonal.core.port.OrderStore;

import org.junit.jupiter.api.Test;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The two claims this project makes, pinned down as tests rather than left
 * as prose.
 *
 * <p>{@code sameCoreAnsweredByHttpAndByCli} is the driving-side claim: one
 * {@code PlaceOrderService} instance, called through two completely
 * different adapters, produces the same order.
 *
 * <p>{@code storageSwapProducesTheSameOrder} is the driven-side claim: two
 * structurally different {@code OrderStore} implementations, handed to an
 * otherwise identical service, produce the same placed order.
 */
class BothSidesAgreeTest {

    @Test
    void sameCoreAnsweredByHttpAndByCli() {
        PlaceOrderService service = new PlaceOrderService(InMemoryProductCatalog.seeded(),
                new InMemoryOrderStore(), InMemoryPaymentGateway.working(), new InMemoryNotifier());

        HttpCheckoutAdapter http = new HttpCheckoutAdapter(service);
        String httpResponse = http.post(jsonBody());
        assertTrue(httpResponse.contains("ord-1001"));
        assertTrue(httpResponse.contains("£382.50"));

        // A second, independent service instance, called only from the CLI adapter.
        PlaceOrderService secondService = new PlaceOrderService(InMemoryProductCatalog.seeded(),
                new InMemoryOrderStore(), InMemoryPaymentGateway.working(), new InMemoryNotifier());
        CliCheckoutAdapter cli = new CliCheckoutAdapter(secondService);
        String cliResponse = cli.run(
                "checkout cust-8801 ada@example.com ESP-001:1,GRD-014:1,BNS-220:2");

        assertTrue(cliResponse.contains("ord-1001"));
        assertTrue(cliResponse.contains("£382.50"));
    }

    @Test
    void storageSwapProducesTheSameOrder() {
        InMemoryProductCatalog catalog1 = InMemoryProductCatalog.seeded();
        OrderStore mapStore = new InMemoryOrderStore();
        PlaceOrderService withMap = new PlaceOrderService(
                catalog1, mapStore, InMemoryPaymentGateway.working(), new InMemoryNotifier());

        InMemoryProductCatalog catalog2 = InMemoryProductCatalog.seeded();
        OrderStore logStore = new AppendOnlyOrderStore();
        PlaceOrderService withLog = new PlaceOrderService(
                catalog2, logStore, InMemoryPaymentGateway.working(), new InMemoryNotifier());

        var request = com.jk.explore.hexagonal.core.PlaceOrderRequest.of("cust-8801",
                new com.jk.explore.hexagonal.core.PlaceOrderRequest.RequestedLine("BNS-220", 2));

        var resultWithMap = withMap.place(request, "ada@example.com");
        var resultWithLog = withLog.place(request, "ada@example.com");

        assertEquals(resultWithMap.total(), resultWithLog.total());
        assertEquals(1, mapStore.count());
        assertEquals(1, logStore.count());
    }

    private Map<String, Object> jsonBody() {
        Map<String, Object> body = new LinkedHashMap<>();
        body.put("customerId", "cust-8801");
        body.put("email", "ada@example.com");
        Map<String, Object> l1 = Map.of("sku", "ESP-001", "quantity", 1);
        Map<String, Object> l2 = Map.of("sku", "GRD-014", "quantity", 1);
        Map<String, Object> l3 = Map.of("sku", "BNS-220", "quantity", 2);
        body.put("lines", List.of(l1, l2, l3));
        return body;
    }
}
