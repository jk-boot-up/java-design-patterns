package com.jk.explore.tdgjdbc;

/**
 * One row of the product table, as plain data. Spring's DataClassRowMapper fills it by column name.
 */
public record Row(String sku, String name, int pence, int quantity) {
}
