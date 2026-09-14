package com.jk.explore.saga;

import java.util.List;

/**
 * How a saga ended. There are three answers, not two.
 *
 * <p>{@code COMPLETED} — every step ran.
 *
 * <p>{@code COMPENSATED} — a step failed and every earlier step was cancelled out
 * successfully. The customer gets an apology and their money back, and nothing needs a
 * human.
 *
 * <p>{@code NEEDS_HUMAN_HELP} — a step failed, and then a compensation failed too. The shop
 * is now in a state no code in this project can fix: perhaps the money was taken and the
 * refund was refused. This outcome exists because pretending it cannot happen is how shops
 * end up with money they should not have and no record of why.
 */
public record SagaOutcome(String orderId, Status status, String failedStep,
                          List<String> compensated, List<String> couldNotCompensate) {

    public enum Status { COMPLETED, COMPENSATED, NEEDS_HUMAN_HELP }

    public boolean succeeded() {
        return status == Status.COMPLETED;
    }

    /** Whether somebody has to go and look at this order by hand. */
    public boolean needsHumanHelp() {
        return status == Status.NEEDS_HUMAN_HELP;
    }

    @Override
    public String toString() {
        return switch (status) {
            case COMPLETED -> orderId + ": completed";
            case COMPENSATED -> orderId + ": " + failedStep + " failed, undid "
                    + compensated;
            case NEEDS_HUMAN_HELP -> orderId + ": " + failedStep
                    + " failed and could not undo " + couldNotCompensate;
        };
    }
}
