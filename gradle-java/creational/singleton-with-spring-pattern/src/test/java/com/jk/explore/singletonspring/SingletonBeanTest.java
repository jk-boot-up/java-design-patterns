package com.jk.explore.singletonspring;

import org.junit.jupiter.api.Test;
import org.springframework.context.ConfigurableApplicationContext;

import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

import static org.junit.jupiter.api.Assertions.*;

class SingletonBeanTest {

    @Test
    void threeCallersShareOneGenerator() {
        try (ConfigurableApplicationContext ctx = ShopApplication.builder().run()) {
            assertSame(ctx.getBean(Checkout.class).generator(), ctx.getBean(AdminConsole.class).generator());
            assertSame(ctx.getBean(AdminConsole.class).generator(), ctx.getBean(RetryJob.class).generator());
            assertEquals("ORD-000001", ctx.getBean(Checkout.class).issue());
            assertEquals("ORD-000002", ctx.getBean(RetryJob.class).issue());
        }
    }

    @Test
    void plainNewMakesAnotherOne() {
        try (ConfigurableApplicationContext ctx = ShopApplication.builder().run()) {
            OrderSequenceGenerator managed = ctx.getBean(OrderSequenceGenerator.class);
            assertNotSame(managed, new OrderSequenceGenerator());
        }
    }

    @Test
    void twoContextsIssueTheSameNumber() {
        try (ConfigurableApplicationContext a = ShopApplication.builder().run();
             ConfigurableApplicationContext b = ShopApplication.builder().run()) {
            assertEquals(a.getBean(Checkout.class).issue(), b.getBean(Checkout.class).issue());
        }
    }

    @Test
    void prototypeScopeGivesEachCallerItsOwn() {
        try (ConfigurableApplicationContext ctx = ShopApplication.builder()
                .initializers(c -> c.addBeanFactoryPostProcessor(
                        bf -> bf.getBeanDefinition("orderSequenceGenerator").setScope("prototype")))
                .run()) {
            assertNotSame(ctx.getBean(Checkout.class).generator(), ctx.getBean(AdminConsole.class).generator());
            assertEquals(ctx.getBean(Checkout.class).issue(), ctx.getBean(AdminConsole.class).issue());
        }
    }

    @Test
    void eagerBuildsAtStartupAndLazyBuildsOnFirstUse() {
        OrderSequenceGenerator.BUILT.set(0);
        try (ConfigurableApplicationContext ctx = ShopApplication.builder().run()) {
            assertEquals(1, OrderSequenceGenerator.BUILT.get());
        }
        OrderSequenceGenerator.BUILT.set(0);
        try (ConfigurableApplicationContext ctx = ShopApplication.builder().lazyInitialization(true).run()) {
            assertEquals(0, OrderSequenceGenerator.BUILT.get());
            ctx.getBean(OrderSequenceGenerator.class);
            assertEquals(1, OrderSequenceGenerator.BUILT.get());
        }
    }

    @Test
    void heldPlainLongIssuesADuplicate() throws Exception {
        UnsafeOrderSequence unsafe = new UnsafeOrderSequence();
        Gate gate = new Gate();
        java.util.concurrent.CountDownLatch inside = new java.util.concurrent.CountDownLatch(1);
        String[] slow = new String[1];
        Thread t = new Thread(() -> slow[0] = unsafe.nextOrderNumber(() -> { inside.countDown(); gate.await(); }));
        t.start();
        inside.await();
        String quick = unsafe.nextOrderNumber(() -> { });
        gate.open();
        t.join();
        assertEquals(slow[0], quick);
    }

    @Test
    void atomicCounterNeverRepeats() throws Exception {
        OrderSequenceGenerator g = new OrderSequenceGenerator();
        Set<String> seen = ConcurrentHashMap.newKeySet();
        Thread[] ts = new Thread[4];
        for (int i = 0; i < 4; i++) {
            ts[i] = new Thread(() -> { for (int n = 0; n < 2500; n++) seen.add(g.nextOrderNumber()); });
            ts[i].start();
        }
        for (Thread t : ts) t.join();
        assertEquals(10000, seen.size());
    }
}
