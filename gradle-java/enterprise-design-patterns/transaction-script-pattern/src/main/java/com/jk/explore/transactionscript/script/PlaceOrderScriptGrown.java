package com.jk.explore.transactionscript.script;

import com.jk.explore.transactionscript.Db;

/**
 * The same script a year later, after loyalty, region and coupon rules were added in the middle. It still
 * works. It also has more paths through it than anyone has tested.
 */
public class PlaceOrderScriptGrown {

    private final Db db;
    private final Payment payment;
    private int sequence;

    public PlaceOrderScriptGrown(Db db, Payment payment) {
        this.db = db;
        this.payment = payment;
    }

    public Db.SavedOrder run(String customer, String sku, int quantity, boolean loyal, String region, String coupon) {
        return db.transaction(() -> {
            if (quantity < 1) {
                throw new IllegalArgumentException("quantity must be at least 1");
            }
            if (db.stockOf(sku) < quantity) {
                throw new IllegalStateException("not enough " + sku + " in stock");
            }
            db.setStock(sku, db.stockOf(sku) - quantity);
            long total = Pricing.total(sku, quantity);
            if (loyal) {
                total = total - total / 20;
            }
            if (region.equals("EU")) {
                total = total + total / 5;
            }
            if (coupon != null && coupon.startsWith("SAVE")) {
                total = total - 500;
            }
            if (total < 0) {
                total = 0;
            }
            if (region.equals("EU") && quantity > 20) {
                throw new IllegalStateException("EU orders are limited to 20 items");
            }
            payment.charge(total);
            Db.SavedOrder order = new Db.SavedOrder("ORD-" + (++sequence), customer, total);
            db.save(order);
            return order;
        });
    }
}
