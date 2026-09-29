package com.jk.explore.authorization;

/**
 * One access question: may this user do this action to this order (for this amount, if it is a refund)?
 */
public record Request(User user, String action, Order order, double amount) {

    public static Request of(User user, String action, Order order) {
        return new Request(user, action, order, 0);
    }
}
