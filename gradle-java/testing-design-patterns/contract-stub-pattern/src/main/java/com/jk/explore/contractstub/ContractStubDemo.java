package com.jk.explore.contractstub;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: a hand-written stub that drifted, a stub made from the contract, the provider
 * checked against the same contract, a strict stub, and the bill.
 */
public final class ContractStubDemo {

    static final String GOOD = "4000000000000001";
    static final String EMPTY = "4000000000000002";

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. A hand-written stub, and a payment service that moved on.");
        out.add("  checkout test, against the hand-written stub: "
                + new Checkout(new HandWrittenStub()).pay("20.00", GOOD, "GBP"));
        out.add("  in production, payment service version 2: "
                + new Checkout(new RealPaymentService(2)).pay("20.00", GOOD, "GBP"));
        out.add("  version 2 renamed \"result\" to \"outcome\"; the stub never knew, so the tests stayed green");

        out.add("");
        out.add("TWO. A stub made from the shared contract.");
        Contract contract = Contract.payments();
        Checkout tested = new Checkout(new ContractStub(contract));
        out.add("  the contract lists " + contract.interactions().size() + " interactions");
        out.add("  normal card:    " + tested.pay("20.00", GOOD, "GBP"));
        out.add("  card, no funds: " + tested.pay("20.00", EMPTY, "GBP"));
        out.add("  zero amount:    " + tested.pay("0.00", GOOD, "GBP"));

        out.add("");
        out.add("THREE. The payment service is checked against the same contract.");
        List<String> v1 = ProviderVerifier.mismatches(contract, new RealPaymentService(1));
        out.add("  version 1: " + (contract.interactions().size() - v1.size()) + " of "
                + contract.interactions().size() + " interactions match");
        List<String> v2 = ProviderVerifier.mismatches(contract, new RealPaymentService(2));
        out.add("  version 2: " + (contract.interactions().size() - v2.size()) + " of "
                + contract.interactions().size() + " match; the rename fails the payment team's build");
        out.add("  so the stub and the real service can never quietly drift apart");

        out.add("");
        out.add("FOUR. The stub refuses what the contract does not cover.");
        out.add("  hand-written stub, charge in USD: " + new Checkout(new HandWrittenStub()).pay("20.00", GOOD, "USD"));
        try {
            tested.pay("20.00", GOOD, "USD");
        } catch (IllegalStateException e) {
            out.add("  contract stub, charge in USD: " + e.getMessage().replaceAll("\\{.*}", "that request"));
        }
        out.add("  checkout must agree USD with the payment team before relying on it");

        out.add("");
        out.add("FIVE. The bill: the contract is shared work.");
        out.add("  both teams must share and version the contract, and run it in both builds");
        out.add("  and it covers only the listed interactions: not speed, and not the real network");
        return out;
    }

    private ContractStubDemo() {
    }
}
