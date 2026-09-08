package com.jk.explore.adapter;

import java.math.BigDecimal;

public final class ShippingDemo {

    public static void main(String[] args) {
        System.out.println("== Checkout works with any ShippingRateProvider, adapted or native ==");

        ShippingRateProvider acme = new AcmeShippingAdapter(new AcmeShippingSdk());
        CheckoutService checkoutWithAcme = new CheckoutService(acme);
        System.out.println("Acme (adapted):  $" + checkoutWithAcme.totalWithShipping(
                new BigDecimal("49.98"), "94107", 3.5));

        ShippingRateProvider flatRate = new FlatRateShippingProvider();
        CheckoutService checkoutWithFlatRate = new CheckoutService(flatRate);
        System.out.println("Flat rate (native):  $" + checkoutWithFlatRate.totalWithShipping(
                new BigDecimal("49.98"), "94107", 3.5));
        System.out.println();

        System.out.println("== The adapter converts units at exactly one seam ==");
        System.out.println("3.5 kg checkout weight -> AcmeShippingSdk sees pounds, returns cents");
        System.out.println("Quoted rate: $" + acme.quoteRate("94107", 3.5));
        System.out.println();

        System.out.println("== The naive alternative, for comparison ==");
        NaiveCheckoutService naiveCheckout = new NaiveCheckoutService();
        NaiveShippingEstimator naiveEstimator = new NaiveShippingEstimator();
        System.out.println("NaiveCheckoutService:    $" + naiveCheckout.shippingCost("94107", 3.5));
        System.out.println("NaiveShippingEstimator:  $" + naiveEstimator.estimate("94107", 3.5));
        System.out.println("Same result, but the pounds/cents conversion is duplicated in both classes,");
        System.out.println("and both are coupled directly to AcmeShippingSdk's shape.");
    }
}
