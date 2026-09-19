package com.jk.explore.unitofwork.domain;

public record OrderLine(int id, int orderId, int productId, int quantity) {
}
