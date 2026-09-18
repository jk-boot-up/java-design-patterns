package com.jk.explore.cleanspring.adapters.gateway;

import com.jk.explore.cleanspring.entities.Money;
import com.jk.explore.cleanspring.usecases.PaymentDeclinedException;
import com.jk.explore.cleanspring.usecases.PaymentGateway;

import java.util.ArrayList;
import java.util.List;

public class InMemoryPaymentGateway implements PaymentGateway {

    public record Charge(String customerId, Money amount) {
    }

    private final List<Charge> charges = new ArrayList<>();
    private final boolean declineEverything;

    private InMemoryPaymentGateway(boolean declineEverything) {
        this.declineEverything = declineEverything;
    }

    public static InMemoryPaymentGateway working() {
        return new InMemoryPaymentGateway(false);
    }

    public static InMemoryPaymentGateway declining() {
        return new InMemoryPaymentGateway(true);
    }

    @Override
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
