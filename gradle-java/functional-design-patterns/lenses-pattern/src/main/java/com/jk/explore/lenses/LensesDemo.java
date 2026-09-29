package com.jk.explore.lenses;

import static com.jk.explore.lenses.Lenses.ADDRESS_POSTCODE;
import static com.jk.explore.lenses.Lenses.ORDER_CITY;
import static com.jk.explore.lenses.Lenses.ORDER_POSTCODE;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: rebuilding by hand, one lens, joined lenses, changing with a function, and the bill.
 */
public final class LensesDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();
        Order order = new Order("ORD-9",
                new Customer("Ana", new Address("1 High Street", "Leeds", "LS1 4AP")),
                List.of("2 x Blue mug", "1 x Teapot"));

        out.add("ONE. Changing one field of an immutable order, by hand.");
        Customer c = order.customer();
        Address a = c.address();
        Order byHand = new Order(order.id(), new Customer(c.name(), new Address(a.city(), a.street(), "LS2 7HY")),
                order.lines());
        out.add("  3 constructors to change the postcode");
        out.add("  result: " + byHand.customer().address());
        out.add("  street and city are both strings, and were swapped by mistake; nothing complained");

        out.add("");
        out.add("TWO. A lens: get and set for one field.");
        out.add("  ADDRESS_POSTCODE.get(address):            " + ADDRESS_POSTCODE.get().apply(a));
        Address moved = ADDRESS_POSTCODE.set().apply(a, "LS2 7HY");
        out.add("  ADDRESS_POSTCODE.set(address, \"LS2 7HY\"): " + moved);
        out.add("  the original is unchanged:                " + a);

        out.add("");
        out.add("THREE. Lenses join, to reach deep inside.");
        out.add("  ORDER_POSTCODE = ORDER_CUSTOMER.andThen(CUSTOMER_ADDRESS).andThen(ADDRESS_POSTCODE)");
        Order updated = ORDER_POSTCODE.set().apply(order, "LS2 7HY");
        out.add("  ORDER_POSTCODE.set(order, \"LS2 7HY\"): " + updated.customer().address());
        out.add("  the old order still says:            " + order.customer().address());

        out.add("");
        out.add("FOUR. Change a part with a function.");
        Order typed = ORDER_POSTCODE.set().apply(order, "ls2 7hy");
        out.add("  typed in lower case:            " + ORDER_POSTCODE.get().apply(typed));
        out.add("  ORDER_POSTCODE.modify(upper):   " + ORDER_POSTCODE.get().apply(ORDER_POSTCODE.modify(typed, String::toUpperCase)));
        Order york = ORDER_CITY.set().apply(ORDER_POSTCODE.set().apply(order, "YO1 7HH"), "York");
        out.add("  city and postcode, two lenses:  " + york.customer().address());

        out.add("");
        out.add("FIVE. The bill: lenses are code to write.");
        out.add("  4 field lenses written by hand for 3 levels; Java has no built-in way to make them");
        out.add("  each set makes 3 new objects, but unchanged parts are shared: lines are the same list: "
                + (updated.lines() == order.lines()));
        out.add("  for one or two shallow records, a small 'with' method is simpler");
        return out;
    }

    private LensesDemo() {
    }
}
