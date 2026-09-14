package com.jk.explore.idempotentconsumer;

/**
 * Five acts. The HashSet that nearly works, the deploy that empties it, the crash that
 * outsmarts it, the id written in the same transaction as the effect, and the handler that
 * needed none of this.
 */
public final class OrderPlacedTwiceDemo {

    private OrderPlacedTwiceDemo() {
    }

    public static void main(String[] args) {
        theHashSetThatNearlyWorks();
        theDeployThatEmptiesIt();
        theCrashThatOutsmartsIt();
        theIdAndTheEffectTogether();
        theHandlerThatNeededNoneOfThis();
    }

    /** Act 1: the duplicate arrives and the HashSet catches it. */
    private static void theHashSetThatNearlyWorks() {
        System.out.println("Act 1 - the same OrderPlaced arrives twice");

        Shop shop = new Shop();
        NaiveNotificationConsumer consumer =
                new NaiveNotificationConsumer(shop.database, shop.log);
        shop.broker.deliverTwice(orderPlaced("msg-1", "ord-7001"), consumer);

        System.out.print(shop.log.timeline());
        System.out.println("  confirmations queued: " + shop.database.confirmationsQueued());
        System.out.println("  a HashSet of ids caught the duplicate. This is the test"
                + " everybody writes, and it passes.");
        System.out.println();
    }

    /** Act 2: the memory was in the process, and the process was replaced. */
    private static void theDeployThatEmptiesIt() {
        System.out.println("Act 2 - a deploy lands between the two deliveries");

        Shop shop = new Shop();
        NaiveNotificationConsumer consumer =
                new NaiveNotificationConsumer(shop.database, shop.log);
        Message message = orderPlaced("msg-1", "ord-7002");

        shop.broker.deliver(message, consumer);
        consumer.restart();
        shop.broker.deliver(message, consumer);

        System.out.print(shop.log.timeline());
        System.out.println("  confirmations queued: " + shop.database.confirmationsQueued());
        for (String confirmation : shop.database.confirmations()) {
            System.out.println("    \"" + confirmation + "\"");
        }
        System.out.println("  the database survived the deploy. The HashSet did not.");
        System.out.println("  and a restart is often exactly why the acknowledgement was"
                + " lost, so this pairing is common, not unlucky.");
        System.out.println();
    }

    /** Act 3: the id is written after the work, so a crash in between loses it. */
    private static void theCrashThatOutsmartsIt() {
        System.out.println("Act 3 - the crash between the work and the record");

        Shop shop = new Shop();
        NaiveNotificationConsumer consumer =
                new NaiveNotificationConsumer(shop.database, shop.log);
        Message message = orderPlaced("msg-1", "ord-7003");

        consumer.dieAfterQueueing();
        try {
            shop.broker.deliver(message, consumer);
        } catch (ProcessDiedException died) {
            System.out.println("  " + died.getMessage());
        }
        consumer.restart();
        shop.broker.deliver(message, consumer);

        System.out.print(shop.log.timeline());
        System.out.println("  confirmations queued: " + shop.database.confirmationsQueued());
        System.out.println("  the email was queued and the id was not remembered, so the"
                + " redelivery queued it again");
        System.out.println("  two emails is embarrassing. Had this consumer been Payments,"
                + " it would have been two charges.");
        System.out.println();
    }

    /** Act 4: check the store, then commit the effect and the id together. */
    private static void theIdAndTheEffectTogether() {
        System.out.println("Act 4 - the id written in the same transaction as the effect");

        Shop shop = new Shop();
        IdempotentNotificationConsumer consumer =
                new IdempotentNotificationConsumer(shop.database, shop.log);
        Message message = orderPlaced("msg-1", "ord-7004");

        shop.broker.deliverTwice(message, consumer);
        System.out.print(shop.log.timeline());
        System.out.println("  confirmations queued: " + shop.database.confirmationsQueued()
                + ", handled ids stored: " + shop.database.handledCount());

        System.out.println("  now the same two failures that beat the HashSet:");
        consumer.restart();
        shop.broker.deliver(message, consumer);
        System.out.println("    after a restart, confirmations queued: "
                + shop.database.confirmationsQueued());

        Shop second = new Shop();
        IdempotentNotificationConsumer crashy =
                new IdempotentNotificationConsumer(second.database, second.log);
        Message other = orderPlaced("msg-2", "ord-7005");
        crashy.dieBeforeCommitting();
        try {
            second.broker.deliver(other, crashy);
        } catch (ProcessDiedException died) {
            System.out.println("    " + died.getMessage()
                    + ", and nothing at all was written: "
                    + second.database.confirmationsQueued() + " confirmation(s), "
                    + second.database.handledCount() + " id(s)");
        }
        crashy.restart();
        second.broker.deliver(other, crashy);
        System.out.println("    after the redelivery, confirmations queued: "
                + second.database.confirmationsQueued());
        System.out.println("  exactly once, out of a broker that only promises at least once.");
        System.out.println();
    }

    /** Act 5: some handlers need no store, and some need rewriting rather than a store. */
    private static void theHandlerThatNeededNoneOfThis() {
        System.out.println("Act 5 - the handler that needed none of this");

        Shop shop = new Shop();
        ShipmentStatusConsumer shipping = new ShipmentStatusConsumer(shop.log);
        shop.broker.deliverTwice(orderShipped("msg-3", "ord-7006"), shipping);

        System.out.println("  status of ord-7006: " + shipping.statusOf("ord-7006")
                + ", orders known: " + shipping.ordersKnown());
        System.out.println("  no dedupe store, no transaction, no expiry policy. Setting a"
                + " status twice sets the same status.");
        System.out.println("  that is a naturally idempotent operation, and it is always the"
                + " better answer when it is available.");
        System.out.println();

        LoyaltyPointsConsumer loyalty = new LoyaltyPointsConsumer(shop.log);
        Message placed = orderPlaced("msg-4", "ord-7007");
        shop.broker.deliverTwice(placed, loyalty);
        System.out.println("  and one that is not: \"add 70 loyalty points\" twice");
        System.out.println("    running total: " + loyalty.runningTotal()
                + " points for a 70 pound order");
        loyalty.awardForOrder(placed);
        loyalty.awardForOrder(placed);
        System.out.println("  rewritten as \"set the points for this order to 70\":");
        System.out.println("    points awarded: " + loyalty.pointsAwarded()
                + " after handling it twice");
        System.out.println("  ask whether the handler can be rewritten before reaching for a"
                + " dedupe table.");
        System.out.println();

        System.out.println("  and the dedupe store's own cost, which is a guess:");
        IdempotentNotificationConsumer notifications =
                new IdempotentNotificationConsumer(shop.database, shop.log);
        Message late = orderPlaced("msg-5", "ord-7008");
        shop.broker.deliver(late, notifications);
        System.out.println("    handled, confirmations queued: "
                + shop.database.confirmationsQueued());
        shop.clock.advance(60_000);
        shop.database.forgetHandledOlderThan(30_000);
        shop.broker.deliver(late, notifications);
        System.out.println("    a minute later, with a thirty second memory, the same message"
                + " arrives again: " + shop.database.confirmationsQueued()
                + " confirmation(s)");
        System.out.println("  ids cannot be kept forever, so they expire, and the window is"
                + " chosen rather than derived.");
        System.out.println("  too short and a duplicate after a long broker outage looks new;"
                + " too long and it is a large table somebody operates.");
    }

    private static Message orderPlaced(String messageId, String orderId) {
        return new Message(messageId, "OrderPlaced", orderId, Money.pence(7095));
    }

    private static Message orderShipped(String messageId, String orderId) {
        return new Message(messageId, "OrderShipped", orderId, Money.pence(7095));
    }

    /** The broker and the Notifications database, fresh for each act. */
    private static final class Shop {

        private final SimulatedClock clock = new SimulatedClock();
        private final CallLog log = new CallLog(clock);
        private final NotificationsDatabase database = new NotificationsDatabase(clock, log);
        private final MessageBroker broker = new MessageBroker(clock, log);
    }
}
