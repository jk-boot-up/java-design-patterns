package com.jk.explore.externalisedconfig;

/**
 * A customer's basket at the moment they reach the delivery step.
 *
 * <p>Only two facts matter for this project: which order it will become, and
 * what the goods come to before delivery is added. Everything else a real
 * basket carries — the lines, the customer, the address — would be noise here.
 *
 * @param orderId the reference the customer will quote if they ring up
 * @param goodsTotal what the items come to, before delivery
 */
public record Basket(String orderId, Money goodsTotal) {
}
