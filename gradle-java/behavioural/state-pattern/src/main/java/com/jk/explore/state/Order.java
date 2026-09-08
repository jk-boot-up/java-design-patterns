package com.jk.explore.state;

import java.util.ArrayList;
import java.util.List;

/**
 * An order, and the context of the State pattern.
 *
 * <p>Every method here is one line: it hands the request to the current
 * state and lets that state decide. There is no {@code switch}, no
 * {@code if (status == ...)}, and no list of legal transitions — the legal
 * transitions are the methods each state chose to override.
 *
 * <p>The order does keep one thing the states do not: its history, including
 * the requests that were refused. An order that was asked to cancel and said
 * no is a different object, for support purposes, from one that was never
 * asked.
 */
public final class Order {

    private final String id;
    private final String customerEmail;
    private final List<OrderLine> lines;
    private final List<OrderEvent> history = new ArrayList<>();
    private final Ledger ledger = new Ledger();

    private OrderState state = PlacedState.INSTANCE;
    private String consignment = "(not shipped)";

    public Order(String id, String customerEmail, List<OrderLine> lines) {
        this.id = id;
        this.customerEmail = customerEmail;
        this.lines = List.copyOf(lines);
    }

    // --- the six requests -------------------------------------------------
    //
    // Each one delegates and records. Read them together: this is the entire
    // context class, and none of it knows which transitions are legal.

    public void pay() {
        attempt("pay", state -> state.pay(this));
    }

    public void pack() {
        attempt("pack", state -> state.pack(this));
    }

    public void ship() {
        attempt("ship", state -> state.ship(this));
    }

    public void deliver() {
        attempt("deliver", state -> state.deliver(this));
    }

    public void cancel(String reason) {
        attempt("cancel", state -> state.cancel(this, reason));
    }

    public void refund(String reason) {
        attempt("refund", state -> state.refund(this, reason));
    }

    /**
     * Run a request against the current state, and write down what happened
     * either way.
     *
     * <p>The refusal is recorded here rather than in the state, because a
     * state should not have to remember to log the fact that it said no. It
     * says no by not overriding a method.
     */
    private void attempt(String action, java.util.function.Consumer<OrderState> request) {
        String from = state.name();
        try {
            request.accept(state);
        } catch (IllegalTransitionException e) {
            history.add(OrderEvent.refused(action, from, e.reason()));
            throw e;
        }
    }

    /**
     * Move to the next state. Called by a state, never by a caller — which is
     * the difference between this pattern and Strategy in one method
     * signature.
     */
    void transitionTo(OrderState next, String action, String detail) {
        history.add(OrderEvent.moved(action, state.name(), next.name(), detail));
        state = next;
    }

    void recordConsignment(String consignment) {
        this.consignment = consignment;
    }

    // --- what the outside world can ask -----------------------------------

    public String id() {
        return id;
    }

    public String customerEmail() {
        return customerEmail;
    }

    public List<OrderLine> lines() {
        return lines;
    }

    public OrderState state() {
        return state;
    }

    /** The name of the state, for printing. */
    public String status() {
        return state.name();
    }

    /** Which buttons a screen should draw. One call, no conditionals. */
    public List<String> allowedActions() {
        return state.allowedActions();
    }

    public boolean canDo(String action) {
        return state.allowedActions().contains(action);
    }

    public Ledger ledger() {
        return ledger;
    }

    public String consignment() {
        return consignment;
    }

    public List<OrderEvent> history() {
        return List.copyOf(history);
    }

    public int itemCount() {
        return lines.stream().mapToInt(OrderLine::quantity).sum();
    }

    public Money total() {
        return lines.stream().map(OrderLine::total).reduce(Money.zero(), Money::plus);
    }

    @Override
    public String toString() {
        return String.format("%s  %-9s %8s  %s", id, status(), total(), customerEmail);
    }
}
