package com.jk.explore.railway;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * The four checkout steps. Each returns a Result instead of throwing, and records that it ran.
 */
public final class CheckoutSteps {

    static final Map<String, Integer> STOCK = Map.of("MUG", 10, "LAMP", 0);
    static final Map<String, Double> PRICES = Map.of("MUG", 9.99, "LAMP", 45.00);

    private final List<String> ran = new ArrayList<>();

    public Result<Cart> validate(Cart cart) {
        ran.add("validate");
        if (cart.items().isEmpty()) {
            return Result.failure("validate", "the cart is empty");
        }
        if (cart.card().isBlank()) {
            return Result.failure("validate", "no card given");
        }
        return Result.success(cart);
    }

    public Result<Cart> reserve(Cart cart) {
        ran.add("reserve");
        for (Map.Entry<String, Integer> line : cart.items().entrySet()) {
            if (STOCK.getOrDefault(line.getKey(), 0) < line.getValue()) {
                return Result.failure("reserve", line.getKey() + " is out of stock");
            }
        }
        double total = cart.items().entrySet().stream().mapToDouble(e -> PRICES.get(e.getKey()) * e.getValue()).sum();
        return Result.success(cart.withTotal(total));
    }

    public Result<Cart> charge(Cart cart) {
        ran.add("charge");
        if (cart.card().endsWith("0002")) {
            return Result.failure("charge", "card declined");
        }
        return Result.success(cart.withOrder("ORD-1"));
    }

    public Result<Cart> email(Cart cart) {
        ran.add("email");
        return Result.success(cart);
    }

    public List<String> ran() {
        return ran;
    }

    /** The whole checkout, read top to bottom like the steps a person would list. */
    public Result<Cart> checkout(Cart cart) {
        return Result.success(cart)
                .flatMap(this::validate)
                .flatMap(this::reserve)
                .flatMap(this::charge)
                .flatMap(this::email);
    }
}
