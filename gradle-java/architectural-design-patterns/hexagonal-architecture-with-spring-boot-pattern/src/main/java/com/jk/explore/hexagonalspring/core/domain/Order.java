package com.jk.explore.hexagonalspring.core.domain;

public record Order(String id, String customer, String sku, int quantity, long totalPence) {
}
