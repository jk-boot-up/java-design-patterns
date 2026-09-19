package com.jk.explore.specification.naive;

import com.jk.explore.specification.domain.Product;

/**
 * The same idea, "cheap and available", written out where each feature needs it. Three features, three
 * copies. The search page and the shipping offer say under ten pounds. The promotion, written last, says
 * ten pounds or less, and forgets discontinued products.
 */
public final class NaiveShop {

    private NaiveShop() {
    }

    public static boolean showOnSearchPage(Product p) {
        return p.inStock() && p.pricePence() < 1000 && !p.discontinued();
    }

    public static boolean eligibleForPromotion(Product p) {
        return p.inStock() && p.pricePence() <= 1000;
    }

    public static boolean qualifiesForFreeShipping(Product p) {
        return p.inStock() && p.pricePence() < 1000 && !p.discontinued();
    }
}
