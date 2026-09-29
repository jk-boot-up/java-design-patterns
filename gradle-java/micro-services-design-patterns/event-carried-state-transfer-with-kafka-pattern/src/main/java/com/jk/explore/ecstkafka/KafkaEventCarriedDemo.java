package com.jk.explore.ecstkafka;

import java.util.ArrayList;
import java.util.List;
import org.apache.kafka.clients.consumer.ConsumerRecord;

/**
 * The five acts, against a real Kafka broker started and stopped by this program.
 */
public final class KafkaEventCarriedDemo {

    static final int ORDERS = 100;

    public static void main(String[] args) throws Exception {
        if (!Kafka.containerRuntimeAvailable()) {
            System.out.println(Kafka.NO_RUNTIME_ADVICE);
            return;
        }
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();
        try (Kafka kafka = new Kafka()) {
            try {
                kafka.start();
            } catch (RuntimeException e) {
                out.add(Kafka.WOULD_NOT_START_ADVICE);
                return out;
            }
            CustomerService customers = new CustomerService();

            out.add("ONE. Thin events on Kafka, and a call back for every label.");
            kafka.createTopic("customer-changed", 1, false);
            for (int c = 1; c <= 10; c++) {
                customers.move("C" + c, c + " High Street, Leeds");
                kafka.send("customer-changed", "C" + c, "changed");
            }
            List<ConsumerRecord<String, String>> thin = kafka.readAll("customer-changed", List.of(0));
            out.add("  shipping read " + thin.size() + " events saying only \"changed\"");
            out.add("  " + ORDERS + " labels: " + printedByCalling(customers) + " printed, " + customers.lookups()
                    + " calls to the customer service");
            customers.setUp(false);
            out.add("  customer service down: " + printedByCalling(customers) + " of " + ORDERS + " printed");

            out.add("");
            out.add("TWO. Events carry the address, on a compacted topic keyed by customer.");
            kafka.createTopic("customer-addresses", 3, true);
            for (int c = 1; c <= 10; c++) {
                kafka.send("customer-addresses", "C" + c, c + " High Street, Leeds");
            }
            ShippingCopy shipping = new ShippingCopy();
            shipping.apply(kafka.readAll("customer-addresses", List.of(0, 1, 2)));
            out.add("  shipping's own copy holds " + shipping.size() + " addresses");
            out.add("  customer service still down: " + printed(shipping) + " of " + ORDERS + " labels printed, 0 calls");

            out.add("");
            out.add("THREE. A new shipping instance starts from nothing.");
            kafka.send("customer-addresses", "C1", "9 Mill Lane, York");
            ShippingCopy fresh = new ShippingCopy();
            List<ConsumerRecord<String, String>> history = kafka.readAll("customer-addresses", List.of(0, 1, 2));
            fresh.apply(history);
            out.add("  it reads the topic from the beginning: " + history.size() + " events, " + fresh.size() + " customers");
            out.add("  C1's label: " + fresh.label("ORD-1", "C1") + " (the latest event for C1 wins)");
            out.add("  the old copy, not yet updated: " + shipping.label("ORD-1", "C1"));

            out.add("");
            out.add("FOUR. Order: Kafka keeps it only within a partition.");
            kafka.createTopic("moves-unkeyed", 2, false);
            kafka.sendToPartition("moves-unkeyed", 0, "C2", "1 Park Road, Hull");
            kafka.sendToPartition("moves-unkeyed", 1, "C2", "4 Quay Street, Bristol");
            ShippingCopy unkeyed = new ShippingCopy();
            unkeyed.apply(kafka.readAll("moves-unkeyed", List.of(1, 0)));
            out.add("  two moves on different partitions, read partition 1 first: " + unkeyed.label("ORD-2", "C2"));
            kafka.send("customer-addresses", "C2", "1 Park Road, Hull");
            kafka.send("customer-addresses", "C2", "4 Quay Street, Bristol");
            ShippingCopy keyed = new ShippingCopy();
            keyed.apply(kafka.readAll("customer-addresses", List.of(2, 1, 0)));
            out.add("  keyed by customer, so both on one partition, in order: " + keyed.label("ORD-2", "C2"));

            out.add("");
            out.add("FIVE. The bill: copies everywhere, and deleting is an event too.");
            kafka.send("customer-addresses", "C3", null);
            ShippingCopy afterDelete = new ShippingCopy();
            afterDelete.apply(kafka.readAll("customer-addresses", List.of(0, 1, 2)));
            out.add("  C3 closes the account: a tombstone (no value) is sent; the copy now holds " + afterDelete.size()
                    + " addresses; C3 now has no label: " + (afterDelete.label("ORD-3", "C3") == null));
            out.add("  every service holding a copy must read and honour it, or the address lives on");
            out.add("  and the topic, and every copy, is more data to store, secure and keep in step");
        }
        return out;
    }

    private static int printedByCalling(CustomerService customers) {
        int n = 0;
        for (int i = 0; i < ORDERS; i++) {
            try {
                if (customers.lookup("C" + (i % 10 + 1)) != null) {
                    n++;
                }
            } catch (IllegalStateException down) {
                // no label
            }
        }
        return n;
    }

    private static int printed(ShippingCopy copy) {
        int n = 0;
        for (int i = 0; i < ORDERS; i++) {
            if (copy.label("ORD-" + i, "C" + (i % 10 + 1)) != null) {
                n++;
            }
        }
        return n;
    }

    private KafkaEventCarriedDemo() {
    }
}
