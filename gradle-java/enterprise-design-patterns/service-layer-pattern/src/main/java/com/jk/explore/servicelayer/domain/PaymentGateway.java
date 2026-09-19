package com.jk.explore.servicelayer.domain;

import java.util.ArrayList;
import java.util.List;

/** A fake payment gateway that remembers every charge, so a demo can say what a customer was charged. */
public class PaymentGateway {

    private final List<Integer> chargesPence = new ArrayList<>();

    public void charge(int customerId, int pence) {
        chargesPence.add(pence);
    }

    public int totalChargedPence() {
        return chargesPence.stream().mapToInt(Integer::intValue).sum();
    }
}
