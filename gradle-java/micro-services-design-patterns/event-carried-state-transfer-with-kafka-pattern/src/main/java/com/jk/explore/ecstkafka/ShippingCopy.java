package com.jk.explore.ecstkafka;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import org.apache.kafka.clients.consumer.ConsumerRecord;

/**
 * The pattern: shipping's own copy of customer addresses, built only from the events on the topic.
 * An event with no value, a tombstone, removes the customer.
 */
public final class ShippingCopy {

    private final Map<String, String> addresses = new LinkedHashMap<>();

    public void apply(List<ConsumerRecord<String, String>> events) {
        for (ConsumerRecord<String, String> e : events) {
            if (e.value() == null) {
                addresses.remove(e.key());
            } else {
                addresses.put(e.key(), e.value());
            }
        }
    }

    public String label(String order, String customer) {
        String a = addresses.get(customer);
        return a == null ? null : order + " -> " + a;
    }

    public int size() {
        return addresses.size();
    }
}
