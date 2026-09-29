package com.jk.explore.modularmonolith.mud;

/**
 * Checkout in the big ball of mud: writes straight into the stock and payment tables.
 */
public final class MudCheckout {

    public static String placeOrder(String orderId, String sku, int qty, long pence) {
        Tables.STOCK.merge(sku, -qty, Integer::sum);
        Tables.PAYMENTS.put(orderId, pence);
        return orderId + " placed";
    }

    private MudCheckout() {
    }
}
