package com.jk.explore.roleobject;

import java.util.ArrayList;
import java.util.List;

/**
 * The roles an account can play. Each holds its own data and its own behaviour.
 */
public final class Roles {

    /** Buys things. Holds the account's order history. */
    public static final class Buyer extends Role {
        private final List<String> orders = new ArrayList<>();

        public Buyer(Account account) {
            super(account);
        }

        public void placeOrder(String orderId) {
            orders.add(orderId);
        }

        public List<String> orders() {
            return orders;
        }
    }

    /** Sells on the marketplace under a shop name. */
    public static final class Seller extends Role {
        private final String shopName;
        private final List<String> listings = new ArrayList<>();

        public Seller(Account account, String shopName) {
            super(account);
            this.shopName = shopName;
        }

        public String list(String product) {
            listings.add(product);
            return shopName + " lists " + product;
        }

        public List<String> listings() {
            return listings;
        }
    }

    /** Earns a commission, in percent, on orders it refers. */
    public static final class Affiliate extends Role {
        private final int percent;
        private long earnedPence;

        public Affiliate(Account account, int percent) {
            super(account);
            this.percent = percent;
        }

        public void referred(long orderPence) {
            earnedPence += orderPence * percent / 100;
        }

        public long earnedPence() {
            return earnedPence;
        }
    }

    private Roles() {
    }
}
