package com.jk.explore.publishersubscriber;

import com.jk.explore.publishersubscriber.naive.DirectOrderService;

import java.util.ArrayList;
import java.util.List;

public class PublisherSubscriberDemo {

    static final java.util.function.Predicate<Event> ANY = e -> true;
    static final java.util.function.Predicate<Event> PLACED = e -> e.kind().equals("OrderPlaced");

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. The order service calls each one.");
        List<String> inventory = new ArrayList<>();
        List<String> email = new ArrayList<>();
        List<String> analytics = new ArrayList<>();
        new DirectOrderService(inventory, email, analytics).place("ORD-1");
        System.out.println("  inventory " + inventory + ", email " + email + ", analytics " + analytics + ".");
        System.out.println("  the order service knows " + DirectOrderService.servicesItKnows() + " services by name. a fourth, loyalty points, means editing it.");
    }

    private static void two() {
        System.out.println("TWO. The order service only publishes.");
        Topic orders = new Topic();
        List<String> inventory = new ArrayList<>();
        List<String> email = new ArrayList<>();
        List<String> analytics = new ArrayList<>();
        var i = orders.subscribeFromStart("inventory", ANY, e -> inventory.add(e.orderId()));
        var m = orders.subscribeFromStart("email", ANY, e -> email.add(e.orderId()));
        var a = orders.subscribeFromStart("analytics", ANY, e -> analytics.add(e.orderId()));
        orders.publish(new Event("OrderPlaced", "ORD-1"));
        i.deliver(10);
        m.deliver(10);
        a.deliver(10);
        System.out.println("  inventory " + inventory + ", email " + email + ", analytics " + analytics + ".");
        List<String> loyalty = new ArrayList<>();
        var l = orders.subscribeFromStart("loyalty", ANY, e -> loyalty.add(e.orderId()));
        l.deliver(10);
        System.out.println("  a fourth subscriber, loyalty points, is added: " + loyalty + ". the order service was not changed.");
    }

    private static void three() {
        System.out.println("THREE. Each at its own pace.");
        Topic orders = new Topic();
        int[] fast = {0};
        int[] slow = {0};
        var f = orders.subscribeFromStart("email", ANY, e -> fast[0]++);
        var s = orders.subscribeFromStart("analytics", ANY, e -> slow[0]++);
        for (int i = 1; i <= 5; i++) {
            orders.publish(new Event("OrderPlaced", "ORD-" + i));
        }
        f.deliver(10);
        s.deliver(1);
        System.out.println("  5 orders published. email handled " + fast[0] + ", analytics handled " + slow[0] + ". backlog of email: " + f.backlog() + ", of analytics: " + s.backlog() + ".");
        s.deliver(10);
        System.out.println("  analytics catches up later: handled " + slow[0] + ", backlog " + s.backlog() + ". a slow subscriber did not hold up the fast one, or the publisher.");
    }

    private static void four() {
        System.out.println("FOUR. Each takes what it wants.");
        Topic orders = new Topic();
        List<String> email = new ArrayList<>();
        List<String> analytics = new ArrayList<>();
        var m = orders.subscribeFromStart("email", PLACED, e -> email.add(e.kind() + " " + e.orderId()));
        var a = orders.subscribeFromStart("analytics", ANY, e -> analytics.add(e.kind() + " " + e.orderId()));
        orders.publish(new Event("OrderPlaced", "ORD-1"));
        orders.publish(new Event("OrderCancelled", "ORD-1"));
        m.deliver(10);
        a.deliver(10);
        System.out.println("  email asked only for placed orders: " + email + ".");
        System.out.println("  analytics asked for everything: " + analytics + ".");
    }

    private static void five() {
        System.out.println("FIVE. A subscriber that arrives late.");
        Topic orders = new Topic();
        for (int i = 1; i <= 3; i++) {
            orders.publish(new Event("OrderPlaced", "ORD-" + i));
        }
        List<String> live = new ArrayList<>();
        List<String> replay = new ArrayList<>();
        var l = orders.subscribeLive("loyalty-live", ANY, e -> live.add(e.orderId()));
        var r = orders.subscribeFromStart("loyalty-replay", ANY, e -> replay.add(e.orderId()));
        orders.publish(new Event("OrderPlaced", "ORD-4"));
        l.deliver(10);
        r.deliver(10);
        System.out.println("  3 orders were published before loyalty was added, and one after.");
        System.out.println("  a subscriber that joins live sees: " + live + ". one that reads from the start sees: " + replay + ".");
        System.out.println("  keeping the log is what makes a late subscriber possible, and it has to be kept somewhere.");
    }

    private static void six() {
        System.out.println("SIX. The bill: nobody knows who got it.");
        Topic orders = new Topic();
        List<String> email = new ArrayList<>();
        var m = orders.subscribeFromStart("email", ANY, e -> email.add(e.orderId()));
        m.disconnect();
        orders.publish(new Event("OrderPlaced", "ORD-1"));
        m.deliver(10);
        System.out.println("  email was down when the order was placed. the publisher was told: nothing. email got: " + email + ", backlog " + m.backlog() + ".");
        m.reconnect();
        m.deliver(10);
        System.out.println("  when it came back, it caught up: " + email + ". because its place in the log was kept.");
        System.out.println("  the publisher still cannot ask whether the email went out. it published, and it does not know who listened.");
    }
}
