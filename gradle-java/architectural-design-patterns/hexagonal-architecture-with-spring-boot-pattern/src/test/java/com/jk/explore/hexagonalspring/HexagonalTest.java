package com.jk.explore.hexagonalspring;

import com.jk.explore.hexagonalspring.adapter.CardNetwork;
import com.jk.explore.hexagonalspring.adapter.driving.CsvBatch;
import com.jk.explore.hexagonalspring.adapter.jdbc.JdbcOrderStore;
import com.jk.explore.hexagonalspring.adapter.memory.InMemoryOrderStore;
import com.jk.explore.hexagonalspring.adapter.memory.InMemoryWarehouse;
import com.jk.explore.hexagonalspring.core.PlaceOrderService;
import com.jk.explore.hexagonalspring.core.domain.OutOfStock;
import com.jk.explore.hexagonalspring.core.domain.PaymentRefused;
import com.jk.explore.hexagonalspring.core.port.OrderStore;
import com.jk.explore.hexagonalspring.core.port.PlaceOrder;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.NoSuchBeanDefinitionException;
import org.springframework.context.ConfigurableApplicationContext;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class HexagonalTest {

    @Test
    void theCoreRunsWithoutAContainerAndRefusesWhatItShould() {
        var orders = new InMemoryOrderStore();
        var core = new PlaceOrderService(orders, new InMemoryWarehouse(), pence -> { });
        assertEquals(30000, core.place("ada", "ESP-001", 1).totalPence());
        assertThrows(OutOfStock.class, () -> core.place("ben", "ESP-001", 10));
        assertEquals(1, orders.count());
    }

    @Test
    void aDeclinedCardStopsTheOrderBeingSaved() {
        var orders = new InMemoryOrderStore();
        var core = new PlaceOrderService(orders, new InMemoryWarehouse(), pence -> { throw new PaymentRefused(); });
        assertThrows(PaymentRefused.class, () -> core.place("ada", "BNS-220", 1));
        assertEquals(0, orders.count());
    }

    @Test
    void theContainerHandsOutThePlainUseCase() {
        try (ConfigurableApplicationContext ctx = ShopApplication.start("memory")) {
            assertEquals(PlaceOrderService.class, ctx.getBean(PlaceOrder.class).getClass());
        }
    }

    @Test
    void thePropertyChoosesTheStorageAdapterAndBothGiveTheSameAnswer() {
        try (ConfigurableApplicationContext m = ShopApplication.start("memory");
             ConfigurableApplicationContext j = ShopApplication.start("jdbc")) {
            assertInstanceOf(InMemoryOrderStore.class, m.getBean(OrderStore.class));
            assertInstanceOf(JdbcOrderStore.class, j.getBean(OrderStore.class));
            assertEquals(m.getBean(PlaceOrder.class).place("a", "ESP-001", 1), j.getBean(PlaceOrder.class).place("a", "ESP-001", 1));
        }
    }

    @Test
    void twoDrivingAdaptersShareOnePort() {
        try (ConfigurableApplicationContext ctx = ShopApplication.start("memory")) {
            assertEquals(List.of("ORD-000001", "refused", "ORD-000002"),
                    ctx.getBean(CsvBatch.class).run(List.of("cy,BNS-220,2", "di,BNS-220,50", "ed,BNS-220,1")));
        }
    }

    @Test
    void aDeclinedCardThroughTheContainer() {
        try (ConfigurableApplicationContext ctx = ShopApplication.start("memory")) {
            ctx.getBean(CardNetwork.class).declineNextCharge();
            assertThrows(PaymentRefused.class, () -> ctx.getBean(PlaceOrder.class).place("a", "BNS-220", 1));
        }
    }

    @Test
    void theInsideRuleFindsOnlyTheShortcut() {
        var details = HexagonRules.checkInsideKnowsNoFramework().getFailureReport().getDetails();
        assertFalse(details.isEmpty());
        assertTrue(details.stream().allMatch(d -> d.contains("SpringyPlaceOrder")));
    }

    @Test
    void anUnknownStorageChoiceStopsStartup() {
        Exception e = assertThrows(Exception.class, () -> ShopApplication.start("nothing").close());
        Throwable root = e;
        while (root.getCause() != null && !(root instanceof NoSuchBeanDefinitionException)) root = root.getCause();
        assertInstanceOf(NoSuchBeanDefinitionException.class, root);
    }
}
