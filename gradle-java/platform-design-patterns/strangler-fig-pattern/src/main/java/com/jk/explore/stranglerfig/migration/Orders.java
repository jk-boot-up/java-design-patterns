package com.jk.explore.stranglerfig.migration;

import com.jk.explore.stranglerfig.domain.Line;
import com.jk.explore.stranglerfig.domain.Order;

import java.util.ArrayList;
import java.util.List;

/** A repeatable stream of orders from a fixed-seed generator, so every run sees the same shop. */
public final class Orders {

    private Orders() {
    }

    public static List<Order> generate(int count) {
        List<Order> orders = new ArrayList<>();
        long seed = 42;
        for (int id = 1; id <= count; id++) {
            List<Line> lines = new ArrayList<>();
            int lineCount = 1 + (int) ((seed = next(seed)) % 3);
            for (int l = 0; l < lineCount; l++) {
                int quantity = 1 + (int) ((seed = next(seed)) % 3);
                long unit = 199 + (seed = next(seed)) % 1_800;
                lines.add(new Line("SKU-" + (1 + (seed = next(seed)) % 4), quantity, unit));
            }
            orders.add(new Order(id, List.copyOf(lines)));
        }
        return orders;
    }

    /** The order that costs exactly fifty pounds in goods, where the two systems disagree about delivery. */
    public static Order exactlyFiftyPounds(int id) {
        return new Order(id, List.of(new Line("SKU-1", 1, 5_000)));
    }

    private static long next(long seed) {
        return (seed * 1_103_515_245L + 12_345L) & 0x7fffffffL;
    }
}
