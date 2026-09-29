package com.jk.explore.secrets;

import java.util.HashSet;
import java.util.Set;

/**
 * The external card-payment company. It accepts any key it has not been told to cancel.
 */
public final class PaymentProvider {

    private final Set<String> valid = new HashSet<>();

    public void enable(String key) {
        valid.add(key);
    }

    public void cancel(String key) {
        valid.remove(key);
    }

    public String charge(String key, String amount) {
        return valid.contains(key) ? "charged " + amount : "refused: unknown key";
    }
}
