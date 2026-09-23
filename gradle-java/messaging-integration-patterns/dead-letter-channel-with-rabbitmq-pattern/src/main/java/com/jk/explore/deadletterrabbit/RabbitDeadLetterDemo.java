package com.jk.explore.deadletterrabbit;

import com.rabbitmq.client.Connection;
import java.util.List;
import java.util.Set;

/**
 * Six acts against a real RabbitMQ broker, started and stopped by this demo.
 *
 * <p>The lesson is the line between the two sides. The shop writes a rule on a queue. The worker either
 * finishes an order or refuses it. Everything after that is the broker's decision, and the broker writes
 * down which rule it applied.
 */
public class RabbitDeadLetterDemo {

    private static final Order ORD_1001 = Order.of("ORD-1001", "ship to 12 Mill Lane, Leeds, card ending 4417");
    private static final Order ORD_1002 = Order.of("ORD-1002", "ship to ??? ?? ?????, card ending 9930");
    private static final Order ORD_1003 = Order.of("ORD-1003", "ship to 4 Harbour Road, Cork, card ending 2261");
    private static final Order ORD_1004 = Order.of("ORD-1004", "ship to 88 Anna Salai, Chennai, card ending 7715");
    private static final Order ORD_1005 = Order.of("ORD-1005", "ship to 3 Bridge Street, Perth, card ending 6002");
    private static final Order ORD_1006 = Order.of("ORD-1006", "ship to 19 Rua Augusta, Lisbon, card ending 3318");
    private static final Order ORD_1007 = Order.of("ORD-1007", "ship to 7 Bay Ridge, Brooklyn, card ending 5240");
    private static final Order ORD_1008 = Order.of("ORD-1008", "ship to 2 Kloof Street, Cape Town, card ending 8806");

    public static void main(String[] args) throws Exception {
        System.setProperty("org.slf4j.simpleLogger.defaultLogLevel", "error");
        if (!Broker.dockerAvailable()) {
            System.out.println(Broker.NO_RUNTIME_ADVICE);
            return;
        }
        try (Broker broker = new Broker()) {
            try {
                broker.start();
            } catch (RuntimeException e) {
                System.out.println(Broker.NO_BROKER_ADVICE);
                return;
            }
            try (Connection connection = broker.connect();
                 OrderChannel orders = new OrderChannel(connection)) {
                one(connection, orders);
                two(connection, orders);
                three(connection, orders);
                four(connection, orders);
                five(connection, orders);
                six(connection, orders);
            }
        }
    }

    /** With no rule on the queue, a refused order comes straight back and blocks everything behind it. */
    private static void one(Connection connection, OrderChannel orders) throws Exception {
        System.out.println("ONE. An order that can never succeed.");
        String queue = "orders.plain";
        orders.workingQueue(queue);
        orders.publish(queue, ORD_1001);
        orders.publish(queue, ORD_1002);
        orders.publish(queue, ORD_1003);
        orders.publish(queue, ORD_1004);
        Broker.waitUntil("four orders are on " + queue, () -> orders.waiting(queue) == 4);
        try (Worker worker = Worker.neverGivingUp(connection, queue, new Shipping(Set.of()))) {
            worker.work(12);
            Broker.waitUntil("three orders are left on " + queue, () -> orders.waiting(queue) == 3);
            System.out.println("  four orders, one with an address nothing can read. handled: " + worker.handled()
                    + ". still waiting: " + orders.waiting(queue) + ". deliveries of ORD-1002: " + worker.deliveriesOf("ORD-1002") + ".");
            System.out.println("  the worker refuses it and asks for it back, so the broker returns it to the head of the queue. ORD-1003 and ORD-1004 never get their turn.");
        }
    }

    /** The queue carries a rule naming where a dead order goes, and the broker moves it there. */
    private static void two(Connection connection, OrderChannel orders) throws Exception {
        System.out.println("TWO. A dead letter channel, made of a real exchange and a real queue.");
        String queue = "orders.work";
        String parked = "orders.parked.rejected";
        orders.parkedQueue(parked, "rejected");
        orders.workingQueueWithParking(queue, "rejected");
        orders.publish(queue, ORD_1001);
        orders.publish(queue, ORD_1002);
        orders.publish(queue, ORD_1003);
        orders.publish(queue, ORD_1004);
        try (Worker worker = Worker.givingUpAfter(3, connection, queue, new Shipping(Set.of("ORD-1003")));
             ParkedOrders parkedOrders = new ParkedOrders(connection, parked)) {
            worker.work(20);
            Broker.waitUntil("one order is parked", () -> parkedOrders.waiting() == 1);
            System.out.println("  the worker gives each order three deliveries. after the third it refuses ORD-1002 for good, and the broker takes it out of the queue.");
            System.out.println("  handled: " + worker.handled() + ". still waiting: " + orders.waiting(queue)
                    + ". parked: " + parkedOrders.waiting() + ". deliveries in all: " + worker.totalDeliveries() + ".");
            System.out.println("  ORD-1003 failed once on a payment gateway timeout and went through on its second delivery. a slow day is not a dead order.");
        }
    }

    /** The broker attaches its own note to the order it parked, and the order itself is untouched. */
    private static void three(Connection connection, OrderChannel orders) throws Exception {
        System.out.println("THREE. The broker writes down why.");
        try (ParkedOrders parkedOrders = new ParkedOrders(connection, "orders.parked.rejected")) {
            List<DeadLetter> parked = parkedOrders.takeAll();
            DeadLetter letter = parked.get(0);
            System.out.println("  " + letter.id() + ": reason " + letter.reason() + ", from queue " + letter.fromQueue() + ", died " + letter.count() + " time.");
            System.out.println("  the order itself is exactly as the shop sent it: " + letter.body());
            System.out.println("  the application wrote none of that. the broker did, and it will be there tomorrow morning.");
        }
    }

    /** Two more ways an order dies, neither of them a refusal by a worker. */
    private static void four(Connection connection, OrderChannel orders) throws Exception {
        System.out.println("FOUR. Not every death is a refusal.");
        String slow = "orders.slow";
        String parkedExpired = "orders.parked.expired";
        orders.parkedQueue(parkedExpired, "expired");
        orders.workingQueueWithTimeLimit(slow, "expired", 500);
        orders.publish(slow, ORD_1005);
        try (ParkedOrders parkedOrders = new ParkedOrders(connection, parkedExpired)) {
            Broker.waitUntil("ORD-1005 ran out of time", () -> parkedOrders.waiting() == 1);
            DeadLetter letter = parkedOrders.takeAll().get(0);
            System.out.println("  ORD-1005 sat in a queue with a time limit of 500 milliseconds and nobody read it: reason " + letter.reason()
                    + ", from queue " + letter.fromQueue() + ".");
        }
        String small = "orders.small";
        String parkedFull = "orders.parked.full";
        orders.parkedQueue(parkedFull, "full");
        orders.workingQueueWithSizeLimit(small, "full", 2);
        orders.publish(small, ORD_1006);
        orders.publish(small, ORD_1007);
        orders.publish(small, ORD_1008);
        try (ParkedOrders parkedOrders = new ParkedOrders(connection, parkedFull)) {
            Broker.waitUntil("the full queue pushed one order out", () -> parkedOrders.waiting() == 1);
            DeadLetter letter = parkedOrders.takeAll().get(0);
            System.out.println("  a queue that holds two orders was sent three. the broker pushed the oldest out: " + letter.id()
                    + ", reason " + letter.reason() + ". still waiting there: " + orders.waiting(small) + ".");
            System.out.println("  no worker refused either order. the broker decided both times, and named the rule it applied.");
        }
    }

    /** Parked orders are kept, so once the cause is fixed they can be put back. */
    private static void five(Connection connection, OrderChannel orders) throws Exception {
        System.out.println("FIVE. Fix it, and put it back.");
        String queue = "orders.replay";
        String parked = "orders.parked.replay";
        orders.parkedQueue(parked, "replay");
        orders.workingQueueWithParking(queue, "replay");
        orders.publish(queue, ORD_1001);
        orders.publish(queue, ORD_1002);
        orders.publish(queue, ORD_1003);
        orders.publish(queue, ORD_1004);
        Shipping shipping = new Shipping(Set.of());
        try (Worker worker = Worker.givingUpAfter(3, connection, queue, shipping);
             ParkedOrders parkedOrders = new ParkedOrders(connection, parked)) {
            worker.work(20);
            Broker.waitUntil("one order is parked", () -> parkedOrders.waiting() == 1);
            System.out.println("  before the fix: handled " + worker.handled() + ", parked " + parkedOrders.waiting() + ".");
            shipping.fixTheAddressParser();
            int replayed = parkedOrders.replayTo(orders, queue);
            Broker.waitUntil("the replayed order is back on " + queue, () -> orders.waiting(queue) == 1);
            worker.work(20);
            System.out.println("  the address parser is fixed and " + replayed + " parked order is published back onto the working queue. handled: "
                    + worker.handled() + ". parked: " + parkedOrders.waiting() + ".");
            System.out.println("  note the order: ORD-1002 was handled after ORD-1003 and ORD-1004. a replay does not restore the order things were sent in.");
            System.out.println("  and it goes back as a new message, so the broker's note is gone unless the operator copies it across first.");
        }
    }

    /** The cost of the pattern: a queue nobody watches, full of orders somebody paid for. */
    private static void six(Connection connection, OrderChannel orders) throws Exception {
        System.out.println("SIX. The bill: nobody is looking.");
        String queue = "orders.bill";
        String parked = "orders.parked.bill";
        orders.parkedQueue(parked, "bill");
        orders.workingQueueWithParking(queue, "bill");
        for (int i = 1; i <= 40; i++) {
            orders.publish(queue, i % 2 == 0
                    ? Order.of("ORD-20" + String.format("%02d", i), "ship to ??? ?? ?????, card ending 0000")
                    : Order.of("ORD-20" + String.format("%02d", i), "ship to 5 Pier Road, Galway, card ending 1290"));
        }
        try (Worker worker = Worker.givingUpAfter(1, connection, queue, new Shipping(Set.of()));
             ParkedOrders parkedOrders = new ParkedOrders(connection, parked)) {
            worker.work(80);
            Broker.waitUntil("twenty orders are parked", () -> parkedOrders.waiting() == 20);
            System.out.println("  40 orders, half of them unreadable: " + parkedOrders.waiting() + " parked, " + worker.handled().size()
                    + " shipped, and every one of those 40 was paid for by a customer.");
            System.out.println("  the working queue reports " + orders.waiting(queue) + " waiting, so every dashboard shows the shop healthy. the loss is in the parked queue, and nothing tells anyone to look at it.");
            System.out.println("  a parked queue needs an owner, an alert on its depth, and a limit on how long an order may stay, because each parked order is a copy of a customer's address.");
            System.out.println("  and a broker is another thing to run: this demo declared " + orders.queuesDeclared() + " queues and "
                    + orders.exchangesDeclared() + " exchange in 1 RabbitMQ container, and took the container away at the end.");
        }
    }
}
