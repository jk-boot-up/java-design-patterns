package com.jk.explore.lazyload.pattern;

import com.jk.explore.lazyload.domain.Shop;
import com.jk.explore.lazyload.toydb.Row;

/** <strong>Variant one: lazy initialisation.</strong> The field is empty until asked. */
public class LazyInitOrder {

    private final Session session;
    private final int customerId;
    private String customerName;

    public LazyInitOrder(Session session, int customerId) {
        this.session = session;
        this.customerId = customerId;
    }

    public String customerName() {
        if (customerName == null) {
            Row row = session.select(Shop.CUSTOMERS, customerId);
            customerName = row.text("name");
        }
        return customerName;
    }
}
