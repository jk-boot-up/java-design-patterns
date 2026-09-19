package com.jk.explore.hexagonalspring.adapter.memory;

import com.jk.explore.hexagonalspring.core.port.Warehouse;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.Map;

@Component
@ConditionalOnProperty(name = "orders.store", havingValue = "memory", matchIfMissing = true)
public class InMemoryWarehouse implements Warehouse {

    private final Map<String, Integer> stock = new HashMap<>(Map.of("ESP-001", 5, "BNS-220", 10));
    private final Map<String, Long> prices = Map.of("ESP-001", 30000L, "BNS-220", 1250L);

    public InMemoryWarehouse() {
    }

    /** For tests that need plenty of stock. */
    public InMemoryWarehouse(int stockOfEach) {
        stock.replaceAll((sku, n) -> stockOfEach);
    }

    @Override
    public long priceOf(String sku) {
        return prices.getOrDefault(sku, 0L);
    }

    @Override
    public synchronized boolean reserve(String sku, int quantity) {
        int left = stock.getOrDefault(sku, 0);
        if (left < quantity) {
            return false;
        }
        stock.put(sku, left - quantity);
        return true;
    }

    @Override
    public synchronized int stockOf(String sku) {
        return stock.getOrDefault(sku, 0);
    }
}
