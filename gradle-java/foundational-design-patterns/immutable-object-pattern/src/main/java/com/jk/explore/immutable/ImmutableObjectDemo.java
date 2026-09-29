package com.jk.explore.immutable;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * The five acts: shared then changed, changed while being read, lost in a set, immutable objects, and the bill.
 */
public final class ImmutableObjectDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    static Map<String, Long> startPrices() {
        Map<String, Long> m = new LinkedHashMap<>();
        m.put("kettle", 3000L);
        m.put("mug", 1000L);
        m.put("teapot", 2500L);
        return m;
    }

    static final List<String> BASKET = List.of("kettle", "mug", "teapot");

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. One address object, shared, then changed.");
        MutableAddress profile = new MutableAddress("4 Mill Lane", "Leeds");
        Orders.OldOrder ord1 = new Orders.OldOrder("ORD-1", profile);
        out.add("  ORD-1 placed, ship to: " + ord1.shipTo());
        profile.setStreet("12 High Street");
        profile.setCity("York");
        out.add("  Priya moves and updates her profile for future orders");
        out.add("  ORD-1 now ships to: " + ord1.shipTo() + ", an order she placed before moving");

        out.add("");
        out.add("TWO. A price list changed while someone reads it.");
        MutablePriceList shared = new MutablePriceList(startPrices());
        out.add("  basket before the sale: " + pounds(shared.total(BASKET)));
        shared.set("kettle", 2700);
        out.add("  10% sale, applied one price at a time; a checkout reads after the first: "
                + pounds(shared.total(BASKET)));
        shared.set("mug", 900);
        shared.set("teapot", 2250);
        out.add("  basket after the sale: " + pounds(shared.total(BASKET))
                + "; that customer paid a price that never existed");

        out.add("");
        out.add("THREE. A changed object is lost in a set.");
        Set<MutableAddress> failedDeliveries = new HashSet<>();
        MutableAddress tom = new MutableAddress("9 Park Road", "Bath");
        failedDeliveries.add(tom);
        tom.setStreet("9 Park Rd");
        out.add("  address added to the failed-deliveries set, then its spelling tidied");
        out.add("  set contains it: " + failedDeliveries.contains(tom) + ", although the set's size is "
                + failedDeliveries.size());

        out.add("");
        out.add("FOUR. Immutable objects: a change makes a new object.");
        Address home = new Address("4 Mill Lane", "Leeds");
        Orders.Order ord2 = new Orders.Order("ORD-2", home);
        Address moved = home.withStreet("12 High Street").withCity("York");
        out.add("  profile is now " + moved + "; ORD-2 still ships to " + ord2.shipTo());
        Shop shop = new Shop(new PriceList(startPrices()));
        PriceList sale = shop.prices().withSale(10);
        out.add("  sale list built on the side; checkout still reads " + pounds(shop.prices().total(BASKET)));
        shop.publish(sale);
        out.add("  published in one swap; checkout now reads " + pounds(shop.prices().total(BASKET))
                + ", never a mix");
        Map<String, Long> input = startPrices();
        PriceList copied = new PriceList(input);
        input.put("kettle", 1L);
        out.add("  the map it was built from is changed afterwards; kettle still " + pounds(copied.prices().get("kettle")));
        Set<Address> failed = new HashSet<>(Set.of(new Address("9 Park Road", "Bath")));
        out.add("  set contains 9 Park Road: " + failed.contains(new Address("9 Park Road", "Bath")));

        out.add("");
        out.add("FIVE. The bill: every change is a copy.");
        Map<String, Long> big = new HashMap<>();
        for (int i = 0; i < 1000; i++) {
            big.put("item-" + i, 100L);
        }
        PriceList catalogue = new PriceList(big);
        PriceList oneChanged = catalogue.withPrice("item-7", 90);
        out.add("  change 1 price in a 1000-item list: a new list of " + oneChanged.size() + " entries");
        out.add("  and every field you may change needs its own with...() method");
        return out;
    }

    static String pounds(long pence) {
        return String.format("£%d.%02d", pence / 100, pence % 100);
    }

    private ImmutableObjectDemo() {
    }
}
