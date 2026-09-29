package com.jk.explore.processmanager;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * The services an order passes through. Each does one job and answers with an event.
 */
public final class Services {

    public static final class Warehouse {
        private final String name;
        private final Map<String, Integer> stock;

        public Warehouse(String name, Map<String, Integer> stock) {
            this.name = name;
            this.stock = new HashMap<>(stock);
        }

        public String reserve(String sku) {
            int have = stock.getOrDefault(sku, 0);
            if (have == 0) {
                return "OUT_OF_STOCK";
            }
            stock.put(sku, have - 1);
            return "RESERVED";
        }

        public void release(String sku) {
            stock.merge(sku, 1, Integer::sum);
        }

        public int stock(String sku) {
            return stock.getOrDefault(sku, 0);
        }

        public String name() {
            return name;
        }
    }

    public static final class Payments {
        private final Set<String> declinedCards;

        public Payments(Set<String> declinedCards) {
            this.declinedCards = declinedCards;
        }

        public String charge(String card) {
            return declinedCards.contains(card) ? "DECLINED" : "PAID";
        }
    }

    public static final class Shipping {
        public String ship(String orderId) {
            return "SHIPPED";
        }
    }

    public static final class Emails {
        private final List<String> sent = new ArrayList<>();

        public void send(String text) {
            sent.add(text);
        }

        public List<String> sent() {
            return sent;
        }
    }

    private Services() {
    }
}
