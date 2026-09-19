package com.jk.explore.nullobject.domain;

import java.util.Map;

/**
 * The truth about who has which discount. Four customers: 1 has a loyalty
 * discount, 3 has a staff discount, 2 and 4 have none. It returns
 * {@code null} for "none", which is the naive version's whole problem, and
 * throws when the service is down.
 */
public class DiscountDirectory {

    private final Map<Integer, Discount> discounts = Map.of(1, new LoyaltyDiscount(), 3, new StaffDiscount());
    private boolean down;

    public void goDown() {
        this.down = true;
    }

    public Discount find(int customerId) {
        if (down) {
            throw new DiscountServiceDown();
        }
        return discounts.get(customerId);
    }
}
