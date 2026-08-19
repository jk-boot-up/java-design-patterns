package com.jk.explore.staticfactory;

import java.util.List;

/**
 * Runs the same order through five different coupon codes, then shows the
 * two things only a static factory can do: hand back a shared instance, and
 * silently swap the class it returns.
 */
public class StaticFactoryDemo {

    public static void main(String[] args) {
        CheckoutService checkout = new CheckoutService();
        Order order = new Order("ORD-4001", "CUST-001", Money.pounds(120.00), Money.pounds(4.99));

        List<String> coupons = List.of("SAVE10", "FIVEROFF", "FREESHIP", "BESTDEAL", "");
        for (String coupon : coupons) {
            System.out.println("Coupon: " + (coupon.isEmpty() ? "(none)" : coupon));
            Receipt receipt = checkout.checkout(order, Discount.forCoupon(coupon));
            System.out.println("Receipt: " + receipt);
            System.out.println();
        }

        // Named, so nobody has to guess what the number means.
        System.out.println("percentage(10) -> " + Discount.percentage(10).describe());
        System.out.println("amountOff(£10) -> " + Discount.amountOff(Money.pounds(10)).describe());

        // No new object where none is needed.
        System.out.println("none() is shared: " + (Discount.none() == Discount.none()));
        System.out.println("zero() is shared: " + (Money.zero() == Money.zero()));

        // The factory picked the class, not the caller.
        System.out.println("percentage(0) -> " + Discount.percentage(0).describe());

        try {
            Discount.forCoupon("SAVE99");
        } catch (IllegalArgumentException e) {
            System.out.println("Rejected: " + e.getMessage());
        }
    }
}
