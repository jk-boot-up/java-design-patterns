package com.jk.explore.state;

/**
 * Thrown when an order is asked to do something its current state does not
 * allow — cancelling a parcel that is already on a van, paying twice.
 *
 * <p>The message always names the state that refused, because "cannot cancel"
 * is not a useful thing to read in a support ticket and "cannot cancel a
 * SHIPPED order" is.
 */
public class IllegalTransitionException extends RuntimeException {

    private final String state;
    private final String action;
    private final String reason;

    public IllegalTransitionException(String state, String action, String reason) {
        super("cannot " + action + " " + article(state) + " " + state + " order: " + reason);
        this.state = state;
        this.action = action;
        this.reason = reason;
    }

    /** "a PLACED order", but "an AT-LOCKER order". */
    private static String article(String state) {
        return "AEIOU".indexOf(state.charAt(0)) >= 0 ? "an" : "a";
    }

    /** The state that refused — not the state the caller thought it was in. */
    public String state() {
        return state;
    }

    public String action() {
        return action;
    }

    public String reason() {
        return reason;
    }
}
