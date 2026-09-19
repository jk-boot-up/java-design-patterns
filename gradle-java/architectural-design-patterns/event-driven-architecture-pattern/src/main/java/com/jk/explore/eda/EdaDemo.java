package com.jk.explore.eda;

import java.util.ArrayList;
import java.util.List;

public class EdaDemo {

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. Calling each other.");
        DirectShop shop = new DirectShop(false);
        boolean accepted = shop.place("ORD-1");
        System.out.println("  the order service calls shipping and waits. shipping is down. order accepted: " + accepted + ". orders placed: " + shop.placed() + ".");
        System.out.println("  a customer lost an order because a service they never see was down.");
    }

    private static void two() {
        System.out.println("TWO. Telling the log.");
        EventLog log = new EventLog();
        OrderService orders = new OrderService(log);
        List<String> heard = new ArrayList<>();
        Reactor inventory = new Reactor("inventory", false, e -> heard.add("inventory reserved " + e.orderId()));
        Reactor shipping = new Reactor("shipping", false, e -> heard.add("shipping planned " + e.orderId()));
        int offset = orders.place("ORD-1");
        System.out.println("  the order service appended the event at offset " + offset + " and finished. it has no reference to inventory or shipping.");
        inventory.poll(log);
        shipping.poll(log);
        System.out.println("  " + heard + ".");
    }

    private static void three() {
        System.out.println("THREE. A service that is down.");
        EventLog log = new EventLog();
        OrderService orders = new OrderService(log);
        List<String> planned = new ArrayList<>();
        Reactor shipping = new Reactor("shipping", false, e -> planned.add(e.orderId()));
        shipping.goDown();
        orders.place("ORD-1");
        orders.place("ORD-2");
        orders.place("ORD-3");
        shipping.poll(log);
        System.out.println("  shipping is down. three orders were accepted anyway. shipping planned " + planned + ", and is " + shipping.lag(log) + " events behind.");
        shipping.comeUp();
        shipping.poll(log);
        System.out.println("  shipping came back and caught up: planned " + planned + ", " + shipping.lag(log) + " behind.");
    }

    private static void four() {
        System.out.println("FOUR. A new reader, and no change to the writer.");
        EventLog log = new EventLog();
        OrderService orders = new OrderService(log);
        orders.place("ORD-1");
        orders.place("ORD-2");
        List<String> counted = new ArrayList<>();
        Reactor analytics = new Reactor("analytics", false, e -> counted.add(e.orderId()));
        analytics.poll(log);
        System.out.println("  analytics was added after two orders. it read the log from the start: " + counted + ".");
        System.out.println("  the order service was not touched. the log is kept, so a new service can be built from history.");
    }

    private static void five() {
        System.out.println("FIVE. Not the same instant.");
        EventLog log = new EventLog();
        OrderService orders = new OrderService(log);
        Warehouse warehouse = new Warehouse(10);
        Reactor inventory = new Reactor("inventory", false, warehouse::reserve);
        orders.place("ORD-1");
        System.out.println("  the order is accepted. stock in the warehouse: " + warehouse.stock() + ". it should be 9.");
        inventory.poll(log);
        System.out.println("  after inventory reads the log: " + warehouse.stock() + ".");
        System.out.println("  for a moment the two disagree. the system is eventually consistent, not consistent at every instant.");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        EventLog log = new EventLog();
        OrderService orders = new OrderService(log);
        Warehouse plain = new Warehouse(10);
        Warehouse careful = new Warehouse(10);
        Reactor plainReader = new Reactor("plain", false, plain::reserve);
        Reactor carefulReader = new Reactor("careful", true, careful::reserve);
        orders.place("ORD-1");
        plainReader.poll(log);
        carefulReader.poll(log);
        Event again = log.readFrom(0).get(0);
        plainReader.redeliver(again);
        carefulReader.redeliver(again);
        System.out.println("  the same event delivered twice. stock: without a duplicate check " + plain.stock() + ", with one " + careful.stock() + ". it should be 9.");
        System.out.println("  and the flow of an order is now spread over several services, each reading the log: to see it, you read the log, not one piece of code.");
    }
}
