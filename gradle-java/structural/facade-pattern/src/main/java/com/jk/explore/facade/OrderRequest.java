package com.jk.explore.facade;

public record OrderRequest(String customerId, String productId, int quantity, double amount,
                            String shippingAddress) {
}
