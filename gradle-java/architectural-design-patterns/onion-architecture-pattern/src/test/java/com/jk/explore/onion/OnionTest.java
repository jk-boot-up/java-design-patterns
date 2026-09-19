package com.jk.explore.onion;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.jk.explore.onion.application.PlaceOrderService;
import com.jk.explore.onion.domain.model.Order;
import com.jk.explore.onion.domain.model.OrderLine;
import com.jk.explore.onion.domain.service.PricingService;
import com.jk.explore.onion.infrastructure.InMemoryOrderRepository;
import com.jk.explore.onion.infrastructure.RecordOrderRepository;
import com.jk.explore.onion.naive.NaiveOrder;
import com.jk.explore.onion.ui.ConsoleApi;
import java.util.List;
import org.junit.jupiter.api.Test;

class OnionTest {

    @Test
    void theOnionHasNoOutwardDependency() {
        assertEquals(List.of(), DependencyRule.violations(OnionDemo.GOOD));
    }

    @Test
    void theNaiveOrderIsCaught() {
        List<String> v = DependencyRule.violations(NaiveOrder.class);
        assertEquals(1, v.stream().filter(s -> s.contains("SqlDatabase")).count());
    }

    @Test
    void bigOrdersGetTenPercentOff() {
        Order big = new Order("A", List.of(new OrderLine("MUG", 2, 6000)));
        new PricingService().price(big);
        assertEquals(10800, big.totalCents());
        Order small = new Order("B", List.of(new OrderLine("TEA", 1, 950)));
        new PricingService().price(small);
        assertEquals(950, small.totalCents());
    }

    @Test
    void bothStoragesGiveTheSameAnswerAndRoundTrip() {
        List<OrderLine> lines = List.of(new OrderLine("MUG", 2, 6000));
        RecordOrderRepository records = new RecordOrderRepository();
        Order a = new PlaceOrderService(new InMemoryOrderRepository(), new PricingService()).place("X", lines);
        Order b = new PlaceOrderService(records, new PricingService()).place("X", lines);
        assertEquals(a.totalCents(), b.totalCents());
        assertEquals(10800, records.find("X").orElseThrow().totalCents());
        assertEquals(2, records.conversions());
    }

    @Test
    void anEmptyOrderIsRefused() {
        try {
            new Order("E", List.of());
        } catch (IllegalArgumentException e) {
            assertTrue(e.getMessage().contains("at least one"));
            return;
        }
        throw new AssertionError("expected a refusal");
    }

    @Test
    void theOutsideTurnsTextIntoAUseCase() {
        ConsoleApi api = new ConsoleApi(new PlaceOrderService(new InMemoryOrderRepository(), new PricingService()));
        assertEquals("ORD-3 total 10800", api.handle("ORD-3 MUG 2 6000"));
    }
}
