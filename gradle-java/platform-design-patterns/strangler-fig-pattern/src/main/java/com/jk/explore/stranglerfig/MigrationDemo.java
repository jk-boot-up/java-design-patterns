package com.jk.explore.stranglerfig;

import com.jk.explore.stranglerfig.domain.Capability;
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

import java.util.List;
import java.util.Map;

/** Six acts. Orders come from a fixed-seed generator, so every count is the same every run. */
public final class MigrationDemo {

    static final Map<String, Integer> OPENING_STOCK = Map.of("SKU-1", 400, "SKU-2", 400, "SKU-3", 400, "SKU-4", 400);

    public static void main(String[] args) {
        System.out.println("STRANGLER FIG — replacing the checkout without a cutover weekend\n");
        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix();
    }

    static Router router(LegacyCheckout legacy, NewPricing pricing, NewStock stock, NewPayment payment, NewMailer mailer) {
        return new Router(legacy, pricing, legacy, stock, legacy, payment, legacy, mailer);
    }

    private static void actOne() {
        System.out.println("ONE. The big-bang rewrite.");
        BigBang.Outcome o = BigBang.run();
        System.out.println("  " + o.weeksOfWork() + " weeks of work in parallel with production. orders the new code served in that time: "
                + o.ordersServedByNewCodeBeforeCutover() + ".");
        System.out.println("  no feedback from real traffic for half a year, and then a cutover weekend.");
        System.out.println("  Monday: " + o.capabilitiesFaulty() + " of " + o.capabilitiesInNewCode() + " capabilities is faulty: payment declines large orders.");
        System.out.println("  the only rollback is all-or-nothing, so " + o.capabilitiesRolledBack() + " of " + o.capabilitiesInNewCode()
                + " go back, including the three that were fine.\n");
    }

    private static void actTwo() {
        System.out.println("TWO. The pattern: a router, and one switch per capability.");
        LegacyCheckout legacy = new LegacyCheckout(OPENING_STOCK);
        Router router = router(legacy, new NewPricing(true), new NewStock(OPENING_STOCK), new NewPayment(), new NewMailer());
        System.out.println("  every capability starts on the legacy checkout: " + routes(router));
        router.route(Capability.PRICING, Route.NEW);
        System.out.println("  pricing moves first: " + routes(router));
        Result result = router.checkout(Orders.generate(1).get(0));
        System.out.println("  an order through the router: priced by the new code, everything else by legacy. succeeded: " + result.succeeded());
        System.out.println("  the customer saw no cutover. the checkout never stopped.\n");
    }

    private static void actThree() {
        System.out.println("THREE. Shadow reads: move on evidence, not on hope.");
        LegacyCheckout legacy = new LegacyCheckout(OPENING_STOCK);
        Router router = router(legacy, new NewPricing(false), new NewStock(OPENING_STOCK), new NewPayment(), new NewMailer());
        router.route(Capability.PRICING, Route.SHADOW);
        List<Order> orders = Orders.generate(200);
        orders.forEach(router::checkout);
        router.checkout(Orders.exactlyFiftyPounds(201));
        System.out.println("  " + router.compared() + " orders served by legacy, and priced by the new code as well, and compared.");
        System.out.println("  they disagreed on " + router.differences().size() + ". the first three:");
        router.differences().stream().limit(3).forEach(d -> System.out.println("    " + d));
        System.out.println("  two causes, both found before a customer paid a penny differently: VAT rounded per line against once,");
        System.out.println("  and free delivery from fifty pounds against over fifty pounds.");
        Router matched = router(new LegacyCheckout(OPENING_STOCK), new NewPricing(true), new NewStock(OPENING_STOCK), new NewPayment(), new NewMailer());
        matched.route(Capability.PRICING, Route.SHADOW);
        orders.forEach(matched::checkout);
        matched.checkout(Orders.exactlyFiftyPounds(201));
        System.out.println("  after the team decides to reproduce legacy exactly: " + matched.differences().size() + " differences in "
                + matched.compared() + ". now pricing can move.\n");
    }

    private static void actFour() {
        System.out.println("FOUR. Rollback: one capability, not the whole checkout.");
        LegacyCheckout legacy = new LegacyCheckout(OPENING_STOCK);
        NewPayment payment = new NewPayment();
        Router router = router(legacy, new NewPricing(true), new NewStock(OPENING_STOCK), payment, new NewMailer());
        router.route(Capability.PRICING, Route.NEW);
        router.route(Capability.PAYMENT, Route.NEW);
        payment.misbehave(true);
        Order big = new Order(300, List.of(new com.jk.explore.stranglerfig.domain.Line("SKU-1", 10, 3_000)));
        Result failing = router.checkout(big);
        System.out.println("  payment is on the new code, and misbehaves on a large order. succeeded: " + failing.succeeded()
                + ", charge: " + failing.chargeId() + ".");
        router.route(Capability.PAYMENT, Route.LEGACY);
        Result recovered = router.checkout(big);
        System.out.println("  one switch flipped: payment alone goes back to legacy. succeeded: " + recovered.succeeded()
                + ", charge: " + recovered.chargeId() + ".");
        System.out.println("  routes now: " + routes(router) + ". pricing stayed on the new code the whole time.\n");
    }

    private static void actFive() {
        System.out.println("FIVE. The bill: two systems, and two versions of the truth.");
        LegacyCheckout legacy = new LegacyCheckout(OPENING_STOCK);
        NewStock newStock = new NewStock(OPENING_STOCK);
        Router router = router(legacy, new NewPricing(true), newStock, new NewPayment(), new NewMailer());
        router.route(Capability.STOCK, Route.NEW);
        Order order = new Order(400, List.of(new com.jk.explore.stranglerfig.domain.Line("SKU-2", 5, 1_000)));
        router.checkout(order);
        System.out.println("  stock moved to the new service, and an order took 5 of SKU-2.");
        System.out.println("  the new service says " + newStock.onHand("SKU-2") + " on hand. the legacy table, which its reports and its invoices still read, says "
                + legacy.onHand("SKU-2") + ".");
        System.out.println("  two tables claim to be the truth, and someone must decide which, and keep them in step until legacy is gone.");
        System.out.println("  and every business rule that changes while both are live is changed twice: in legacy, and in the new code.\n");
    }

    private static void actSix() {
        System.out.println("SIX. The failure mode that actually happens: the migration stalls.");
        System.out.println("  a cost model, stated as one. all legacy costs " + StallModel.LEGACY_ALL + " a quarter, all new costs "
                + StallModel.NEW_ALL + ". while both are live there is an extra " + StallModel.RUNNING_BOTH_OVERHEAD + " for running two.");
        System.out.println("  quarter   stalled: moved  running  total     finished: moved  running  total");
        List<StallModel.Quarter> stalled = StallModel.stalled();
        List<StallModel.Quarter> finished = StallModel.finished();
        int stalledSum = 0;
        int finishedSum = 0;
        for (int i = 0; i < 6; i++) {
            StallModel.Quarter st = stalled.get(i);
            StallModel.Quarter fi = finished.get(i);
            stalledSum += st.totalCost();
            finishedSum += fi.totalCost();
            System.out.printf("  %-8d           %-5d  %-7d  %-8d           %-5d  %-7d  %d%n", st.number(), st.capabilitiesMoved(),
                    st.runningCost(), st.totalCost(), fi.capabilitiesMoved(), fi.runningCost(), fi.totalCost());
        }
        System.out.println("  six quarters, cumulative: stalled " + stalledSum + ", finished " + finishedSum + ".");
        StallModel.Quarter last = stalled.get(5);
        System.out.println("  budget goes elsewhere after quarter 2. two of four capabilities moved, and it stays that way.");
        System.out.println("  the stalled state costs " + last.runningCost() + " a quarter, more than all legacy (" + StallModel.LEGACY_ALL
                + ") and more than all new (" + StallModel.NEW_ALL + "). two checkouts, forever, is worse than either endpoint.");
        System.out.println("  verdict: use it, but treat the end date and the decommissioning of legacy as part of the migration, not a later job.");
        System.out.println("  where you have met this: an API gateway or proxy sending one path to the old service and another to the new.");
    }

    private static String routes(Router router) {
        StringBuilder sb = new StringBuilder();
        for (Capability c : Capability.values()) {
            sb.append(c).append('=').append(router.routeOf(c)).append(' ');
        }
        return sb.toString().trim();
    }
}
