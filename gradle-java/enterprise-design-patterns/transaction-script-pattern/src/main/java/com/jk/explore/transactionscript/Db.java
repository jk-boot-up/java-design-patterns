package com.jk.explore.transactionscript;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Supplier;

/** A very small database: stock counts and saved orders, with one transaction at a time that can roll back. */
public class Db {

    public record SavedOrder(String id, String customer, long totalPence) {
    }

    private Map<String, Integer> stock = new HashMap<>(Map.of("MUG-BLUE", 10, "ESP-001", 3));
    private List<SavedOrder> orders = new ArrayList<>();

    public int stockOf(String sku) {
        return stock.getOrDefault(sku, 0);
    }

    public void setStock(String sku, int quantity) {
        stock.put(sku, quantity);
    }

    public List<SavedOrder> orders() {
        return List.copyOf(orders);
    }

    public void save(SavedOrder order) {
        orders.add(order);
    }

    public void update(String orderId, long newTotal) {
        for (int i = 0; i < orders.size(); i++) {
            if (orders.get(i).id().equals(orderId)) {
                SavedOrder o = orders.get(i);
                orders.set(i, new SavedOrder(o.id(), o.customer(), newTotal));
            }
        }
    }

    /** Runs the work as one transaction: if it throws, every change it made is undone. */
    public <T> T transaction(Supplier<T> work) {
        Map<String, Integer> stockBefore = new HashMap<>(stock);
        List<SavedOrder> ordersBefore = new ArrayList<>(orders);
        try {
            return work.get();
        } catch (RuntimeException e) {
            stock = stockBefore;
            orders = ordersBefore;
            throw e;
        }
    }
}
