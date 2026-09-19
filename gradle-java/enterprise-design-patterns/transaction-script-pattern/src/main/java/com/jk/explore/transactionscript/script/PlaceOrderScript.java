package com.jk.explore.transactionscript.script;

import com.jk.explore.transactionscript.Db;

/**
 * Placing an order as one procedure, top to bottom. This is a transaction script: one request, one
 * method, one transaction. No order object, no rules class. The steps are the design.
 */
public class PlaceOrderScript {

    private static final long UNIT_PENCE_MUG = 800;
    private static final long UNIT_PENCE_MACHINE = 30000;

    private final Db db;
    private final Payment payment;
    private int sequence;

    public PlaceOrderScript(Db db, Payment payment) {
        this.db = db;
        this.payment = payment;
    }

    public Db.SavedOrder run(String customer, String sku, int quantity) {
        return db.transaction(() -> {
            if (quantity < 1) {
                throw new IllegalArgumentException("quantity must be at least 1");
            }
            if (db.stockOf(sku) < quantity) {
                throw new IllegalStateException("not enough " + sku + " in stock");
            }
            db.setStock(sku, db.stockOf(sku) - quantity);
            long unit = sku.startsWith("ESP") ? UNIT_PENCE_MACHINE : UNIT_PENCE_MUG;
            long total = unit * quantity;
            if (quantity >= 5) {
                total = total - total / 10;
            }
            payment.charge(total);
            Db.SavedOrder order = new Db.SavedOrder("ORD-" + (++sequence), customer, total);
            db.save(order);
            return order;
        });
    }
}
