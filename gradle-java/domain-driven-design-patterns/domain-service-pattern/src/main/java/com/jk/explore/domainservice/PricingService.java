package com.jk.explore.domainservice;

import com.jk.explore.domainservice.Model.Basket;
import com.jk.explore.domainservice.Model.Coupon;
import com.jk.explore.domainservice.Model.Customer;
import com.jk.explore.domainservice.Model.Tier;

/**
 * The pattern: a business rule that involves several domain objects and belongs to none of them, in its own stateless class.
 *
 * <p>The rule: gold customers get 10% off; a coupon gives its amount off
 * baskets over its minimum; the two do not add up, the bigger discount wins.
 * The class holds no data between calls, and is named in the shop's own words.
 */
public final class PricingService {

    /** The price, and the reason for it in words a customer service agent could read out. */
    public record Price(long totalPence, String why) {
    }

    public Price price(Customer customer, Basket basket, Coupon coupon) {
        long sub = basket.subtotalPence();
        long gold = customer.tier() == Tier.GOLD ? sub * 10 / 100 : 0;
        long off = coupon != null && sub > coupon.minimumPence() ? coupon.offPence() : 0;
        String why;
        if (gold == 0 && off == 0) {
            why = "no discount";
        } else if (gold >= off) {
            why = "gold 10% -" + DomainServiceDemo.pounds(gold) + (off > 0 ? " beats " + coupon.code() + " -" + DomainServiceDemo.pounds(off) : "");
        } else {
            why = coupon.code() + " -" + DomainServiceDemo.pounds(off) + (gold > 0 ? " beats gold -" + DomainServiceDemo.pounds(gold) : "");
        }
        return new Price(sub - Math.max(gold, off), "subtotal " + DomainServiceDemo.pounds(sub) + "; " + why);
    }
}
