package com.jk.explore.edakafka;

import java.util.ArrayList;
import java.util.List;

public class KafkaEdaDemo {

    public static void main(String[] args) throws Exception {
        if (!Broker.toolsAvailable()) {
            System.out.println("This demo needs Docker running, and the Kafka image. Start Docker, and run it again.");
            return;
        }
        System.setProperty("org.slf4j.simpleLogger.defaultLogLevel", "error");
        try (Broker broker = new Broker()) {
            broker.start();
            String run = Long.toString(System.currentTimeMillis());
            one();
            two(broker, "orders-two-" + run, run);
            three(broker, "orders-three-" + run, run);
            four(broker, "orders-four-" + run, run);
            five(broker, "orders-five-" + run, run);
            six(broker, "orders-six-" + run, run);
        }
    }

    private static void one() {
        System.out.println("ONE. Calling and waiting.");
        DirectShop shop = new DirectShop(false);
        System.out.println("  the order service calls shipping and waits. shipping is down. order accepted: " + shop.place("ORD-1") + ". orders placed: " + shop.placed() + ".");
        System.out.println("  a customer lost an order because a service they never see was down.");
    }

    private static void two(Broker broker, String topic, String run) throws Exception {
        System.out.println("TWO. Telling the log.");
        broker.createTopic(topic);
        List<String> heard = new ArrayList<>();
        try (OrderService orders = new OrderService(topic);
             Reader inventory = new Reader("inventory-" + run, topic, true, false, e -> heard.add("inventory saw " + e));
             Reader shipping = new Reader("shipping-" + run, topic, true, false, e -> heard.add("shipping saw " + e))) {
            long offset = orders.place("ORD-1");
            inventory.read(1);
            shipping.read(1);
            System.out.println("  the order service sent the event to Kafka, which gave it offset " + offset + ", and finished. it has no reference to inventory or shipping.");
            System.out.println("  " + heard + ".");
        }
    }

    private static void three(Broker broker, String topic, String run) throws Exception {
        System.out.println("THREE. A service that is down.");
        broker.createTopic(topic);
        String group = "shipping-" + run;
        List<String> planned = new ArrayList<>();
        try (OrderService orders = new OrderService(topic)) {
            orders.place("ORD-1");
            try (Reader shipping = new Reader(group, topic, true, false, planned::add)) {
                shipping.read(1);
            }
            orders.place("ORD-2");
            orders.place("ORD-3");
            orders.place("ORD-4");
            System.out.println("  shipping read ORD-1 and then went down. three more orders were accepted. shipping is " + Reader.lag(group, topic) + " events behind, as the broker counts it.");
            try (Reader shipping = new Reader(group, topic, true, false, planned::add)) {
                shipping.read(3);
            }
            System.out.println("  shipping came back and caught up, from where it stopped. it has now planned " + planned.size() + " orders, and is " + Reader.lag(group, topic) + " behind.");
        }
    }

    private static void four(Broker broker, String topic, String run) throws Exception {
        System.out.println("FOUR. A new reader, and no change to the writer.");
        broker.createTopic(topic);
        List<String> counted = new ArrayList<>();
        try (OrderService orders = new OrderService(topic)) {
            orders.place("ORD-1");
            orders.place("ORD-2");
            try (Reader analytics = new Reader("analytics-" + run, topic, true, false, counted::add)) {
                analytics.read(2);
            }
        }
        System.out.println("  analytics was added after two orders. it read the topic from the start: " + counted + ".");
        System.out.println("  the order service was not touched. Kafka keeps the events, so a new service can be built from history.");
    }

    private static void five(Broker broker, String topic, String run) throws Exception {
        System.out.println("FIVE. Not the same instant.");
        broker.createTopic(topic);
        Warehouse warehouse = new Warehouse(10);
        try (OrderService orders = new OrderService(topic);
             Reader inventory = new Reader("inventory-" + run, topic, true, false, warehouse::reserve)) {
            orders.place("ORD-1");
            System.out.println("  the order is accepted. stock in the warehouse: " + warehouse.stock() + ". it should be 9.");
            inventory.read(1);
            System.out.println("  after inventory reads the topic: " + warehouse.stock() + ".");
            System.out.println("  for a moment the two disagree. the system is eventually consistent, not consistent at every instant.");
        }
    }

    private static void six(Broker broker, String topic, String run) throws Exception {
        System.out.println("SIX. The bill.");
        broker.createTopic(topic);
        Warehouse plain = new Warehouse(10);
        Warehouse careful = new Warehouse(10);
        try (OrderService orders = new OrderService(topic);
             Reader plainReader = new Reader("plain-" + run, topic, true, false, plain::reserve);
             Reader carefulReader = new Reader("careful-" + run, topic, true, true, careful::reserve)) {
            orders.place("ORD-1");
            plainReader.read(1);
            carefulReader.read(1);
            plainReader.goBackTo(0);
            carefulReader.goBackTo(0);
            plainReader.read(1);
            carefulReader.read(1);
        }
        System.out.println("  the same event delivered twice, as Kafka may after a missed commit. stock: without a duplicate check " + plain.stock() + ", with one " + careful.stock() + ". it should be 9.");
        System.out.println("  and the flow of an order is now spread over several services, each reading the topic: to see it, you read the topic, not one piece of code.");
        System.out.println("  and a broker is another system to run: this demo needed 1 container for 1 topic.");
    }
}
