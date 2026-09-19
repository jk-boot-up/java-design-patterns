package com.jk.explore.stranglerfig;

import com.jk.explore.stranglerfig.domain.Capability;
import com.jk.explore.stranglerfig.domain.Line;
import com.jk.explore.stranglerfig.domain.Order;
import com.jk.explore.stranglerfig.domain.Result;
import com.jk.explore.stranglerfig.fresh.NewMailer;
import com.jk.explore.stranglerfig.fresh.NewPayment;
import com.jk.explore.stranglerfig.fresh.NewPricing;
import com.jk.explore.stranglerfig.fresh.NewStock;
import com.jk.explore.stranglerfig.legacy.LegacyCheckout;
import com.jk.explore.stranglerfig.migration.BigBang;
import com.jk.explore.stranglerfig.migration.Orders;
import com.jk.explore.stranglerfig.migration.StallModel;
import com.jk.explore.stranglerfig.route.Route;
import com.jk.explore.stranglerfig.route.Router;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class StranglerFigTest {

    private Router router(LegacyCheckout legacy, NewPricing pricing, NewStock stock, NewPayment payment) {
        return MigrationDemo.router(legacy, pricing, stock, payment, new NewMailer());
    }

    @Test
    void theBigBangRollbackIsAllOrNothingSoWorkingCapabilitiesGoBackToo() {
        BigBang.Outcome o = BigBang.run();
        assertEquals(0, o.ordersServedByNewCodeBeforeCutover());
        assertEquals(1, o.capabilitiesFaulty());
        assertEquals(4, o.capabilitiesRolledBack());
        assertTrue(o.rollbackWasAllOrNothing());
    }

    @Test
    void everyCapabilityStartsOnLegacyAndEachMovesOnItsOwn() {
        Router r = router(new LegacyCheckout(MigrationDemo.OPENING_STOCK), new NewPricing(true), new NewStock(MigrationDemo.OPENING_STOCK), new NewPayment());
        for (Capability c : Capability.values()) {
            assertEquals(Route.LEGACY, r.routeOf(c));
        }
        r.route(Capability.PRICING, Route.NEW);
        assertEquals(Route.NEW, r.routeOf(Capability.PRICING));
        assertEquals(Route.LEGACY, r.routeOf(Capability.STOCK));
        assertTrue(r.checkout(Orders.generate(1).get(0)).succeeded());
    }

    @Test
    void shadowReadsFindTheRoundingAndTheFiftyPoundDifferencesBeforeAnyCustomerDoes() {
        Router r = router(new LegacyCheckout(MigrationDemo.OPENING_STOCK), new NewPricing(false), new NewStock(MigrationDemo.OPENING_STOCK), new NewPayment());
        r.route(Capability.PRICING, Route.SHADOW);
        Orders.generate(200).forEach(r::checkout);
        r.checkout(Orders.exactlyFiftyPounds(201));
        assertEquals(201, r.compared());
        assertEquals(29, r.differences().size());
        assertTrue(r.differences().stream().anyMatch(d -> d.startsWith("order 7:")), "a per-line VAT rounding difference");
        assertTrue(r.differences().stream().anyMatch(d -> d.startsWith("order 201:")), "exactly fifty pounds: the delivery difference");
    }

    @Test
    void afterMatchingLegacyTheShadowFindsNothing() {
        Router r = router(new LegacyCheckout(MigrationDemo.OPENING_STOCK), new NewPricing(true), new NewStock(MigrationDemo.OPENING_STOCK), new NewPayment());
        r.route(Capability.PRICING, Route.SHADOW);
        Orders.generate(200).forEach(r::checkout);
        r.checkout(Orders.exactlyFiftyPounds(201));
        assertEquals(0, r.differences().size());
        assertEquals(201, r.compared());
    }

    @Test
    void shadowServesFromLegacyWhilstItCompares() {
        LegacyCheckout legacy = new LegacyCheckout(MigrationDemo.OPENING_STOCK);
        Router r = router(legacy, new NewPricing(false), new NewStock(MigrationDemo.OPENING_STOCK), new NewPayment());
        r.route(Capability.PRICING, Route.SHADOW);
        Result served = r.checkout(Orders.exactlyFiftyPounds(1));
        assertEquals(legacy.price(Orders.exactlyFiftyPounds(1)), served.pricing(), "the customer got legacy's answer");
    }

    @Test
    void oneMisbehavingCapabilityRollsBackAloneAndTheOthersStayMoved() {
        NewPayment payment = new NewPayment();
        Router r = router(new LegacyCheckout(MigrationDemo.OPENING_STOCK), new NewPricing(true), new NewStock(MigrationDemo.OPENING_STOCK), payment);
        r.route(Capability.PRICING, Route.NEW);
        r.route(Capability.PAYMENT, Route.NEW);
        payment.misbehave(true);
        Order big = new Order(300, List.of(new Line("SKU-1", 10, 3_000)));
        Result failing = r.checkout(big);
        assertFalse(failing.succeeded());
        assertNull(failing.chargeId());
        r.route(Capability.PAYMENT, Route.LEGACY);
        Result recovered = r.checkout(big);
        assertTrue(recovered.succeeded());
        assertEquals(Route.NEW, r.routeOf(Capability.PRICING), "pricing never moved back");
    }

    @Test
    void twoStockTablesDriftTheMomentStockMoves() {
        LegacyCheckout legacy = new LegacyCheckout(MigrationDemo.OPENING_STOCK);
        NewStock fresh = new NewStock(MigrationDemo.OPENING_STOCK);
        Router r = router(legacy, new NewPricing(true), fresh, new NewPayment());
        r.route(Capability.STOCK, Route.NEW);
        r.checkout(new Order(400, List.of(new Line("SKU-2", 5, 1_000))));
        assertEquals(395, fresh.onHand("SKU-2"));
        assertEquals(400, legacy.onHand("SKU-2"));
    }

    @Test
    void runningBothCostsMoreThanEitherEndpointAndAStalledMigrationStaysThere() {
        assertEquals(100, StallModel.runningCost(0));
        assertEquals(60, StallModel.runningCost(4));
        assertTrue(StallModel.runningCost(2) > StallModel.runningCost(0));
        List<StallModel.Quarter> stalled = StallModel.stalled();
        assertEquals(2, stalled.get(5).capabilitiesMoved());
        assertEquals(115, stalled.get(5).runningCost());
        int stalledSum = stalled.stream().mapToInt(StallModel.Quarter::totalCost).sum();
        int finishedSum = StallModel.finished().stream().mapToInt(StallModel.Quarter::totalCost).sum();
        assertTrue(finishedSum < stalledSum, "finished " + finishedSum + " against stalled " + stalledSum);
    }
}
