package com.jk.explore.contextmap.sales;

import com.jk.explore.contextmap.catalog.Catalog;
import com.jk.explore.contextmap.kernel.Address;
import com.jk.explore.contextmap.kernel.Money;

/**
 * The sales context: takes orders. It uses the catalogue's prices and the shared kernel's Address and Money.
 */
public final class Sales {

    public record Order(String id, Address deliverTo, Money total) {
    }

    public static Order placeOrder(String id, Address deliverTo, String... skus) {
        Money total = new Money(0);
        for (String sku : skus) {
            total = total.plus(Catalog.price(sku));
        }
        return new Order(id, deliverTo, total);
    }

    private Sales() {
    }
}
