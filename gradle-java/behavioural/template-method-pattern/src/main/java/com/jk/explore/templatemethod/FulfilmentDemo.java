package com.jk.explore.templatemethod;

import java.util.List;

/**
 * Runnable walkthrough. Run it with {@code ./gradlew run}.
 *
 * <p>Section 1 fulfils two orders with the hand-written routes and shows what
 * drift costs. Section 2 runs three completely different routes through one
 * {@code fulfil} and prints their step names side by side. Section 3 exercises
 * the hook. Section 4 adds a fourth route without opening
 * {@link FulfilmentProcess}.
 */
public final class FulfilmentDemo {

    public static void main(String[] args) {
        theTrap();
        thePattern();
        theHook();
        aFourthRoute();
        whatItCost();
    }

    // ---- 1 --------------------------------------------------------------

    private static void theTrap() {
        System.out.println();
        System.out.println("=== 1. The trap: three hand-written copies of the same sequence ===");
        System.out.println();

        NaiveFulfilment naive = new NaiveFulfilment(warehouseStock(), "Reading", acme());

        System.out.println("  A download, fulfilled by NaiveFulfilment.fulfilDigital:");
        FulfilmentReport digital = naive.fulfilDigital(digitalOrder("D-9001"));
        printSteps(digital);
        System.out.println("    email sent:");
        digital.notifications().forEach(n -> System.out.println("      " + n));
        System.out.println("  The customer was told before the key existed.");
        System.out.println();

        System.out.println("  A marketplace order the seller will not confirm:");
        Order refused = Order.shipped("M-9002", "priya@example.com", "12 Mill Lane, Bath",
                List.of(new OrderLine("T-410", "Bamboo tripod", Money.pounds(42.00), 1)));
        try {
            naive.fulfilFromMarketplace(refused);
        } catch (FulfilmentException e) {
            System.out.println("    " + e.getMessage());
            System.out.println("    but the card was charged " + refused.subtotal()
                    + " one step earlier.");
        }
        System.out.println();
        System.out.println("  Both are one line in the wrong place, in a copy nobody rereads.");
    }

    // ---- 2 --------------------------------------------------------------

    private static void thePattern() {
        System.out.println();
        System.out.println("=== 2. The pattern: one sequence, three routes ===");
        System.out.println();

        FulfilmentReport warehouse =
                new WarehouseFulfilment(warehouseStock(), "Reading").fulfil(warehouseOrder("A-1001"));
        FulfilmentReport marketplace =
                new MarketplaceFulfilment(acme()).fulfil(marketplaceOrder("M-1002"));
        FulfilmentReport digital =
                new DigitalFulfilment().fulfil(digitalOrder("D-1003"));

        for (FulfilmentReport report : List.of(warehouse, marketplace, digital)) {
            System.out.println("  " + report.route() + " (" + report.orderId() + ")");
            printSteps(report);
            report.notifications().forEach(n -> System.out.println("    email: " + n));
            report.notes().forEach(n -> System.out.println("    note : " + n));
            System.out.println();
        }

        System.out.println("  step names, warehouse   : " + warehouse.stepNames());
        System.out.println("  step names, marketplace : " + marketplace.stepNames());
        System.out.println("  step names, digital     : " + digital.stepNames());
        System.out.println("  Identical, and no route chose that. FulfilmentProcess.fulfil did.");
        System.out.println();
        System.out.println("  This time the digital email carries the key, because dispatch");
        System.out.println("  runs before notify and no subclass is allowed a say in that.");
    }

    // ---- 3 --------------------------------------------------------------

    private static void theHook() {
        System.out.println();
        System.out.println("=== 3. The hook: one question, two answers ===");
        System.out.println();

        Order noAddress = Order.addressless("D-1004", "sam@example.com",
                List.of(new OrderLine("E-777", "Recipe e-book", Money.pounds(9.99), 1)));

        FulfilmentReport ok = new DigitalFulfilment().fulfil(noAddress);
        System.out.println("  digital, no address     : " + ok.steps().get(0));

        Order alsoNoAddress = new Order("A-1005", "sam@example.com", null,
                List.of(new OrderLine("H-100", "Wireless headphones", Money.pounds(89.99), 1)));
        try {
            new WarehouseFulfilment(warehouseStock(), "Reading").fulfil(alsoNoAddress);
        } catch (FulfilmentException e) {
            System.out.println("  warehouse, no address   : refused — " + e.getMessage());
        }
        System.out.println();
        System.out.println("  requiresShippingAddress() is the only say a route gets in");
        System.out.println("  validation. It cannot skip the check, only answer it.");
    }

    // ---- 4 --------------------------------------------------------------

    /**
     * Click and collect, defined here in the demo file. Adding it required no
     * change to {@link FulfilmentProcess} and no change to any existing route
     * — which is the claim, made where it can be checked.
     */
    private static final class ClickAndCollectFulfilment extends FulfilmentProcess {

        private final StockLedger ledger;
        private final String store;

        private ClickAndCollectFulfilment(StockLedger ledger, String store) {
            this.ledger = ledger;
            this.store = store;
        }

        @Override
        protected String routeName() {
            return "click-and-collect";
        }

        @Override
        protected boolean requiresShippingAddress() {
            return false;
        }

        @Override
        protected void reserveStock(Order order, FulfilmentReport report) {
            for (OrderLine line : order.lines()) {
                ledger.reserve(line.sku(), line.quantity());
            }
            report.step("reserve", order.itemCount() + " unit(s) held at the " + store + " counter");
        }

        @Override
        protected void charge(Order order, FulfilmentReport report) {
            report.charged(order.subtotal());
            report.step("charge", order.subtotal() + " taken by the store");
        }

        @Override
        protected void dispatch(Order order, FulfilmentReport report) {
            String slot = "PICKUP-" + order.id();
            report.dispatchedAs(slot);
            report.step("dispatch", "moved to the collection shelf, " + slot);
        }

        @Override
        protected void notifyCustomer(Order order, FulfilmentReport report) {
            report.notified(order.customerEmail() + ": Order " + order.id()
                    + " is ready to collect from " + store + ". Quote " + report.dispatchReference());
            report.step("notify", "emailed " + order.customerEmail());
        }
    }

    private static void aFourthRoute() {
        System.out.println();
        System.out.println("=== 4. A fourth route, added without touching the base class ===");
        System.out.println();

        Order order = Order.addressless("C-1006", "leo@example.com",
                List.of(new OrderLine("K-330", "Carry case", Money.pounds(24.00), 1)));
        FulfilmentReport report =
                new ClickAndCollectFulfilment(warehouseStock(), "Bristol").fulfil(order);

        System.out.println("  " + report.route() + " (" + report.orderId() + ")");
        printSteps(report);
        report.notifications().forEach(n -> System.out.println("    email: " + n));
        System.out.println();
        System.out.println("  Four required steps, one hook, one override. Six steps, in the");
        System.out.println("  same order as the other three, for free.");
    }

    // ---- 5 --------------------------------------------------------------

    private static void whatItCost() {
        System.out.println();
        System.out.println("=== 5. What it cost ===");
        System.out.println();
        System.out.println("  Inheritance. Every route is welded to FulfilmentProcess and can");
        System.out.println("  extend nothing else, and a new step in the base class lands on");
        System.out.println("  all four at once. Compose strategies instead when the steps are");
        System.out.println("  independent enough to be swapped at runtime; use this when the");
        System.out.println("  ORDER is the thing you are trying to guarantee.");
    }

    // ---- fixtures -------------------------------------------------------

    private static void printSteps(FulfilmentReport report) {
        report.steps().forEach(s -> System.out.println("    " + s));
    }

    private static StockLedger warehouseStock() {
        return new StockLedger().stock("H-100", 20).stock("C-220", 50).stock("K-330", 8);
    }

    private static SellerApi acme() {
        return new SellerApi("Acme Optics").willConfirm("L-900", "L-901");
    }

    private static Order warehouseOrder(String id) {
        return Order.shipped(id, "grace@example.com", "4 Blackfriars Road, London",
                List.of(new OrderLine("H-100", "Wireless headphones", Money.pounds(89.99), 2),
                        new OrderLine("C-220", "USB-C cable", Money.pounds(7.50), 1)));
    }

    private static Order marketplaceOrder(String id) {
        return Order.shipped(id, "priya@example.com", "12 Mill Lane, Bath",
                List.of(new OrderLine("L-900", "Macro lens", Money.pounds(129.00), 1)));
    }

    private static Order digitalOrder(String id) {
        return Order.addressless(id, "sam@example.com",
                List.of(new OrderLine("E-777", "Recipe e-book", Money.pounds(9.99), 1),
                        new OrderLine("E-778", "Meal planner", Money.pounds(4.50), 1)));
    }

    private FulfilmentDemo() {
    }
}
