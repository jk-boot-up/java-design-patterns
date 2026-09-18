package com.jk.explore.layered.naive;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * The first naive version: no layers at all.
 *
 * <p>One class validates the request, keeps the catalogue, does the
 * arithmetic, takes the money, stores the order and writes the email. Nothing
 * here is badly written. Every line is clear, the method reads in order, and a
 * new joiner could follow it. That is exactly why this shape survives in real
 * codebases for years.
 *
 * <p>It has one property that no amount of tidying fixes: <strong>you cannot
 * test the arithmetic without the storage.</strong> To assert that three lines
 * come to £382.50 you must construct this class, which means constructing its
 * catalogue map, its order map and its list of sent email, because they are
 * fields of the same object. The total and the map are welded together. There
 * is no seam.
 *
 * <p>The second thing, which is easier to feel than to argue: read it and count
 * the different kinds of thinking on the screen at once. Pence arithmetic. A
 * card. An email address. A map. Four subjects in one place is what "hard to
 * read" actually means, and layering is the first and cheapest answer to it.
 */
public class EverythingOrderService {

    private final Map<String, Long> priceInPence = new LinkedHashMap<>();
    private final Map<String, Integer> stock = new LinkedHashMap<>();
    private final Map<String, String> orders = new LinkedHashMap<>();
    private final List<String> sentEmail = new ArrayList<>();
    private int nextOrderNumber = 1001;

    public EverythingOrderService() {
        priceInPence.put("ESP-001", 24900L);
        stock.put("ESP-001", 4);
        priceInPence.put("GRD-014", 8950L);
        stock.put("GRD-014", 2);
        priceInPence.put("BNS-220", 2200L);
        stock.put("BNS-220", 40);
    }

    public String checkout(String customerId, String customerEmail, Map<String, Integer> wanted) {
        long total = 0;
        for (Map.Entry<String, Integer> line : wanted.entrySet()) {
            Long price = priceInPence.get(line.getKey());
            if (price == null) {
                return "Sorry — no such product: " + line.getKey() + ".";
            }
            int available = stock.getOrDefault(line.getKey(), 0);
            if (available < line.getValue()) {
                return "Sorry — only " + available + " of " + line.getKey() + " left.";
            }
            total += price * line.getValue();
        }

        for (Map.Entry<String, Integer> line : wanted.entrySet()) {
            stock.put(line.getKey(), stock.get(line.getKey()) - line.getValue());
        }
        String orderId = "ord-" + nextOrderNumber++;
        orders.put(orderId, customerId + ":" + total);
        String money = String.format("£%d.%02d", total / 100, total % 100);
        sentEmail.add(customerEmail + ": Thank you. Your order " + orderId
                + " for " + money + " is confirmed.");
        return "Order " + orderId + " placed. Total " + money + ".";
    }

    public int stockOf(String sku) {
        return stock.getOrDefault(sku, 0);
    }

    public int ordersStored() {
        return orders.size();
    }

    public List<String> sentEmail() {
        return List.copyOf(sentEmail);
    }
}
