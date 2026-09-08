package com.jk.explore.state;

import java.util.List;

/**
 * What an order is allowed to do, right now.
 *
 * <p>There is one implementation per state an order can be in, and each one
 * overrides only the actions that state permits. Everything else falls
 * through to the defaults below, which refuse — so an illegal transition is
 * not something anybody has to remember to check for. It is what happens when
 * a state says nothing.
 *
 * <p>The states hold no data of their own, only behaviour, so one instance of
 * each is enough and every implementation exposes a single {@code INSTANCE}.
 *
 * <p><b>This is not Strategy</b>, although the class diagram is identical. A
 * strategy is chosen by the caller and never replaces itself. A state is
 * entered as a consequence of what the order did, and states hand control to
 * one another: {@link PlacedState#pay} is what decides the order is now
 * {@link PaidState}, and no caller is consulted about it.
 */
public interface OrderState {

    /** The name a customer, an operator or a log line would recognise. */
    String name();

    /**
     * Everything this state permits, in the order a screen would show them.
     *
     * <p>This exists because the interesting question is rarely "may I cancel
     * this order" one action at a time — it is "which buttons do I draw". With
     * a status field that question needs a third copy of the same chain of
     * conditionals; here it is one method per state, sitting next to the code
     * that implements the answers.
     */
    List<String> allowedActions();

    default void pay(Order order) {
        throw refuse("pay");
    }

    default void pack(Order order) {
        throw refuse("pack");
    }

    default void ship(Order order) {
        throw refuse("ship");
    }

    default void deliver(Order order) {
        throw refuse("deliver");
    }

    default void cancel(Order order, String reason) {
        throw refuse("cancel");
    }

    default void refund(Order order, String reason) {
        throw refuse("refund");
    }

    /** A refusal whose message names this state and what it would have accepted. */
    default IllegalTransitionException refuse(String action) {
        return new IllegalTransitionException(name(), action, because());
    }

    /** A refusal with a reason of its own, where the generic one is too vague. */
    default IllegalTransitionException refuse(String action, String reason) {
        return new IllegalTransitionException(name(), action, reason);
    }

    private String because() {
        List<String> allowed = allowedActions();
        return allowed.isEmpty()
                ? "it is final, and nothing more can happen to it"
                : "the only thing it will accept is " + String.join(" or ", allowed);
    }
}
