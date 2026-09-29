package com.jk.explore.tabledatagateway;

/**
 * The same three callers, now asking the gateway. None of them contains SQL.
 */
public final class Pages {

    public static String productPage(ProductGateway g, String sku) {
        return g.findBySku(sku).map(r -> r.name() + ", " + r.stock() + " in stock").orElse("no such product");
    }

    public static int stockReport(ProductGateway g) {
        return g.countOutOfStock();
    }

    public static void checkout(ProductGateway g, String sku, int qty) {
        g.takeStock(sku, qty);
    }

    private Pages() {
    }
}
