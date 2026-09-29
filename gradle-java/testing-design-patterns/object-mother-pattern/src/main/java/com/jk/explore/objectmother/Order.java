package com.jk.explore.objectmother;

import java.util.List;

/**
 * An order, with everything the constructor insists on.
 */
public record Order(Customer customer, String country, List<Line> lines, boolean giftWrap) {

    public double total() {
        return lines.stream().mapToDouble(Line::total).sum();
    }
}
