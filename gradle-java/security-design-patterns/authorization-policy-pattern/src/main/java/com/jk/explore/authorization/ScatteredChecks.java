package com.jk.explore.authorization;

/**
 * Before: each endpoint writes its own access check, and one of them forgot to check ownership.
 */
public final class ScatteredChecks {

    public static boolean viewOrder(User user, Order order) {
        return true;   // "only signed-in users reach here anyway"
    }

    public static boolean cancelOrder(User user, Order order) {
        return user.name().equals(order.owner()) || user.role().equals("ADMIN");
    }

    public static boolean refund(User user, Order order, double amount) {
        return user.role().equals("SUPPORT") || user.role().equals("ADMIN");
    }

    private ScatteredChecks() {
    }
}
