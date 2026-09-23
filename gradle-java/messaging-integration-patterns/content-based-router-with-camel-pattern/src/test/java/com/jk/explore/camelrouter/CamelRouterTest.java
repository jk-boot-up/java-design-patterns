package com.jk.explore.camelrouter;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

/**
 * The routes, checked against a real RabbitMQ broker in a container.
 *
 * <p>There is no pause anywhere in this file. Every wait is a loop that asks the broker how many messages
 * it is holding, and every one of those loops gives up with an error rather than hanging for ever. One
 * broker is started for the whole class and removed at the end.
 */
class CamelRouterTest {

    private static Broker broker;

    @BeforeAll
    static void startTheBroker() {
        System.setProperty("org.slf4j.simpleLogger.defaultLogLevel", "error");
        System.setProperty("org.slf4j.simpleLogger.log.org.testcontainers", "off");
        System.setProperty("org.slf4j.simpleLogger.log.tc", "off");
        if (!Broker.dockerAvailable()) {
            return;
        }
        broker = new Broker();
        broker.start();
    }

    @AfterAll
    static void stopTheBroker() {
        if (broker != null) {
            broker.close();
        }
    }

    private static void needsABroker() {
        assumeTrue(broker != null, "needs a container runtime");
    }

    // ---- these two need nothing running ----

    @Test
    void anOrderReadsBackOutOfItsOwnBody() {
        Order order = new Order("ORD-1", "physical", "express", "UK", 4999);
        assertEquals(order, Order.parse(order.body()));
    }

    @Test
    void theWarehouseCanOnlyShipPhysicalOrders() {
        Warehouse warehouse = new Warehouse();
        warehouse.handle(new Order("ORD-1", "physical", "express", "UK", 4999));
        warehouse.handle(new Order("ORD-2", "digital", "none", "UK", 2500));
        warehouse.handle(new Order("ORD-5", "subscription", "none", "UK", 999));
        assertEquals(1, warehouse.shipped());
        assertEquals(2, warehouse.couldNotHandle());
    }

    @Test
    void aMissingContainerRuntimeIsExplainedInSentences() {
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        CamelRouterDemo.explainNoContainerRuntime(new PrintStream(captured, true, StandardCharsets.UTF_8), null);
        String said = captured.toString(StandardCharsets.UTF_8);
        assertEquals(2, said.lines().count(), said);
        assertTrue(said.contains("container runtime"), said);
        assertTrue(said.contains("./gradlew run again"), said);
        assertFalse(said.contains("Exception"), said);
        assertFalse(said.contains("\tat "), said);
    }

    // ---- these run against the broker ----

    @Test
    void eachOrderGoesToTheQueueItsOwnContentAsksFor() {
        needsABroker();
        Map<String, String> went = CamelRouterDemo.routeAll(broker, ShopRoutes.standard(), CamelRouterDemo.ORDERS, 6);
        assertEquals("express-shipping", went.get("ORD-1"));
        assertEquals("digital-delivery", went.get("ORD-2"));
        assertEquals("fraud-review", went.get("ORD-3"));
        assertEquals("digital-delivery", went.get("ORD-4"));
        assertEquals("manual-review", went.get("ORD-5"));
        assertEquals("standard-shipping", went.get("ORD-6"));
        assertEquals(6, went.size());
    }

    @Test
    void theFirstQuestionAnsweredYesDecidesSoTheirOrderMatters() {
        needsABroker();
        Order big = new Order("ORD-7", "digital", "none", "UK", 150000);
        assertEquals("fraud-review", CamelRouterDemo.routeAll(broker, ShopRoutes.standard(), List.of(big), 1).get("ORD-7"));
        assertEquals("digital-delivery", CamelRouterDemo.routeAll(broker, ShopRoutes.highValueLast(), List.of(big), 1).get("ORD-7"));
    }

    @Test
    void withNoOtherwiseBranchTheUnclaimedMessageIsGone() {
        needsABroker();
        Order odd = new Order("ORD-8", "subscription", "none", "UK", 999);
        broker.clear();
        broker.post(Broker.ORDERS, odd);
        try (ShopRouter router = new ShopRouter(broker, ShopRoutes.noOtherwise())) {
            broker.settleRouted(0);
        }
        assertEquals(0, broker.waitingEverywhere());
    }

    @Test
    void anOtherwiseBranchKeepsWhatNoQuestionClaimed() {
        needsABroker();
        Order odd = new Order("ORD-8", "subscription", "none", "UK", 999);
        assertEquals("manual-review", CamelRouterDemo.routeAll(broker, ShopRoutes.standard(), List.of(odd), 1).get("ORD-8"));
        assertEquals("unclaimed", CamelRouterDemo.routeAll(broker, ShopRoutes.otherwiseUnclaimed(), List.of(odd), 1).get("ORD-8"));
    }

    @Test
    void aNewQuestionCatchesWhatFellThroughAndLeavesTheRestAlone() {
        needsABroker();
        Order euSubscription = new Order("ORD-10", "subscription", "none", "EU", 999);
        Order euPhysical = CamelRouterDemo.ORDERS.get(5);
        assertEquals("manual-review",
                CamelRouterDemo.routeAll(broker, ShopRoutes.standard(), List.of(euSubscription), 1).get("ORD-10"));
        Map<String, String> after =
                CamelRouterDemo.routeAll(broker, ShopRoutes.withEuVat(), List.of(euSubscription, euPhysical), 2);
        assertEquals("eu-vat-check", after.get("ORD-10"));
        assertEquals("standard-shipping", after.get("ORD-6"));
    }

    @Test
    void aRenamedFieldMakesEveryQuestionMissAndTheOrderFallsToTheOtherwiseBranch() {
        needsABroker();
        broker.clear();
        broker.post(Broker.ORDERS, "id=ORD-9;kind=goods;shipping=standard;region=UK;pence=100");
        try (ShopRouter router = new ShopRouter(broker, ShopRoutes.standard())) {
            broker.settleRouted(1);
        }
        assertEquals("manual-review", CamelRouterDemo.whereEachWent(broker).get("ORD-9"));
    }

    @Test
    void aBranchThatCannotFinishIsTriedThreeTimesAndThenKept() {
        needsABroker();
        AtomicInteger attempts = new AtomicInteger();
        broker.clear();
        broker.post(Broker.ORDERS, new Order("ORD-11", "physical", "standard", "UK", 250000));
        try (ShopRouter router = new ShopRouter(broker, ShopRoutes.fraudCheckBroken(attempts))) {
            broker.settleRouted(1);
        }
        assertEquals(3, attempts.get());
        assertEquals(1, broker.waiting("router-errors"));
    }

    @Test
    void oneRouteIsInstalledAndItCarriesTheNameItWasGiven() {
        needsABroker();
        try (ShopRouter router = new ShopRouter(broker, ShopRoutes.standard())) {
            assertEquals(1, router.routes());
            assertEquals("order-router", router.routeId());
        }
    }
}
