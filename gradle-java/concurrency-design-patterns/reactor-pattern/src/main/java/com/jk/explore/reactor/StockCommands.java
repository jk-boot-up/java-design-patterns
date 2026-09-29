package com.jk.explore.reactor;

import java.util.Map;

/**
 * What the stock server answers: a word and a product code in, one line out.
 */
public final class StockCommands {

    static final Map<String, Integer> STOCK = Map.of("KETTLE-1", 4, "MUG-1", 20);
    static final Map<String, Integer> PRICE = Map.of("KETTLE-1", 3000, "MUG-1", 800);

    public static String answer(String line) {
        String[] parts = line.trim().split(" ");
        return switch (parts[0]) {
            case "stock" -> String.valueOf(STOCK.getOrDefault(parts[1], 0));
            case "price" -> String.valueOf(PRICE.getOrDefault(parts[1], 0));
            case "report" -> slowReport();
            default -> "unknown command";
        };
    }

    /** A handler that takes 300 ms, as if it added up a day of sales. */
    static String slowReport() {
        try {
            Thread.sleep(300);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        return "report ready";
    }

    private StockCommands() {
    }
}
