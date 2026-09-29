package com.jk.explore.currying;

import java.util.ArrayList;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.function.BiFunction;
import java.util.function.Function;

/**
 * The five acts: repeated arguments, a curried function, ready-made functions per zone,
 * argument order, and the bill.
 */
public final class CurryingDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();
        List<Double> parcels = List.of(0.5, 2.0, 10.0);

        out.add("ONE. The same arguments, passed again and again.");
        for (double kg : parcels) {
            out.add("  price(EU, STANDARD, " + kg + ") = " + money(Shipping.price(Zone.EU, Service.STANDARD, kg)));
        }
        out.add("  the EU warehouse repeats \"EU, STANDARD\" in every call; only the weight changes");

        out.add("");
        out.add("TWO. Curried: fix the first arguments once, get a function of the rest.");
        Function<Double, Double> euStandard = Shipping.CURRIED.apply(Zone.EU).apply(Service.STANDARD);
        out.add("  euStandard = CURRIED.apply(EU).apply(STANDARD)");
        out.add("  euStandard.apply(2.0) = " + money(euStandard.apply(2.0)) + ", the same as price(EU, STANDARD, 2.0)");

        out.add("");
        out.add("THREE. Ready-made functions, one per zone, built at start-up.");
        Map<Zone, Function<Double, Double>> standardByZone = new EnumMap<>(Zone.class);
        for (Zone zone : Zone.values()) {
            standardByZone.put(zone, Shipping.CURRIED.apply(zone).apply(Service.STANDARD));
        }
        Function<Double, Double> euExpress = Shipping.CURRIED.apply(Zone.EU).apply(Service.EXPRESS);
        out.add("  a 2 kg parcel, standard: UK " + money(standardByZone.get(Zone.UK).apply(2.0))
                + ", EU " + money(standardByZone.get(Zone.EU).apply(2.0))
                + ", WORLD " + money(standardByZone.get(Zone.WORLD).apply(2.0)));
        out.add("  checkout's parcels, EU express, with map: "
                + parcels.stream().map(euExpress).map(CurryingDemo::money).toList());

        out.add("");
        out.add("FOUR. Argument order matters: what is fixed first must come first.");
        BiFunction<Double, Double, Double> discount = (percent, price) -> price * (100 - percent) / 100;
        Function<Double, Double> twentyOff = Shipping.curry(discount).apply(20.0);
        out.add("  discount(percent, price), curried, then apply(20): a \"20% off\" function");
        out.add("  twentyOff.apply(45.0) = " + money(twentyOff.apply(45.0)));
        BiFunction<Double, Double, Double> backwards = (price, percent) -> price * (100 - percent) / 100;
        out.add("  with (price, percent) the first thing fixed is a price: curry(backwards).apply(20.0) is \"a 20.00 item\"");
        out.add("  applied to 45 it gives " + money(Shipping.curry(backwards).apply(20.0).apply(45.0))
                + ", not a discount at all");

        out.add("");
        out.add("FIVE. The bill: Java makes it noisy.");
        out.add("  the type is Function<Zone, Function<Service, Function<Double, Double>>>");
        Function<Double, Double> plainLambda = kg -> Shipping.price(Zone.EU, Service.STANDARD, kg);
        out.add("  a plain lambda, kg -> price(EU, STANDARD, kg), gives the same " + money(plainLambda.apply(2.0))
                + ", and is often clearer");
        return out;
    }

    static String money(double amount) {
        return String.format("%.2f", amount);
    }

    private CurryingDemo() {
    }
}
