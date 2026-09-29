package com.jk.explore.messagefilter;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;

/**
 * Receivers that only care about some orders: gift wrapping and loyalty bonuses.
 */
public final class Services {

    /** Records everything it is handed, and what it acted on. */
    public static final class Receiver implements Consumer<OrderEvent> {
        private final List<String> received = new ArrayList<>();

        public void accept(OrderEvent e) {
            received.add(e.orderId());
        }

        public List<String> received() {
            return received;
        }
    }

    /** Without the pattern: the gift-wrap service is handed every order and must check each one itself. */
    public static final class GiftWrapUnfiltered implements Consumer<OrderEvent> {
        private int handed;
        private final List<String> wrapped = new ArrayList<>();

        public void accept(OrderEvent e) {
            handed++;
            if (e.gift()) {
                wrapped.add(e.orderId());
            }
        }

        public int handed() {
            return handed;
        }

        public List<String> wrapped() {
            return wrapped;
        }
    }

    private Services() {
    }
}
