package com.jk.explore.observerspring;

import org.junit.jupiter.api.Test;
import org.springframework.context.ConfigurableApplicationContext;

import static org.junit.jupiter.api.Assertions.*;

class ObserverBeanTest {

    @Test
    void everyListenerHearsAShipmentInOrderOnTheCallersThread() {
        try (ConfigurableApplicationContext ctx = OrderEventsApplication.builder().run()) {
            ctx.getBean(OrderService.class).ship("A");
            var lines = ctx.getBean(Journal.class).lines();
            assertEquals(4, lines.size());
            assertTrue(lines.get(0).startsWith("inventory"));
            assertTrue(lines.get(1).startsWith("email"));
            assertTrue(lines.get(2).startsWith("analytics"));
            assertTrue(lines.get(3).startsWith("warehouse"));
            assertTrue(lines.get(0).endsWith("on " + Thread.currentThread().getName()));
        }
    }

    @Test
    void aFailingListenerStopsTheOthersAndReachesTheCaller() {
        try (ConfigurableApplicationContext ctx = OrderEventsApplication.builder().run()) {
            ctx.getBean(EmailListener.class).mailServerDown(true);
            OrderService orders = ctx.getBean(OrderService.class);
            assertThrows(IllegalStateException.class, () -> orders.ship("B"));
            assertTrue(orders.isShipped("B"));
            assertEquals(1, ctx.getBean(Journal.class).lines().size());
        }
    }

    @Test
    void asyncListenerRunsOnAnotherThreadAfterTheCallReturns() throws Exception {
        try (ConfigurableApplicationContext ctx = OrderEventsApplication.builder().run()) {
            AuditListener audit = ctx.getBean(AuditListener.class);
            Journal journal = ctx.getBean(Journal.class);
            audit.hold();
            ctx.getBean(OrderService.class).cancel("C");
            assertTrue(journal.lines().stream().noneMatch(l -> l.startsWith("audit")));
            audit.release();
            audit.done().await();
            String line = journal.lines().stream().filter(l -> l.startsWith("audit")).findFirst().orElseThrow();
            assertFalse(line.endsWith("on " + Thread.currentThread().getName()));
        }
    }

    @Test
    void conditionFiltersByStatus() throws Exception {
        try (ConfigurableApplicationContext ctx = OrderEventsApplication.builder().run()) {
            AuditListener audit = ctx.getBean(AuditListener.class);
            audit.hold();
            audit.release();
            ctx.getBean(OrderService.class).cancel("D");
            audit.done().await();
            assertTrue(ctx.getBean(Journal.class).lines().stream().noneMatch(l -> l.startsWith("warehouse")));
        }
    }

    @Test
    void anEventWithNoListenerIsSilentlyDropped() {
        try (ConfigurableApplicationContext ctx = OrderEventsApplication.builder().run()) {
            assertDoesNotThrow(() -> ctx.getBean(OrderService.class).refund("E"));
            assertTrue(ctx.getBean(Journal.class).lines().isEmpty());
        }
    }
}
