package com.jk.explore.servicestub;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: developing against the real service, the stub, edge cases on demand, the contract check, and the bill.
 */
public final class ServiceStubDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. Developing against the real postcode service.");
        PostcodeService real = new PostcodeService();
        for (int i = 0; i < 50; i++) {
            Checkout.address(real, "LS1 4AP");
        }
        out.add("  a day of 50 test checkouts: " + pounds(real.spentPence()) + " in lookups, "
                + real.waitedMs() / 1000 + " s of waiting");
        real.setOnline(false);
        out.add("  on a train with no signal: " + Checkout.address(real, "LS1 4AP"));

        out.add("");
        out.add("TWO. A service stub: the same interface, in memory.");
        PostcodeStub stub = new PostcodeStub();
        out.add("  " + Checkout.address(stub, "LS1 4AP"));
        for (int i = 0; i < 49; i++) {
            Checkout.address(stub, "LS1 4AP");
        }
        out.add("  50 checkouts: " + stub.lookups() + " lookups, £0.00, no network, no waiting");

        out.add("");
        out.add("THREE. The stub plays the awkward cases on demand.");
        out.add("  unknown postcode: " + Checkout.address(stub, "ZZ9 9ZZ"));
        out.add("  service down:     " + Checkout.address(new PostcodeStub().goDown(), "LS1 4AP"));
        out.add("  neither can be ordered from the real service when you need to test it");

        out.add("");
        out.add("FOUR. A contract check: ask both the same questions, weekly.");
        PostcodeService realAgain = new PostcodeService();
        List<String> diffs = ContractCheck.differences(new PostcodeStub(), realAgain,
                List.of("LS1 4AP", "ZZ9 9ZZ", "ls1 4ap"));
        diffs.forEach(d -> out.add("  " + d));
        out.add("  the stub accepts small letters; the real service refuses them");
        out.add("  checkout code tested only against the stub would have broken in production");

        out.add("");
        out.add("FIVE. The bill: a stub is a second, simpler copy of someone else's service.");
        out.add("  it must be kept in step, and it only knows the postcodes you gave it");
        return out;
    }

    static String pounds(long pence) {
        return String.format("£%d.%02d", pence / 100, pence % 100);
    }

    private ServiceStubDemo() {
    }
}
