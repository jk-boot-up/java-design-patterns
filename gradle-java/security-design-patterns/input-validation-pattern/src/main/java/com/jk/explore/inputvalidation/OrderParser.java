package com.jk.explore.inputvalidation;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Supplier;

/**
 * The pattern at the boundary: turn untrusted text into checked values, collecting every problem
 * so the customer can fix them all at once.
 */
public final class OrderParser {

    public record Result(ValidOrder order, List<String> problems) {

        public boolean ok() {
            return problems.isEmpty();
        }
    }

    public static Result parse(OrderForm form) {
        List<String> problems = new ArrayList<>();
        Sku sku = attempt(() -> new Sku(form.sku()), problems);
        Quantity quantity = attempt(() -> Quantity.parse(form.quantity()), problems);
        Email email = attempt(() -> new Email(form.email()), problems);
        CustomerName name = attempt(() -> new CustomerName(form.name()), problems);
        return new Result(problems.isEmpty() ? new ValidOrder(sku, quantity, email, name) : null, problems);
    }

    private static <T> T attempt(Supplier<T> make, List<String> problems) {
        try {
            return make.get();
        } catch (IllegalArgumentException e) {
            problems.add(e.getMessage());
            return null;
        }
    }

    private OrderParser() {
    }
}
