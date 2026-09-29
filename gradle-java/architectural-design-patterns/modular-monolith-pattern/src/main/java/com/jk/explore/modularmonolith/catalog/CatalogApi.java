package com.jk.explore.modularmonolith.catalog;

import com.jk.explore.modularmonolith.catalog.internal.CatalogModule;

/**
 * The catalogue module's front door: the only way other modules may touch stock.
 */
public interface CatalogApi {

    /** Takes {@code qty} out of stock, or refuses if there are not enough. */
    boolean reserve(String sku, int qty);

    int stock(String sku);

    static CatalogApi create() {
        return new CatalogModule();
    }
}
