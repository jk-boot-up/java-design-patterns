package com.jk.explore.railway;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * The five acts: exceptions the caller forgot, the happy track, switching to the failure track,
 * plain functions and a way back, and the bill.
 */
public final class RailwayDemo {

    static final String GOOD = "4000000000000001";
    static final String DECLINED = "4000000000000002";
    static final List<String> ALL = List.of("validate", "reserve", "charge", "email");

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. Exceptions, and a catch nobody wrote.");
        out.add("  out of stock:  " + ExceptionCheckout.controller(Cart.of(Map.of("LAMP", 1), GOOD)));
        out.add("  card declined: " + ExceptionCheckout.controller(Cart.of(Map.of("MUG", 2), DECLINED)));
        out.add("  the declined-card exception was added later; nothing forced the controller to handle it");

        out.add("");
        out.add("TWO. Each step returns a Result; the steps are chained in a straight line.");
        CheckoutSteps steps = new CheckoutSteps();
        out.add("  2 mugs, good card: " + respond(steps.checkout(Cart.of(Map.of("MUG", 2), GOOD))));
        out.add("  " + trace(steps));

        out.add("");
        out.add("THREE. A failure switches to the other track; later steps are skipped.");
        CheckoutSteps empty = new CheckoutSteps();
        out.add("  empty cart:    " + respond(empty.checkout(Cart.of(Map.of(), GOOD))));
        out.add("  " + trace(empty));
        CheckoutSteps declined = new CheckoutSteps();
        out.add("  card declined: " + respond(declined.checkout(Cart.of(Map.of("MUG", 2), DECLINED))));
        out.add("  " + trace(declined));

        out.add("");
        out.add("FOUR. Plain functions ride along with map; recover offers a way back.");
        CheckoutSteps withTax = new CheckoutSteps();
        Result<Cart> taxed = Result.success(Cart.of(Map.of("MUG", 2), GOOD))
                .flatMap(withTax::validate)
                .flatMap(withTax::reserve)
                .map(c -> c.withTotal(Math.round(c.total() * 1.2 * 100) / 100.0));
        out.add("  2 mugs plus 20% tax, with map: total " + taxed.fold(c -> String.format("%.2f", c.total()), f -> "-"));
        CheckoutSteps lamp = new CheckoutSteps();
        Result<Cart> backOrder = lamp.checkout(Cart.of(Map.of("LAMP", 1), GOOD))
                .recover(f -> f.step().equals("reserve") ? Result.success(Cart.of(Map.of("LAMP", 1), GOOD).asBackOrder())
                        : f);
        out.add("  lamp out of stock, recovered: " + backOrder.fold(
                c -> c.backOrder() ? "back-order placed, we will email when it arrives" : "ok", f -> f.reason()));

        out.add("");
        out.add("FIVE. The bill: the first failure stops everything.");
        CheckoutSteps both = new CheckoutSteps();
        out.add("  empty cart and no card: " + respond(both.checkout(Cart.of(Map.of(), ""))));
        out.add("  only the first problem is reported; showing every form error needs a different tool");
        out.add("  and it is an unfamiliar style in Java: keep exceptions for the truly unexpected");
        return out;
    }

    static String respond(Result<Cart> result) {
        return result.fold(c -> "200 order " + c.orderNumber() + " confirmed",
                f -> "422 " + f.reason() + " (at " + f.step() + ")");
    }

    static String trace(CheckoutSteps steps) {
        List<String> skipped = ALL.stream().filter(s -> !steps.ran().contains(s)).toList();
        return "ran: " + String.join(", ", steps.ran()) + (skipped.isEmpty() ? "" : "; skipped: " + String.join(", ", skipped));
    }

    private RailwayDemo() {
    }
}
