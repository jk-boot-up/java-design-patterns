package com.jk.explore.objectmother;

import static com.jk.explore.objectmother.OrderBuilder.anOrder;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: hand-built test data, an Object Mother, the mother's explosion,
 * a Test Data Builder, and the bill.
 */
public final class ObjectMotherDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. Every test builds its own order by hand.");
        Order byHand = new Order(new Customer("Ana", "ana@example.com", false), "GB",
                List.of(new Line("MUG", 2, 9.99)), false);
        out.add("  3 constructors, 8 values, to test one rule: shipping " + money(ShippingRules.cost(byHand)));
        out.add("  which of the 8 values matter to this test? the reader cannot tell");
        out.add("  give Customer a new field, and every test like this must be edited");

        out.add("");
        out.add("TWO. An Object Mother: named, ready-made orders.");
        out.add("  TestOrders.domestic():      shipping " + money(ShippingRules.cost(TestOrders.domestic())));
        out.add("  TestOrders.vip():           shipping " + money(ShippingRules.cost(TestOrders.vip())));
        out.add("  TestOrders.international(): shipping " + money(ShippingRules.cost(TestOrders.international())));
        out.add("  one line per test, and a new Customer field is added in one place");

        out.add("");
        out.add("THREE. The mother grows a method for every mix.");
        String[] flags = {"vip", "international", "giftWrapped"};
        int combinations = 1 << flags.length;
        out.add("  " + flags.length + " yes-or-no details: " + combinations + " methods to cover every mix,"
                + " such as vipInternationalGiftWrapped()");
        out.add("  one more detail and it is " + (combinations * 2));

        out.add("");
        out.add("FOUR. A Test Data Builder: defaults, plus only what this test cares about.");
        Order vipAbroad = anOrder().vip().shippedTo("FR").build();
        out.add("  anOrder().vip().shippedTo(\"FR\").build(): shipping " + money(ShippingRules.cost(vipAbroad))
                + "  (VIP free shipping is UK only)");
        Order wrapped = anOrder().vip().giftWrapped().build();
        out.add("  anOrder().vip().giftWrapped().build():   shipping " + money(ShippingRules.cost(wrapped)));
        out.add("  any mix, in one line, and the test says exactly what matters");

        out.add("");
        out.add("FIVE. The bill: a test that leans on a hidden default.");
        out.add("  a free-shipping test was written as anOrder().build(), when the default price was 60.00");
        out.add("  then:  shipping " + money(ShippingRules.cost(anOrder().totalling(60).build())));
        out.add("  someone lowers the default to " + money(OrderBuilder.DEFAULT_PRICE) + ": shipping "
                + money(ShippingRules.cost(anOrder().build())) + ", and the test fails with no visible reason");
        out.add("  the fix: anOrder().totalling(60).build(), so the test states what it relies on");
        out.add("  defaults must be dull; anything a test depends on belongs in the test");
        return out;
    }

    static String money(double amount) {
        return String.format("%.2f", amount);
    }

    private ObjectMotherDemo() {
    }
}
