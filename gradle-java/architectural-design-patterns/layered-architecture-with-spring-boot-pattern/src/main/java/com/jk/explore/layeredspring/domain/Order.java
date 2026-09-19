package com.jk.explore.layeredspring.domain;

/** An order as the shop keeps it. {@code costPence} is what the shop paid, and no customer should ever see it. */
public record Order(String id, String customer, String sku, int quantity, long totalPence, long costPence, String status) {
}
