package com.jk.explore.publishersubscriber.naive;

import java.util.List;

/** The order service calling each interested service itself. Adding a fourth means changing this class. */
public class DirectOrderService {

    private final List<String> inventory;
    private final List<String> email;
    private final List<String> analytics;

    public DirectOrderService(List<String> inventory, List<String> email, List<String> analytics) {
        this.inventory = inventory;
        this.email = email;
        this.analytics = analytics;
    }

    public void place(String orderId) {
        inventory.add(orderId);
        email.add(orderId);
        analytics.add(orderId);
    }

    /** How many services this class has to know by name. */
    public static int servicesItKnows() {
        return 3;
    }
}
