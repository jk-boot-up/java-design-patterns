package com.jk.explore.dto.domain;

import java.util.AbstractList;
import java.util.ArrayList;
import java.util.List;

/**
 * A customer's order history, loaded the first time anything touches it.
 * A serialiser that walks every field touches it.
 */
public class LazyOrders extends AbstractList<Order> {

    public static final int ORDERS_PER_CUSTOMER = 25;

    private List<Order> loaded;
    private int loadCount;

    private List<Order> load() {
        if (loaded == null) {
            loadCount++;
            loaded = new ArrayList<>();
            for (int i = 1; i <= ORDERS_PER_CUSTOMER; i++) {
                loaded.add(new Order(i, 4_500 + i, List.of(
                        new OrderLine("Keyboard", 1, 2_500),
                        new OrderLine("Mouse", 1, 1_200),
                        new OrderLine("Cable", 2, 400))));
            }
        }
        return loaded;
    }

    @Override
    public Order get(int index) {
        return load().get(index);
    }

    @Override
    public int size() {
        return load().size();
    }

    /** How many times the history was actually loaded from storage. */
    public int loadCount() {
        return loadCount;
    }
}
