package com.jk.explore.servicestub;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/**
 * Asks the stub and the real service the same questions and lists where they disagree. Run it weekly, not in every test.
 */
public final class ContractCheck {

    public static List<String> differences(AddressGateway stub, AddressGateway real, List<String> postcodes) {
        List<String> diffs = new ArrayList<>();
        for (String p : postcodes) {
            String s = answer(stub, p);
            String r = answer(real, p);
            if (!s.equals(r)) {
                diffs.add("\"" + p + "\": stub says " + s + ", real says " + r);
            }
        }
        return diffs;
    }

    private static String answer(AddressGateway g, String postcode) {
        try {
            Optional<String> a = g.lookup(postcode);
            return a.map(x -> "found").orElse("unknown");
        } catch (RuntimeException e) {
            return "error";
        }
    }

    private ContractCheck() {
    }
}
