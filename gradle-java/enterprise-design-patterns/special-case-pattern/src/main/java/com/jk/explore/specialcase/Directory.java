package com.jk.explore.specialcase;

import java.util.HashMap;
import java.util.Map;

/**
 * Finds customers. The old lookup returns null when there is nobody; the new one returns a special case.
 */
public final class Directory {

    private final Map<String, RegisteredCustomer> accounts = new HashMap<>();

    public Directory() {
        accounts.put("C-17", new RegisteredCustomer("Priya", 120));
    }

    /** Without the pattern. */
    public RegisteredCustomer findOrNull(String id) {
        return id == null ? null : accounts.get(id);
    }

    /** With the pattern: never null. No id means a guest; an id nobody has any more means an unknown customer. */
    public Customer find(String id) {
        if (id == null) {
            return new SpecialCases.Guest();
        }
        Customer c = accounts.get(id);
        return c != null ? c : new SpecialCases.Unknown(id);
    }
}
