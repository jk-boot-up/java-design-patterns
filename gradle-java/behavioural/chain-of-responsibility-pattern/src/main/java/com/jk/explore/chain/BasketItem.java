package com.jk.explore.chain;

/** One line of a checkout basket: what it is, what it costs, and how many. */
public record BasketItem(String sku, String description, int unitPricePounds, int quantity) {

    public int totalPounds() {
        return unitPricePounds * quantity;
    }

    @Override
    public String toString() {
        return String.format("%-6s %-22s %d x £%d = £%d",
                sku, description, quantity, unitPricePounds, totalPounds());
    }
}
