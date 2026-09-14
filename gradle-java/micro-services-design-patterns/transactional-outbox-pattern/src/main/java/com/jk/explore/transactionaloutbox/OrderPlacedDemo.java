package com.jk.explore.transactionaloutbox;

/**
 * Five acts. The two lines that work, the two lines that lose an order event, the out-tray, the
 * broker being down, and the price the out-tray charges.
 */
public final class OrderPlacedDemo {

    private OrderPlacedDemo() {
    }

    public static void main(String[] args) {
        theTwoLinesThatUsuallyWork();
        theTwoLinesOnABadDay();
        theOutTray();
        theBrokerGoesDown();
        thePriceOfNeverLosingIt();
    }

    /** Act 1: save then publish. On a good day it is fine, and it is fine most days. */
    private static void theTwoLinesThatUsuallyWork() {
        System.out.println("Act 1 - save the order, then publish the event");

        Shop shop = new Shop();
        new NaiveOrderService(shop.database, shop.broker, shop.log)
                .placeOrder(order("ord-8001"));

        System.out.print(shop.log.timeline());
        System.out.println("  orders saved: " + shop.database.orderCount()
                + ", events delivered: " + shop.broker.deliveredCount()
                + ", emails sent: " + shop.notifications.emailsSent());
        System.out.println("  two lines, and they did the right thing. This is what every"
                + " test the author writes will see.");
        System.out.println();
    }

    /** Act 2: the same two lines, with the process dying in the gap between them. */
    private static void theTwoLinesOnABadDay() {
        System.out.println("Act 2 - the same two lines, and a deploy lands in between");

        Shop shop = new Shop();
        NaiveOrderService orders = new NaiveOrderService(shop.database, shop.broker, shop.log);
        orders.dieBetweenTheTwoLines();
        try {
            orders.placeOrder(order("ord-8002"));
        } catch (ProcessDiedException died) {
            System.out.println("  " + died.getMessage());
        }

        System.out.print(shop.log.timeline());
        System.out.println("  the order in the database: " + shop.database.find("ord-8002"));
        System.out.println("  events delivered: " + shop.broker.deliveredCount()
                + ", emails sent: " + shop.notifications.emailsSent());
        System.out.println("  the order is real. The customer will be charged. Nobody will"
                + " ever be told.");
        System.out.println("  and there is nothing left anywhere that knows a message was"
                + " owed, so nothing will retry.");
        System.out.println("  swapping the two lines round does not help: publish first and"
                + " a crash announces an order that does not exist.");
        System.out.println();
    }

    /** Act 3: one commit, two rows, and a collector that comes round after. */
    private static void theOutTray() {
        System.out.println("Act 3 - the message goes in the database, next to the order");

        Shop shop = new Shop();
        new OrderService(shop.database, shop.log).placeOrder(order("ord-8003"));

        System.out.println("  after the commit, before any sweep:");
        System.out.println("    orders saved: " + shop.database.orderCount()
                + ", messages waiting in the out-tray: " + shop.database.unsent().size()
                + ", events delivered: " + shop.broker.deliveredCount());
        System.out.println("  Orders never called the broker. Now the relay comes round:");
        int published = shop.relay().sweep();

        System.out.print(shop.log.timeline());
        System.out.println("  published on that sweep: " + published);
        System.out.println("  messages still waiting: " + shop.database.unsent().size()
                + ", emails sent: " + shop.notifications.emailsSent());
        System.out.println("  the order and the message were written by one commit, so there"
                + " is no moment where one exists without the other.");
        System.out.println();
    }

    /** Act 4: the broker is down for a while, and nothing is lost or even noticed. */
    private static void theBrokerGoesDown() {
        System.out.println("Act 4 - the broker is down while the shop is busy");

        Shop shop = new Shop();
        OrderService orders = new OrderService(shop.database, shop.log);
        orders.placeOrder(order("ord-8004"));
        orders.placeOrder(order("ord-8005"));
        System.out.println("  two customers checked out while the broker was unreachable"
                + " -- checkout does not depend on it");

        shop.broker.failNext(2);
        System.out.println("  first sweep, broker still down: published "
                + shop.relay().sweep());
        System.out.println("  messages still in the out-tray: "
                + shop.database.unsent().size());
        System.out.println("  broker comes back. Second sweep: published "
                + shop.relay().sweep());

        System.out.print(shop.log.timeline());
        System.out.println("  events delivered: " + shop.broker.deliveredCount()
                + ", emails sent: " + shop.notifications.emailsSent()
                + ", still waiting: " + shop.database.unsent().size());
        System.out.println("  nobody wrote any retry logic. The retry is a consequence of"
                + " where the message is kept.");
        System.out.println();
    }

    /** Act 5: the gap the pattern cannot close, and the duplicate it lets through. */
    private static void thePriceOfNeverLosingIt() {
        System.out.println("Act 5 - what the guarantee costs");

        Shop shop = new Shop();
        new OrderService(shop.database, shop.log).placeOrder(order("ord-8006"));

        OutboxRelay relay = shop.relay();
        relay.dieAfterPublishing();
        relay.sweepAndSurvive();
        System.out.println("  the broker took the message. Emails sent: "
                + shop.notifications.emailsSent());
        System.out.println("  but the relay died before writing down that it had, so the"
                + " out-tray still holds: " + shop.database.unsent().size());

        relay.restart();
        relay.sweep();

        System.out.print(shop.log.timeline());
        System.out.println("  times message msg-1 was delivered: "
                + shop.broker.timesDelivered("msg-1"));
        System.out.println("  emails in the customer's inbox: "
                + shop.notifications.emailsSent());
        for (String email : shop.notifications.emails()) {
            System.out.println("    \"" + email + "\"");
        }
        System.out.println("  this is at-least-once delivery, and it is the deal: never"
                + " lost, sometimes twice.");
        System.out.println("  the fix is not in this project. It belongs to whoever receives"
                + " the message, and it is the next pattern along.");
        System.out.println("  note that the message id was the same both times. That is the"
                + " only thing a receiver needs to spot the duplicate.");
        System.out.println();
    }

    private static Order order(String orderId) {
        return new Order(orderId, "cust-7", Money.pence(7095));
    }

    /** Orders, its database, the broker and a subscriber, wired up fresh for each act. */
    private static final class Shop {

        private final SimulatedClock clock = new SimulatedClock();
        private final CallLog log = new CallLog(clock);
        private final OrderDatabase database = new OrderDatabase(log);
        private final MessageBroker broker = new MessageBroker(clock, log);
        private final NotificationService notifications = new NotificationService(log);

        private Shop() {
            broker.subscribe(notifications::on);
        }

        private OutboxRelay relay() {
            return new OutboxRelay(database, broker, log);
        }
    }
}
