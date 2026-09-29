package com.jk.explore.railwayvavr;

import io.vavr.control.Either;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * The five acts, with Vavr's Either, Try and Validation.
 */
public final class VavrRailwayDemo {

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

        out.add("ONE. The payment library throws; nothing makes the caller handle it.");
        try {
            LegacyPayments.charge(DECLINED, 19.98);
            out.add("  charged");
        } catch (IllegalStateException e) {
            out.add("  LegacyPayments.charge threw \"" + e.getMessage() + "\"; a controller that forgot to catch it answers 500");
        }

        out.add("");
        out.add("TWO. Either<Failure, Cart>: each step's result, chained with flatMap.");
        CheckoutSteps steps = new CheckoutSteps();
        out.add("  2 mugs, good card: " + respond(steps.checkout(Cart.of(Map.of("MUG", 2), GOOD))));
        out.add("  " + trace(steps));

        out.add("");
        out.add("THREE. Left is the failure track; later steps are skipped.");
        CheckoutSteps empty = new CheckoutSteps();
        out.add("  empty cart:    " + respond(empty.checkout(Cart.of(Map.of(), GOOD))));
        out.add("  " + trace(empty));
        CheckoutSteps declined = new CheckoutSteps();
        out.add("  card declined: " + respond(declined.checkout(Cart.of(Map.of("MUG", 2), DECLINED))));
        out.add("  " + trace(declined));
        out.add("  Try.of(...).toEither() moved the library's exception onto the failure track");

        out.add("");
        out.add("FOUR. map for a plain step; orElse for a way back.");
        CheckoutSteps tax = new CheckoutSteps();
        Either<Failure, Cart> taxed = Either.<Failure, Cart>right(Cart.of(Map.of("MUG", 2), GOOD))
                .flatMap(tax::validate)
                .flatMap(tax::reserve)
                .map(c -> c.withTotal(Math.round(c.total() * 1.2 * 100) / 100.0));
        out.add("  2 mugs plus 20% tax: total " + taxed.fold(f -> "-", c -> String.format("%.2f", c.total())));
        CheckoutSteps lamp = new CheckoutSteps();
        Either<Failure, String> backOrder = lamp.checkout(Cart.of(Map.of("LAMP", 1), GOOD))
                .map(c -> "confirmed")
                .orElse(() -> Either.right("back-order placed, we will email when it arrives"));
        out.add("  lamp out of stock, with orElse: " + backOrder.get());

        out.add("");
        out.add("FIVE. The first failure stops a chain; Validation collects every problem.");
        out.add("  empty cart and no card, Either chain: " + respond(new CheckoutSteps().checkout(Cart.of(Map.of(), ""))));
        out.add("  the same form, Validation.combine: "
                + CheckoutSteps.checkForm(Cart.of(Map.of(), "")).fold(errors -> errors.mkString(" and "), c -> "ok"));
        out.add("  the bill: a library to learn and carry, and Left and Right to remember which is which");
        return out;
    }

    static String respond(Either<Failure, Cart> result) {
        return result.fold(f -> "422 " + f, c -> "200 order " + c.orderNumber() + " confirmed");
    }

    static String trace(CheckoutSteps steps) {
        List<String> skipped = ALL.stream().filter(s -> !steps.ran().contains(s)).toList();
        return "ran: " + String.join(", ", steps.ran()) + (skipped.isEmpty() ? "" : "; skipped: " + String.join(", ", skipped));
    }

    private VavrRailwayDemo() {
    }
}
