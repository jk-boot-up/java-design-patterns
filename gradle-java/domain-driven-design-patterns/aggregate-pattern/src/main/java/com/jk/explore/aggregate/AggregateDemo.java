package com.jk.explore.aggregate;

import com.jk.explore.aggregate.domain.CustomerId;
import com.jk.explore.aggregate.domain.InvariantViolated;
import com.jk.explore.aggregate.domain.Money;
import com.jk.explore.aggregate.domain.Order;
import com.jk.explore.aggregate.domain.OrderId;
import com.jk.explore.aggregate.infrastructure.ConcurrentModification;
import com.jk.explore.aggregate.infrastructure.Loaded;
import com.jk.explore.aggregate.infrastructure.VersionedStore;
import com.jk.explore.aggregate.naive.CustomerRecord;
import com.jk.explore.aggregate.naive.CustomerWithOrders;
import com.jk.explore.aggregate.naive.EagerOrder;
import com.jk.explore.aggregate.naive.LooseOrder;

import java.util.function.Consumer;

public class AggregateDemo {

    static final Money MUG = Money.pounds(8);
    static final Money MACHINE = Money.pounds(300);

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    static String attempt(Runnable action) {
        try {
            action.run();
            return "accepted";
        } catch (InvariantViolated e) {
            return "refused, " + e.getMessage();
        }
    }

    private static void one() {
        System.out.println("ONE. A loose order.");
        LooseOrder order = new LooseOrder();
        order.lines.add(new LooseOrder.Line("MUG-BLUE", 800, -3));
        order.lines.add(new LooseOrder.Line("ESP-001", 30000, 10));
        order.lines.add(new LooseOrder.Line("ESP-001", 30000, 10));
        order.placed = true;
        order.lines.add(new LooseOrder.Line("BNS-220", 1250, 1));
        System.out.println("  a line of -3 mugs: in. the same machine on two lines: in. total: " + new Money(order.totalPence()) + ", past the £1000 limit: in.");
        System.out.println("  a line added to an order already placed: in.");
        System.out.println("  every rule is true in the head of the person who wrote the caller.");
    }

    private static void two() {
        System.out.println("TWO. The root guards the rules.");
        Order order = new Order(new OrderId("ORD-1"), new CustomerId("ada"));
        System.out.println("  0 mugs:            " + attempt(() -> order.addLine("MUG-BLUE", MUG, 0)));
        System.out.println("  11 mugs:           " + attempt(() -> order.addLine("MUG-BLUE", MUG, 11)));
        order.addLine("MUG-BLUE", MUG, 6);
        System.out.println("  6 mugs:            accepted. 5 more of the same: " + attempt(() -> order.addLine("MUG-BLUE", MUG, 5)));
        order.addLine("ESP-001", MACHINE, 2);
        System.out.println("  two more machines: " + attempt(() -> order.addLine("ESP-002", MACHINE, 2)) + ".");
        order.place();
        System.out.println("  after place():     " + attempt(() -> order.addLine("BNS-220", Money.pounds(12), 1)));
        System.out.println("  an empty order:    " + attempt(() -> new Order(new OrderId("ORD-2"), new CustomerId("ada")).place()));
    }

    private static void three() {
        System.out.println("THREE. There is only one door.");
        Order order = new Order(new OrderId("ORD-3"), new CustomerId("ada"));
        order.addLine("MUG-BLUE", MUG, 2);
        try {
            order.lines().clear();
        } catch (UnsupportedOperationException e) {
            System.out.println("  order.lines().clear(): UnsupportedOperationException.");
        }
        System.out.println("  an OrderLine has no public constructor, so none can exist that the order has not checked.");
        System.out.println("  lines seen from outside: " + order.lines().size() + ", total " + order.total() + ".");
    }

    private static void four() {
        System.out.println("FOUR. Other aggregates by id.");
        CustomerRecord.LOADS.set(0);
        for (int i = 0; i < 3; i++) {
            new EagerOrder(CustomerRecord.load("ada"));
        }
        System.out.println("  three orders that hold the whole customer: " + CustomerRecord.LOADS.get() + " customer loads.");
        CustomerRecord.LOADS.set(0);
        for (int i = 0; i < 3; i++) {
            new Order(new OrderId("ORD-" + i), new CustomerId("ada"));
        }
        System.out.println("  three orders that hold only a CustomerId: " + CustomerRecord.LOADS.get() + " customer loads.");
    }

    private static void five() {
        System.out.println("FIVE. Saved whole, or not at all.");
        VersionedStore<Order> orders = new VersionedStore<>(Order::copy);
        Order start = new Order(new OrderId("ORD-5"), new CustomerId("ada"));
        start.addLine("MUG-BLUE", MUG, 1);
        orders.insert("ORD-5", start);
        Loaded<Order> clerkA = orders.load("ORD-5");
        Loaded<Order> clerkB = orders.load("ORD-5");
        clerkA.value().addLine("BNS-220", Money.pounds(12), 1);
        clerkB.value().addLine("TEA-050", Money.pounds(5), 1);
        orders.save("ORD-5", clerkA);
        System.out.println("  clerk A adds beans and saves: accepted.");
        try {
            orders.save("ORD-5", clerkB);
        } catch (ConcurrentModification e) {
            System.out.println("  clerk B adds tea and saves: " + e.getMessage() + ".");
        }
        System.out.println("  the order was read whole, changed whole and saved whole, so a half-updated order cannot exist.");
    }

    private static void six() {
        System.out.println("SIX. An aggregate drawn too big.");
        VersionedStore<CustomerWithOrders> customers = new VersionedStore<>(CustomerWithOrders::copy);
        CustomerWithOrders ada = new CustomerWithOrders();
        for (String id : new String[]{"ORD-A", "ORD-B"}) {
            Order o = new Order(new OrderId(id), new CustomerId("ada"));
            o.addLine("MUG-BLUE", MUG, 1);
            ada.add(o);
        }
        customers.insert("ada", ada);
        Loaded<CustomerWithOrders> first = customers.load("ada");
        Loaded<CustomerWithOrders> second = customers.load("ada");
        first.value().addLineTo("ORD-A", "TEA-050", Money.pounds(5), 1);
        second.value().addLineTo("ORD-B", "BNS-220", Money.pounds(12), 1);
        customers.save("ada", first);
        String result;
        try {
            customers.save("ada", second);
            result = "accepted";
        } catch (ConcurrentModification e) {
            result = "refused, changed by someone else";
        }
        System.out.println("  one aggregate holding the customer and all their orders. two clerks change two different orders.");
        System.out.println("  the second save: " + result + ".");
        VersionedStore<Order> orders = new VersionedStore<>(Order::copy);
        for (String id : new String[]{"ORD-A", "ORD-B"}) {
            Order o = new Order(new OrderId(id), new CustomerId("ada"));
            o.addLine("MUG-BLUE", MUG, 1);
            orders.insert(id, o);
        }
        Loaded<Order> a = orders.load("ORD-A");
        Loaded<Order> b = orders.load("ORD-B");
        a.value().addLine("TEA-050", Money.pounds(5), 1);
        b.value().addLine("BNS-220", Money.pounds(12), 1);
        orders.save("ORD-A", a);
        orders.save("ORD-B", b);
        System.out.println("  one aggregate per order: both saves accepted.");
        System.out.println("  the boundary is a choice, and a boundary drawn too wide costs you false conflicts.");
    }
}
