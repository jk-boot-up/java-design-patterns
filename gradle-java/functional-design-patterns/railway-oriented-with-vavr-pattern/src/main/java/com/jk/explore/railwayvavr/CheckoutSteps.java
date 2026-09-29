package com.jk.explore.railwayvavr;

import io.vavr.control.Either;
import io.vavr.control.Try;
import io.vavr.control.Validation;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * The checkout steps. Each returns Vavr's Either: Left is the failure track, Right the success track.
 */
public final class CheckoutSteps {

    static final Map<String, Integer> STOCK = Map.of("MUG", 10, "LAMP", 0);
    static final Map<String, Double> PRICES = Map.of("MUG", 9.99, "LAMP", 45.00);

    private final List<String> ran = new ArrayList<>();

    public Either<Failure, Cart> validate(Cart cart) {
        ran.add("validate");
        if (cart.items().isEmpty()) {
            return Either.left(new Failure("validate", "the cart is empty"));
        }
        return cart.card().isBlank() ? Either.left(new Failure("validate", "no card given")) : Either.right(cart);
    }

    public Either<Failure, Cart> reserve(Cart cart) {
        ran.add("reserve");
        for (Map.Entry<String, Integer> line : cart.items().entrySet()) {
            if (STOCK.getOrDefault(line.getKey(), 0) < line.getValue()) {
                return Either.left(new Failure("reserve", line.getKey() + " is out of stock"));
            }
        }
        double total = cart.items().entrySet().stream().mapToDouble(e -> PRICES.get(e.getKey()) * e.getValue()).sum();
        return Either.right(cart.withTotal(total));
    }

    /** The payment company's client throws when a card is declined. Try turns that into the failure track. */
    public Either<Failure, Cart> charge(Cart cart) {
        ran.add("charge");
        return Try.of(() -> LegacyPayments.charge(cart.card(), cart.total()))
                .toEither()
                .mapLeft(e -> new Failure("charge", e.getMessage()))
                .map(cart::withOrder);
    }

    public Either<Failure, Cart> email(Cart cart) {
        ran.add("email");
        return Either.right(cart);
    }

    /** The whole checkout: four steps, read top to bottom. */
    public Either<Failure, Cart> checkout(Cart cart) {
        return Either.<Failure, Cart>right(cart)
                .flatMap(this::validate)
                .flatMap(this::reserve)
                .flatMap(this::charge)
                .flatMap(this::email);
    }

    /** Checking a form: Validation keeps every problem instead of stopping at the first. */
    public static Validation<io.vavr.collection.Seq<String>, Cart> checkForm(Cart cart) {
        Validation<String, Map<String, Integer>> items = cart.items().isEmpty()
                ? Validation.invalid("the cart is empty") : Validation.valid(cart.items());
        Validation<String, String> card = cart.card().isBlank()
                ? Validation.invalid("no card given") : Validation.valid(cart.card());
        return Validation.combine(items, card).ap(Cart::of);
    }

    public List<String> ran() {
        return ran;
    }
}
