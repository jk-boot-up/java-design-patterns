package com.jk.explore.apigateway;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.NoSuchElementException;

/**
 * The Catalog service: product names and descriptions.
 *
 * Read-heavy, rarely changes, and owns nothing else. It has no idea what
 * anything costs.
 */
public final class CatalogService {

    private final Map<String, Product> products = new LinkedHashMap<>();

    public CatalogService() {
        products.put("SKU-1234", new Product("SKU-1234", "Barista Pro Espresso Machine",
                "Fifteen bar pump, steam wand, two year guarantee."));
        products.put("SKU-2001", new Product("SKU-2001", "Rwandan Single Origin Beans",
                "One kilogram, whole bean, roasted in Bermondsey."));
        products.put("SKU-2002", new Product("SKU-2002", "Stainless Milk Jug",
                "Six hundred millilitres, for steaming."));
    }

    public Product product(String sku) {
        Product product = products.get(sku);
        if (product == null) {
            throw new NoSuchElementException("no such product: " + sku);
        }
        return product;
    }
}
