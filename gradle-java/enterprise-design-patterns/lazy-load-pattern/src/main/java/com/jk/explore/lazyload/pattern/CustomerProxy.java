package com.jk.explore.lazyload.pattern;

import com.jk.explore.lazyload.domain.Shop;

/** <strong>Variant two: virtual proxy.</strong> It stands in for the customer and loads the real one on first use. */
public class CustomerProxy implements CustomerRef {

    private final Session session;
    private final int id;
    private String name;

    public CustomerProxy(Session session, int id) {
        this.session = session;
        this.id = id;
    }

    @Override
    public String name() {
        if (name == null) {
            name = session.select(Shop.CUSTOMERS, id).text("name");
        }
        return name;
    }
}
