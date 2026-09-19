package com.jk.explore.transactionscript.script;

import com.jk.explore.transactionscript.Db;

/**
 * A second script, written later, that also has to price a quantity. It copied the pricing from the
 * first one, and when the bulk discount changed, only one of them was told.
 */
public class AmendOrderScript {

    private final Db db;

    public AmendOrderScript(Db db) {
        this.db = db;
    }

    public long run(String orderId, String sku, int newQuantity) {
        long unit = sku.startsWith("ESP") ? 30000 : 800;
        long total = unit * newQuantity;
        if (newQuantity >= 10) {
            total = total - total / 10;
        }
        db.update(orderId, total);
        return total;
    }
}
