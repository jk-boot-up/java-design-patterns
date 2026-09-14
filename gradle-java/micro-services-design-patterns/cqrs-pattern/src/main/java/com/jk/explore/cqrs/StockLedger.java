package com.jk.explore.cqrs;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * The write side's count of what is actually on the shelf.
 *
 * This class is the reason the whole project exists in the shape it does. The count here
 * is the truth, it is checked and decremented in the same breath, and two shoppers
 * reaching for the last kettle cannot both succeed. It is not fast, it is not
 * denormalised, and it is not a copy.
 *
 * <p>A read model may show a stock number, and often should — "only 2 left" sells
 * kettles. It must never be the number a sale is decided against, because it is by
 * design a moment out of date, and a moment is all it takes to sell the same kettle
 * twice. That distinction is the single most useful thing to take away from CQRS.
 */
public final class StockLedger {

    private final Map<String, Integer> onShelf = new LinkedHashMap<>();
    private final EventBus events;

    public StockLedger(EventBus events) {
        this.events = events;
    }

    public void stock(String sku, int quantity) {
        onShelf.put(sku, quantity);
        events.publish(new ShopEvent.StockChanged(sku, quantity));
    }

    public int available(String sku) {
        return onShelf.getOrDefault(sku, 0);
    }

    /**
     * Takes stock off the shelf, or refuses.
     *
     * @throws OutOfStockException if there is not enough, which is the whole point
     */
    public void reserve(String sku, int quantity) {
        int left = available(sku);
        if (left < quantity) {
            throw new OutOfStockException(sku, quantity, left);
        }
        onShelf.put(sku, left - quantity);
        events.publish(new ShopEvent.StockChanged(sku, left - quantity));
    }
}
