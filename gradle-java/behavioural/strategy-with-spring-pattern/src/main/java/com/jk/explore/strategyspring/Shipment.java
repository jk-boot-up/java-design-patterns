package com.jk.explore.strategyspring;

/** What a rule may look at. Carries more than any one rule uses, so a new rule never changes the interface. */
public record Shipment(int weightGrams, int miles, long orderTotalPence) {
}
