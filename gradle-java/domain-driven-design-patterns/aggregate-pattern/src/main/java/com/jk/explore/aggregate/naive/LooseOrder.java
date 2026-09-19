package com.jk.explore.aggregate.naive;

import java.util.ArrayList;
import java.util.List;

/** An order with public fields and a public list, so anyone can do anything to it. */
public class LooseOrder {

    public static class Line {
        public String sku;
        public long unitPence;
        public int quantity;

        public Line(String sku, long unitPence, int quantity) {
            this.sku = sku;
            this.unitPence = unitPence;
            this.quantity = quantity;
        }
    }

    public final List<Line> lines = new ArrayList<>();
    public boolean placed;

    public long totalPence() {
        return lines.stream().mapToLong(l -> l.unitPence * l.quantity).sum();
    }
}
