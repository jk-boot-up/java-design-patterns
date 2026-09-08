package com.jk.explore.chain;

import java.util.List;

/**
 * The verdict, plus which links ran and which never did.
 *
 * <p>{@link #neverRan()} is the part a sequence of {@code if} statements never
 * gives you. Once a link stops the chain, the links behind it are not merely
 * ignored — they are never executed. A fraud check that costs a network call is
 * not paid for on an order already rejected for a bad postcode.
 */
public record ScreeningReport(String chain,
                              Decision decision,
                              List<String> consulted,
                              List<String> neverRan) {

    public ScreeningReport {
        consulted = List.copyOf(consulted);
        neverRan = List.copyOf(neverRan);
    }

    public Outcome outcome() {
        return decision.outcome();
    }

    public boolean isApproved() {
        return decision.isApproved();
    }

    @Override
    public String toString() {
        String line = String.format("%-9s by %-14s %s",
                decision.outcome(), decision.decidedBy(), decision.reason());
        if (!neverRan.isEmpty()) {
            line += System.lineSeparator() + "              never ran: " + String.join(", ", neverRan);
        }
        return line;
    }
}
