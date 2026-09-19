package com.jk.explore.lazyload.pattern;

import com.jk.explore.lazyload.domain.Shop;
import com.jk.explore.lazyload.toydb.Row;

/** <strong>Variant four: ghost.</strong> Created with only its id; the first access to anything loads all of it. */
public class GhostCustomer implements CustomerRef {

    private final Session session;
    private final int id;
    private boolean loaded;
    private String name;

    public GhostCustomer(Session session, int id) {
        this.session = session;
        this.id = id;
    }

    public int id() {
        return id;
    }

    @Override
    public String name() {
        if (!loaded) {
            Row row = session.select(Shop.CUSTOMERS, id);
            name = row.text("name");
            loaded = true;
        }
        return name;
    }
}
