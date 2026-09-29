package com.jk.explore.specialcase;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: null checks, a guest special case, an unknown customer, behaviour instead of type checks, and the bill.
 */
public final class SpecialCaseDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();
        Directory directory = new Directory();

        out.add("ONE. No customer means null, and null checks everywhere.");
        out.add("  " + Checkout.withNullChecks(directory.findOrNull("C-17"), 4000));
        try {
            Checkout.withNullChecks(directory.findOrNull(null), 4000);
        } catch (NullPointerException e) {
            out.add("  a guest checks out: NullPointerException; the points line forgot its check");
        }

        out.add("");
        out.add("TWO. A Guest special case answers every question.");
        out.add("  " + Checkout.run(directory.find("C-17"), 4000));
        out.add("  " + Checkout.run(directory.find(null), 4000));
        out.add("  checkout has no ifs: the guest simply has no discount and no points");

        out.add("");
        out.add("THREE. A second special case: the account no longer exists.");
        Customer former = directory.find("C-99");
        out.add("  order history for an order by C-99: " + Checkout.run(former, 2500));
        out.add("  the report runs, and says who it was: " + former);

        out.add("");
        out.add("FOUR. Ask for behaviour, not for the type.");
        for (String id : new String[] {"C-17", null, "C-99"}) {
            Customer c = directory.find(id);
            out.add("  " + c.name() + ": newsletter " + (c.canReceiveMarketing() ? "yes" : "no"));
        }
        out.add("  no instanceof Guest anywhere; each case answers for itself");

        out.add("");
        out.add("FIVE. The bill: a special case can hide a mistake.");
        out.add("  a mistyped id, \"C-71\": " + directory.find("C-71").name() + ", and checkout carries on");
        out.add("  and every new Customer method must be written for Guest and Unknown too");
        return out;
    }

    static String pounds(long pence) {
        return String.format("£%d.%02d", pence / 100, pence % 100);
    }

    private SpecialCaseDemo() {
    }
}
