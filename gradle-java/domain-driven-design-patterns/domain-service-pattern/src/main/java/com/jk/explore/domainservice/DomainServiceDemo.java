package com.jk.explore.domainservice;

import com.jk.explore.domainservice.Model.Basket;
import com.jk.explore.domainservice.Model.Coupon;
import com.jk.explore.domainservice.Model.Customer;
import com.jk.explore.domainservice.Model.Line;
import com.jk.explore.domainservice.Model.Tier;
import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: the rule copied into two places, a domain service, the rule in the shop's words, many cases one service, and the bill.
 */
public final class DomainServiceDemo {

    static final Basket BASKET = new Basket(List.of(new Line("kettle", 3000), new Line("teapot", 2500), new Line("mug", 500)));
    static final Customer PRIYA = new Customer("C-17", Tier.GOLD);

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. The pricing rule, copied into the web checkout and the phone app.");
        out.add("  gold customer, £60 basket, coupon SAVE5");
        out.add("  web checkout says: " + pounds(Copies.webCheckout(PRIYA, BASKET, Coupon.SAVE5)));
        out.add("  phone app says:    " + pounds(Copies.phoneApp(PRIYA, BASKET, Coupon.SAVE5)));
        out.add("  the app's copy is older: it adds both discounts; the rule says the bigger one wins");

        out.add("");
        out.add("TWO. A domain service: the rule in one place, used by both.");
        PricingService pricing = new PricingService();
        out.add("  web checkout: " + pounds(pricing.price(PRIYA, BASKET, Coupon.SAVE5).totalPence()));
        out.add("  phone app:    " + pounds(pricing.price(PRIYA, BASKET, Coupon.SAVE5).totalPence()));

        out.add("");
        out.add("THREE. The rule speaks the shop's language.");
        out.add("  " + pricing.price(PRIYA, BASKET, Coupon.SAVE5).why());
        out.add("  the rule needs the customer, the basket and the coupon; it belongs to none of them alone");

        out.add("");
        out.add("FOUR. One stateless service, every case.");
        Customer tom = new Customer("C-42", Tier.STANDARD);
        Basket small = new Basket(List.of(new Line("mug", 500), new Line("tea towel", 600), new Line("teapot", 1900)));
        Object[][] cases = {
            {tom, BASKET, null}, {tom, BASKET, Coupon.SAVE5}, {PRIYA, BASKET, null},
            {PRIYA, BASKET, Coupon.SAVE5}, {tom, small, Coupon.SAVE5}};
        for (Object[] c : cases) {
            PricingService.Price price = pricing.price((Customer) c[0], (Basket) c[1], (Coupon) c[2]);
            out.add("  " + ((Customer) c[0]).tier() + ", " + pounds(((Basket) c[1]).subtotalPence()) + ", "
                    + (c[2] == null ? "no coupon" : "SAVE5") + ": " + pounds(price.totalPence()));
        }
        out.add("  one service object priced all five; it keeps nothing between calls");

        out.add("");
        out.add("FIVE. The bill: services can empty the objects.");
        out.add("  the basket still works out its own subtotal: " + pounds(BASKET.subtotalPence()));
        out.add("  move that into a service too, and the basket becomes a bag of data with no behaviour");
        return out;
    }

    static String pounds(long pence) {
        return String.format("£%d.%02d", pence / 100, pence % 100);
    }

    private DomainServiceDemo() {
    }
}
