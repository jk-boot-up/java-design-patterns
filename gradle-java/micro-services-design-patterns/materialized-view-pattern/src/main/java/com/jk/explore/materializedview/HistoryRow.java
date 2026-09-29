package com.jk.explore.materializedview;

/**
 * One line of the "my orders" page: which order, what was bought, how many, and whether it has shipped.
 */
public record HistoryRow(String orderId, String product, int quantity, String status) {

    @Override
    public String toString() {
        return orderId + " " + quantity + " x " + product + " (" + status + ")";
    }
}
