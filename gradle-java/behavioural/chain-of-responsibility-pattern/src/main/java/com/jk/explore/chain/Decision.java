package com.jk.explore.chain;

/**
 * A screening verdict, and the name of the link that reached it.
 *
 * <p>{@code decidedBy} is not decoration. In a chain, the question support asks
 * is never "was it rejected" — it is "which link rejected it". A verdict that
 * cannot answer that leaves you reading log messages and guessing.
 *
 * @param reason one sentence a human can read
 */
public record Decision(Outcome outcome, String decidedBy, String reason) {

    public static Decision approved(String decidedBy, String reason) {
        return new Decision(Outcome.APPROVED, decidedBy, reason);
    }

    public static Decision rejected(String decidedBy, String reason) {
        return new Decision(Outcome.REJECTED, decidedBy, reason);
    }

    public static Decision referred(String decidedBy, String reason) {
        return new Decision(Outcome.REFERRED, decidedBy, reason);
    }

    public boolean isApproved() {
        return outcome == Outcome.APPROVED;
    }

    @Override
    public String toString() {
        return outcome + " by " + decidedBy + ": " + reason;
    }
}
