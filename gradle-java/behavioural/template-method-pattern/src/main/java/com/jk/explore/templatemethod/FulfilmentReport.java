package com.jk.explore.templatemethod;

import java.util.ArrayList;
import java.util.List;

/**
 * What happened while an order was fulfilled: every step that ran, in the
 * order it ran, with the detail that route filled in.
 *
 * <p>This exists so the sequence is <em>observable</em>. A test can assert
 * that three completely different routes produced the same list of step
 * names, which is the claim the pattern actually makes; and the demo can
 * print the three side by side so a reader can see it rather than take it on
 * trust.
 */
public final class FulfilmentReport {

    /** One step of the sequence: its fixed name, and what this route did for it. */
    public record Step(String name, String detail) {
        @Override
        public String toString() {
            return String.format("%-14s %s", name, detail);
        }
    }

    private final String orderId;
    private final String route;
    private final List<Step> steps = new ArrayList<>();
    private final List<String> notifications = new ArrayList<>();
    private final List<String> notes = new ArrayList<>();
    private Money charged = Money.zero();
    private String dispatchReference = "(not dispatched)";

    FulfilmentReport(String orderId, String route) {
        this.orderId = orderId;
        this.route = route;
    }

    void step(String name, String detail) {
        steps.add(new Step(name, detail));
    }

    void charged(Money amount) {
        this.charged = amount;
    }

    void dispatchedAs(String reference) {
        this.dispatchReference = reference;
    }

    void notified(String message) {
        notifications.add(message);
    }

    /**
     * Something a route did that is not one of the six steps — the work an
     * {@code afterFulfilment} hook exists to carry. Notes are kept apart from
     * steps so that adding one cannot change the sequence a test asserts on.
     */
    void note(String text) {
        notes.add(text);
    }

    public String orderId() {
        return orderId;
    }

    public String route() {
        return route;
    }

    public List<Step> steps() {
        return List.copyOf(steps);
    }

    /**
     * The step names alone — the invariant part. Every route must produce the
     * same list from this method, however differently it filled the steps in.
     */
    public List<String> stepNames() {
        return steps.stream().map(Step::name).toList();
    }

    public Money charged() {
        return charged;
    }

    /** The courier consignment, the seller job, or the licence key. */
    public String dispatchReference() {
        return dispatchReference;
    }

    public List<String> notifications() {
        return List.copyOf(notifications);
    }

    public List<String> notes() {
        return List.copyOf(notes);
    }
}
