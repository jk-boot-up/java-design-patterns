package com.jk.explore.contentrouter;

import java.util.List;

public class ContentRouterDemo {

    static final List<Order> ORDERS = List.of(
            new Order("ORD-1", "physical", "UK", 4999),
            new Order("ORD-2", "gift-card", "UK", 2500),
            new Order("ORD-3", "physical", "EU", 120000),
            new Order("ORD-4", "gift-card", "UK", 90000),
            new Order("ORD-5", "subscription", "UK", 999),
            new Order("ORD-6", "physical", "EU", 3000));

    static Router standard() {
        return new Router("manual-review")
                .route("high value", o -> o.pence() >= 100000, "fraud-review")
                .route("gift card", o -> o.kind().equals("gift-card"), "digital-delivery")
                .route("physical", o -> o.kind().equals("physical"), "warehouse");
    }

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. One channel for everything.");
        long digital = ORDERS.stream().filter(o -> o.kind().equals("gift-card")).count();
        long other = ORDERS.stream().filter(o -> !o.kind().equals("physical") && !o.kind().equals("gift-card")).count();
        System.out.println("  all " + ORDERS.size() + " orders arrive on the warehouse's channel. " + digital + " are gift cards, which nothing physical can be done for, and " + other + (other == 1 ? " is" : " are") + " neither.");
        System.out.println("  the warehouse now has an if for each kind, and every new kind means changing the warehouse.");
    }

    private static void two() {
        System.out.println("TWO. A router looks inside.");
        Router r = standard();
        for (Order o : ORDERS) {
            System.out.println("  " + o.id() + " (" + o.kind() + ", " + o.region() + ", " + o.pence() + ") -> " + r.send(o));
        }
        System.out.println("  " + r.channels() + ".");
    }

    private static void three() {
        System.out.println("THREE. The first rule that matches wins.");
        Router first = standard();
        Router last = new Router("manual-review")
                .route("gift card", o -> o.kind().equals("gift-card"), "digital-delivery")
                .route("physical", o -> o.kind().equals("physical"), "warehouse")
                .route("high value", o -> o.pence() >= 100000, "fraud-review");
        Order big = new Order("ORD-7", "gift-card", "UK", 150000);
        System.out.println("  a gift card for 1500.00. with 'high value' first: " + first.send(big) + ". with it last: " + last.send(big) + ".");
        System.out.println("  the order of the rules is part of the design, and nothing warns you when it changes.");
    }

    private static void four() {
        System.out.println("FOUR. Nothing matches.");
        Router withFallback = standard();
        Router without = new Router(null).route("physical", o -> o.kind().equals("physical"), "warehouse");
        Order odd = new Order("ORD-8", "subscription", "UK", 999);
        System.out.println("  a subscription order, which no rule covers. with a fallback channel: " + withFallback.send(odd) + ".");
        System.out.println("  with no fallback: " + java.util.Objects.requireNonNullElse(without.send(odd), "nowhere") + ". orders dropped and counted: " + without.dropped() + ".");
        System.out.println("  a router with no fallback loses what it does not recognise, and says nothing.");
    }

    private static void five() {
        System.out.println("FIVE. A new route, and nobody else changes.");
        Router r = standard();
        int before = r.rules();
        r.route("EU region", o -> o.region().equals("EU"), "eu-vat-check");
        System.out.println("  rules before: " + before + ", after: " + r.rules() + ". senders and receivers were not touched.");
        System.out.println("  an EU subscription, which nothing before it covers, now goes to: " + r.send(new Order("ORD-10", "subscription", "EU", 999)) + ".");
        System.out.println("  ORD-6 (physical, EU) still goes to: " + r.send(ORDERS.get(5)) + ", because an earlier rule matched first.");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        Router r = new Router("manual-review").route("physical", o -> o.kind().equals("physical"), "warehouse");
        String renamed = new Order("ORD-9", "goods", "UK", 100).kind();
        System.out.println("  the sender starts calling physical orders 'goods'. the router's rule looks for 'physical': " + r.send(new Order("ORD-9", renamed, "UK", 100)) + ".");
        System.out.println("  the router reads the content, so it is coupled to the content's format. routing on a header keeps that in the envelope, at the cost of the sender having to fill it in.");
        System.out.println("  every route is a rule to test, and rules grow: this shop has " + standard().rules() + " today.");
    }
}
