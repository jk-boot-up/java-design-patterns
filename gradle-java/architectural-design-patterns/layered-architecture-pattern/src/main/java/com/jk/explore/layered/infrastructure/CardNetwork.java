package com.jk.explore.layered.infrastructure;

import com.jk.explore.layered.domain.Money;

import java.util.ArrayList;
import java.util.List;

/**
 * Taking money from a card.
 *
 * <p>Nothing leaves this JVM. Every charge is recorded so a test can assert
 * that exactly one happened, for exactly the order total — which is acceptance
 * assertion A4 of the shared feature, and the one that catches an architecture
 * that has quietly started charging twice.
 */
public class CardNetwork {

    /** One charge, as it was recorded. */
    public record Charge(String customerId, Money amount) {
    }

    private final List<Charge> charges = new ArrayList<>();
    private final boolean declineEverything;

    private CardNetwork(boolean declineEverything) {
        this.declineEverything = declineEverything;
    }

    public static CardNetwork working() {
        return new CardNetwork(false);
    }

    /** A card that always refuses, for the third of the three refusal runs. */
    public static CardNetwork declining() {
        return new CardNetwork(true);
    }

    public void charge(String customerId, Money amount) {
        if (declineEverything) {
            throw new PaymentDeclinedException("card declined for " + amount);
        }
        charges.add(new Charge(customerId, amount));
    }

    public List<Charge> charges() {
        return List.copyOf(charges);
    }
}
