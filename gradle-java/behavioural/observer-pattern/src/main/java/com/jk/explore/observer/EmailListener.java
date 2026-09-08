package com.jk.explore.observer;

import java.util.Objects;
import java.util.function.Consumer;

/**
 * Sends the customer a message on every status change.
 *
 * <p>The copy lives here, next to the decision to send it, rather than in the
 * order. That is the ordinary payoff of the pattern: marketing rewriting the
 * shipping email touches one file, and it is not the file the payment team is
 * also editing.
 */
public final class EmailListener implements OrderListener {

    private final String customerEmail;
    private final Consumer<String> sink;
    private int sent;

    public EmailListener(String customerEmail, Consumer<String> sink) {
        this.customerEmail = Objects.requireNonNull(customerEmail, "customerEmail");
        this.sink = Objects.requireNonNull(sink, "sink");
    }

    @Override
    public String name() {
        return "email";
    }

    @Override
    public void onStatusChanged(OrderEvent event) {
        sent++;
        sink.accept("  [email] to " + customerEmail + ": " + subjectFor(event));
    }

    private String subjectFor(OrderEvent event) {
        return switch (event.to()) {
            case PLACED -> "We have your order " + event.orderId();
            case PAID -> "Payment received for " + event.orderId();
            case SHIPPED -> "Your order " + event.orderId() + " is on its way";
            case DELIVERED -> "Your order " + event.orderId() + " has arrived";
            case CANCELLED -> "Your order " + event.orderId() + " has been cancelled";
        };
    }

    public int sent() {
        return sent;
    }
}
