package com.jk.explore.delegation;

import com.jk.explore.delegation.naive.GiftOrder;
import com.jk.explore.delegation.naive.PlainOrder;
import com.jk.explore.delegation.naive.PremiumGiftOrder;
import com.jk.explore.delegation.naive.PremiumOrder;
import java.util.List;

public class DelegationDemo {

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. A subclass for each way of pricing.");
        List<Class<?>> classes = List.of(PlainOrder.class, PremiumOrder.class, GiftOrder.class, PremiumGiftOrder.class);
        System.out.println("  premium, gift wrap, and both: " + classes.size() + " classes for 2 features. a third feature would need " + (1 << 3) + ".");
        System.out.println("  premium and gift order: " + new PremiumGiftOrder(10000, 2).total() + ". and an order cannot change its class once it exists.");
    }

    private static void two() {
        System.out.println("TWO. The order hands the pricing on.");
        Order plain = new Order(10000, 2, PricingRule.NONE);
        Order premium = new Order(10000, 2, PricingRule.premium());
        Order gift = new Order(10000, 2, PricingRule.giftWrap());
        System.out.println("  one Order class. no rule " + plain.total() + ", premium " + premium.total() + ", gift wrap " + gift.total() + ".");
    }

    private static void three() {
        System.out.println("THREE. Change the helper while it lives.");
        Order order = new Order(10000, 2, PricingRule.NONE);
        long before = order.total();
        order.useRule(PricingRule.premium());
        System.out.println("  the customer joins the premium plan while shopping. the same order object: " + before + " then " + order.total() + ".");
    }

    private static void four() {
        System.out.println("FOUR. Two helpers at once.");
        Order order = new Order(10000, 2, PricingRule.inOrder(PricingRule.premium(), PricingRule.giftWrap()));
        System.out.println("  premium then gift wrap: " + order.total() + ", the same as the class made for both. classes added: 0.");
    }

    private static void five() {
        System.out.println("FIVE. The helper needs to see the order.");
        Order two = new Order(10000, 2, PricingRule.giftWrap());
        Order three = new Order(10000, 3, PricingRule.giftWrap());
        System.out.println("  gift wrap is 300 for each item, so it must look at the order it was called for. 2 items: " + two.total() + ". 3 items: " + three.total() + ".");
        System.out.println("  that is why the order passes itself in: the helper is a different object, and does not know which order it is helping.");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        PricingRule.CALLS.set(0);
        Order order = new Order(10000, 2, PricingRule.inOrder(PricingRule.NONE, PricingRule.premium(), PricingRule.giftWrap()));
        order.total();
        System.out.println("  one total() made " + PricingRule.CALLS.get() + " calls to helpers, where inheritance made none: one more hop for every helper.");
        System.out.println("  to look like a helper with " + Shipping.class.getMethods().length + " methods, the order had to write " + OrderWithShipping.class.getDeclaredMethods().length + " forwarding methods that only pass the call on.");
        System.out.println("  and a helper knows nothing of its owner unless it is told: it cannot call a method on the order that the order did not pass in.");
    }
}
