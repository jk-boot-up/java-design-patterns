package com.jk.explore.dependencyinjection.domain;

import java.util.ArrayList;
import java.util.List;

/** A gateway that remembers every charge, so a demo or test can say what was taken. */
public final class RecordingGateway implements PaymentGateway {

    private final List<Long> charges = new ArrayList<>();

    @Override
    public String charge(long pence) {
        charges.add(pence);
        return "receipt-" + charges.size();
    }

    public List<Long> charges() {
        return List.copyOf(charges);
    }
}
