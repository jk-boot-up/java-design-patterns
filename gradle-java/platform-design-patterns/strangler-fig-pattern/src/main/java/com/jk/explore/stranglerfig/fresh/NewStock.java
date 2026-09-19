package com.jk.explore.stranglerfig.fresh;

import com.jk.explore.stranglerfig.domain.Line;
import com.jk.explore.stranglerfig.domain.Order;
import com.jk.explore.stranglerfig.domain.StockKeeper;

import java.util.HashMap;
import java.util.Map;

/** The rewritten stock service, with <em>its own</em> stock table. Two tables now claim to be the truth. */
public class NewStock implements StockKeeper {

    private final Map<String, Integer> stock = new HashMap<>();

    public NewStock(Map<String, Integer> openingStock) {
        stock.putAll(openingStock);
    }

    @Override
    public boolean reserve(Order order) {
        for (Line line : order.lines()) {
            if (stock.getOrDefault(line.sku(), 0) < line.quantity()) {
                return false;
            }
        }
        order.lines().forEach(l -> stock.merge(l.sku(), -l.quantity(), Integer::sum));
        return true;
    }

    @Override
    public int onHand(String sku) {
        return stock.getOrDefault(sku, 0);
    }
}
