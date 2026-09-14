package com.jk.explore.databaseperservice;

/**
 * One line of one order, as the Orders service stores it.
 *
 * Look at what it holds and, more importantly, what it does not. There is a
 * {@code sku} but no product name, because the product name is not the Orders
 * service's to know. Once the two services stop sharing a database, that missing
 * field is the whole story of this project: somebody now has to go and ask for it.
 */
public record Order(String orderId, String customerId, String sku, int quantity) {
}
