package com.jk.explore.saga;

import java.util.List;

/**
 * Five acts. The saga working, the saga unwinding, the unwinding itself failing, a step that
 * cannot be unwound at all, and the try block everybody writes instead.
 */
public final class PlaceOrderSagaDemo {

    private static final String CUSTOMER = "cust-7";

    private PlaceOrderSagaDemo() {
    }

    public static void main(String[] args) {
        theHappyPath();
        shippingRefuses();
        theRefundFailsToo();
        theStepWithNoUndo();
        theTryBlockEverybodyWritesInstead();
    }

    /** Act 1: five services, five steps, one order. */
    private static void theHappyPath() {
        System.out.println("Act 1 - placing an order across five services");

        Shop shop = new Shop();
        SagaOutcome outcome = shop.saga().run(shop.basket("ord-9001"));

        System.out.print(shop.log.timeline());
        System.out.println("  outcome: " + outcome);
        System.out.println("  shipments scheduled: " + shop.shipping.shipmentsScheduled()
                + ", money held: " + shop.payments.netTaken());
        System.out.println("  no transaction spanned any of that. Each step committed"
                + " on its own.");
        System.out.println();
    }

    /** Act 2: the last step refuses, and the earlier four are cancelled out backwards. */
    private static void shippingRefuses() {
        System.out.println("Act 2 - no courier covers the postcode");

        Shop shop = new Shop();
        shop.shipping.refuseEveryPostcode();
        SagaOutcome outcome = shop.saga().run(shop.basket("ord-9002"));

        System.out.print(shop.log.timeline());
        System.out.println("  outcome: " + outcome);
        System.out.println("  kettles back on the shelf: "
                + shop.stock.available("SKU-KETTLE") + " of 20");
        System.out.println("  money the shop is holding: " + shop.payments.netTaken());
        System.out.println("  order state: " + shop.orders.stateOf("ord-9002"));
        System.out.println("  and note what the payment ledger looks like:");
        for (PaymentService.Entry entry : shop.payments.entries()) {
            System.out.println("    " + entry.kind() + " " + entry.amount()
                    + "  " + entry.ref());
        }
        System.out.println("  two lines, not zero. A refund is a new fact, not an erasure.");
        System.out.println("  the customer saw the money leave and come back, and may"
                + " well ring up to ask why.");
        System.out.println();
    }

    /** Act 3: the compensation fails as well. Somebody has to be told. */
    private static void theRefundFailsToo() {
        System.out.println("Act 3 - the refund fails as well");

        Shop shop = new Shop();
        shop.shipping.refuseEveryPostcode();
        shop.payments.failNextRefund(1);
        SagaOutcome outcome = shop.saga().run(shop.basket("ord-9003"));

        System.out.print(shop.log.timeline());
        System.out.println("  outcome: " + outcome);
        System.out.println("  needs a human: " + outcome.needsHumanHelp());
        System.out.println("  money the shop is holding that it should not: "
                + shop.payments.netTaken());
        System.out.println("  the order was still cancelled and the stock still released"
                + " -- unwinding does not give up at the first refusal");
        System.out.println("  in a real shop this outcome is a row in a queue that a"
                + " person works through. Not having one does not make it go away.");
        System.out.println();
    }

    /** Act 4: the same five steps in the wrong order. */
    private static void theStepWithNoUndo() {
        System.out.println("Act 4 - the confirmation email, sent too early");

        Shop shop = new Shop();
        shop.shipping.refuseEveryPostcode();
        SagaOutcome outcome = new SagaOrchestrator(
                PlaceOrderSteps.withTheEmailInTheWrongPlace(shop.stock, shop.payments,
                        shop.orders, shop.shipping, shop.email), shop.log)
                .run(shop.basket("ord-9004"));

        System.out.println("  outcome: " + outcome);
        System.out.println("  emails in the customer's inbox: " + shop.email.sent().size());
        for (String message : shop.email.sent()) {
            System.out.println("    \"" + message + "\"");
        }
        System.out.println("  the order is cancelled and the money is back, and that"
                + " email is still sitting there");
        System.out.println("  there is no unsend. The only fix is a second email"
                + " apologising, which is a new fact too.");
        System.out.println("  so steps that cannot be undone go last, after everything"
                + " that might fail.");
        System.out.println();
    }

    /** Act 5: four calls in a try block, and the money that stays taken. */
    private static void theTryBlockEverybodyWritesInstead() {
        System.out.println("Act 5 - the same failure, without a saga");

        Shop shop = new Shop();
        shop.shipping.refuseEveryPostcode();
        String shipment = new NaiveCheckoutService(shop.stock, shop.payments, shop.orders,
                shop.shipping, shop.log).placeOrder(shop.basket("ord-9005"));

        System.out.println("  returned: " + shipment);
        System.out.println("  card charged: " + shop.payments.netTaken());
        System.out.println("  kettles still reserved: "
                + (20 - shop.stock.available("SKU-KETTLE")));
        System.out.println("  order state: " + shop.orders.stateOf("ord-9005"));
        System.out.println("  shipments scheduled: " + shop.shipping.shipmentsScheduled());
        System.out.println("  nothing threw. A line went into a log. The customer has"
                + " paid for a parcel that will never be sent.");
        System.out.println("  a @Transactional annotation on that method would have"
                + " covered its own database and nothing else.");
        System.out.println();
    }

    /** The five services, wired up so every act starts from a clean shop. */
    private static final class Shop {

        private final SimulatedClock clock = new SimulatedClock();
        private final CallLog log = new CallLog(clock);
        private final StockService stock = new StockService(clock, log);
        private final PaymentService payments = new PaymentService(clock, log);
        private final OrderService orders = new OrderService(clock, log);
        private final ShippingService shipping = new ShippingService(clock, log);
        private final EmailService email = new EmailService(clock, log);

        private Shop() {
            stock.stock("SKU-KETTLE", 20);
            stock.stock("SKU-MUG", 50);
        }

        private SagaOrchestrator saga() {
            return new SagaOrchestrator(
                    PlaceOrderSteps.allOf(stock, payments, orders, shipping, email), log);
        }

        private SagaContext basket(String orderId) {
            return new SagaContext(orderId, CUSTOMER, List.of(
                    new SagaContext.Line("SKU-KETTLE", 1, Money.pence(3499)),
                    new SagaContext.Line("SKU-MUG", 4, Money.pence(899))));
        }
    }
}
