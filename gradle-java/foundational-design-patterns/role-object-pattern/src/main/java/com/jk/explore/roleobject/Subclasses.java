package com.jk.explore.roleobject;

import java.util.ArrayList;
import java.util.List;

/**
 * Without the pattern: one subclass per kind of customer, fixed when the object is made.
 */
public final class Subclasses {

    public static class Customer {
        private final String name;
        private final List<String> orders = new ArrayList<>();

        public Customer(String name) {
            this.name = name;
        }

        public void placeOrder(String orderId) {
            orders.add(orderId);
        }

        public List<String> orders() {
            return orders;
        }

        public String name() {
            return name;
        }
    }

    /** A customer who sells. Becoming one means making a new object. */
    public static class SellingCustomer extends Customer {
        private final String shopName;

        public SellingCustomer(String name, String shopName) {
            super(name);
            this.shopName = shopName;
        }

        public String shopName() {
            return shopName;
        }
    }

    /** With three kinds (buyer, seller, affiliate), every mix needs its own class: 2^3 - 1 of them. */
    public static int classesNeeded(int kinds) {
        return (1 << kinds) - 1;
    }

    private Subclasses() {
    }
}
