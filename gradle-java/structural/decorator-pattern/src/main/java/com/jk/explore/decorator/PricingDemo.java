package com.jk.explore.decorator;

import java.math.BigDecimal;

public final class PricingDemo {

    public static void main(String[] args) {
        PricedItem product = new Product("Wireless Headphones", new BigDecimal("79.99"));

        System.out.println("== Stacking decorators, one feature at a time ==");
        print(product);

        PricedItem giftWrapped = new GiftWrapDecorator(product);
        print(giftWrapped);

        PricedItem giftWrappedInsured = new InsuranceDecorator(giftWrapped);
        print(giftWrappedInsured);

        PricedItem giftWrappedInsuredExpress = new ExpressHandlingDecorator(giftWrappedInsured);
        print(giftWrappedInsuredExpress);

        System.out.println();
        System.out.println("== Stacking order changes the result -- insurance prices whatever it wraps ==");
        PricedItem insuredFirst = new InsuranceDecorator(product);
        PricedItem insuredThenGiftWrapped = new GiftWrapDecorator(insuredFirst);
        print(insuredThenGiftWrapped);
        System.out.println("(compare to gift-wrapped-then-insured above: same two decorators, different total)");

        System.out.println();
        System.out.println("== The naive alternative, for comparison ==");
        NaiveGiftWrappedInsuredProduct naive =
                new NaiveGiftWrappedInsuredProduct("Wireless Headphones", new BigDecimal("79.99"));
        System.out.println(naive.description() + ": $" + naive.cost());
        System.out.println("Same result as gift-wrapped-then-insured, but a whole new class was needed --");
        System.out.println("adding express handling to this combination would mean four more naive classes.");
    }

    private static void print(PricedItem item) {
        System.out.println(item.description() + ": $" + item.cost());
    }
}
