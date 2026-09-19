package com.jk.explore.transactionscript.script;

import com.jk.explore.transactionscript.Db;

/** A script at its best: a job with one purpose, read once, changed rarely. */
public final class MonthEndScript {

    private MonthEndScript() {
    }

    public static String run(Db db) {
        long total = 0;
        for (Db.SavedOrder order : db.orders()) {
            total += order.totalPence();
        }
        return db.orders().size() + " orders, " + String.format("£%d.%02d", total / 100, total % 100) + " taken";
    }
}
