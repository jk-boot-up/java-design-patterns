package com.jk.explore.domainservice;

import com.jk.explore.domainservice.Model.Basket;
import com.jk.explore.domainservice.Model.Coupon;
import com.jk.explore.domainservice.Model.Customer;
import com.jk.explore.domainservice.Model.Tier;

/**
 * Without the pattern: the pricing rule written inside each place that needs it.
 *
 * <p>The web checkout has the current rule: the gold discount and a coupon do
 * not add up; the bigger one wins. The phone app's copy is older and adds both.
 */
public final class Copies {

    public static long webCheckout(Customer c, Basket b, Coupon coupon) {
        long sub = b.subtotalPence();
        long gold = c.tier() == Tier.GOLD ? sub * 10 / 100 : 0;
        long off = coupon != null && sub > coupon.minimumPence() ? coupon.offPence() : 0;
        return sub - Math.max(gold, off);
    }

    public static long phoneApp(Customer c, Basket b, Coupon coupon) {
        long total = b.subtotalPence();
        if (c.tier() == Tier.GOLD) {
            total -= total * 10 / 100;
        }
        if (coupon != null && b.subtotalPence() > coupon.minimumPence()) {
            total -= coupon.offPence();
        }
        return total;
    }

    private Copies() {
    }
}
