package com.jk.explore.apigateway;

/** What the Catalog service owns: the words on a product page, and nothing else. */
public record Product(String sku, String name, String description) {

    @Override
    public String toString() {
        return name;
    }
}
