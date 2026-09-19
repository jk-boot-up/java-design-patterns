package com.jk.explore.onion.naive;

import com.jk.explore.onion.infrastructure.SqlDatabase;

/** Meant to be the core, but it reaches out to the database itself. */
public class NaiveOrder {

    private final SqlDatabase db;
    private final long subtotalCents;

    public NaiveOrder(SqlDatabase db, long subtotalCents) {
        this.db = db;
        this.subtotalCents = subtotalCents;
    }

    public void save() {
        db.execute("insert into orders values (" + subtotalCents + ")");
    }
}
