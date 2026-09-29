package com.jk.explore.queryobject;

/**
 * One row of the product table.
 */
public record Product(String name, String category, long pricePence, int stock) {
}
