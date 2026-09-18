package com.jk.explore.mvc.naive;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * The first naive version: no model, no view, no controller. One class
 * checks stock, takes the money, and formats the screen text, all in the
 * same method.
 *
 * <p>It has a property worth noticing before dismissing it: the screen text
 * and the (equally inline) email text, if this class grew a second output,
 * would trivially agree, because there is only one method and one set of
 * local variables computing the total. The problem this version has is a
 * different one from the shortcut further down — you cannot render the
 * screen without also running the checkout, so testing "does the summary
 * look right" means constructing stock, a card network and an order store
 * every time.
 */
public class EverythingOrderScreen {

    private final Map<String, Long> priceInPence = new LinkedHashMap<>();
    private final Map<String, Integer> stock = new LinkedHashMap<>();
    private int nextOrderNumber = 1001;

    public EverythingOrderScreen() {
        priceInPence.put("ESP-001", 24900L);
        stock.put("ESP-001", 4);
        priceInPence.put("GRD-014", 8950L);
        stock.put("GRD-014", 2);
        priceInPence.put("BNS-220", 2200L);
        stock.put("BNS-220", 40);
    }

    public String checkout(Map<String, Integer> wanted) {
        long total = 0;
        List<String> lines = new ArrayList<>();
        for (Map.Entry<String, Integer> line : wanted.entrySet()) {
            Long price = priceInPence.get(line.getKey());
            if (price == null) {
                return "Sorry — no such product: " + line.getKey() + ".";
            }
            int available = stock.getOrDefault(line.getKey(), 0);
            if (available < line.getValue()) {
                return "Sorry — only " + available + " of " + line.getKey() + " left.";
            }
            long lineTotal = price * line.getValue();
            total += lineTotal;
            lines.add("  " + line.getValue() + " x " + line.getKey() + "  "
                    + formatted(lineTotal));
        }

        for (Map.Entry<String, Integer> line : wanted.entrySet()) {
            stock.put(line.getKey(), stock.get(line.getKey()) - line.getValue());
        }
        String orderId = "ord-" + nextOrderNumber++;

        StringBuilder out = new StringBuilder();
        out.append("Order ").append(orderId).append(" placed.\n");
        for (String line : lines) {
            out.append(line).append("\n");
        }
        out.append("  Total: ").append(formatted(total));
        return out.toString();
    }

    private static String formatted(long pence) {
        return String.format("£%d.%02d", pence / 100, pence % 100);
    }
}
