package com.jk.explore.contractwiremock;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: real WireMock stubs and a real payment service, all over HTTP.
 */
public final class WireMockContractStubDemo {

    static final String GOOD = "4000000000000001";
    static final String EMPTY = "4000000000000002";

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();
        Contract contract = Contract.payments();

        out.add("ONE. A hand-written stub, and a payment service that moved on.");
        try (ContractStub hand = ContractStub.handWritten(); PaymentService v2 = new PaymentService(2)) {
            out.add("  checkout test against the hand-written WireMock stub: " + new Checkout(hand.url()).pay("20.00", GOOD, "GBP"));
            out.add("  in production, payment service version 2: " + new Checkout(v2.url()).pay("20.00", GOOD, "GBP"));
            out.add("  version 2 renamed \"result\" to \"outcome\"; the stub never knew, so the tests stayed green");

            out.add("");
            out.add("TWO. A WireMock stub built from the shared contract file.");
            try (ContractStub stub = ContractStub.fromContract(contract)) {
                Checkout tested = new Checkout(stub.url());
                out.add("  contracts/payments.json lists " + contract.interactions().size() + " interactions");
                out.add("  normal card:    " + tested.pay("20.00", GOOD, "GBP"));
                out.add("  card, no funds: " + tested.pay("20.00", EMPTY, "GBP"));
                out.add("  zero amount:    " + tested.pay("0.00", GOOD, "GBP"));

                out.add("");
                out.add("THREE. The payment service is checked against the same file.");
                try (PaymentService v1 = new PaymentService(1)) {
                    int n = contract.interactions().size();
                    out.add("  version 1: " + (n - ProviderVerifier.mismatches(contract, v1.url()).size()) + " of " + n
                            + " interactions match");
                }
                out.add("  version 2: " + (contract.interactions().size() - ProviderVerifier.mismatches(contract, v2.url()).size())
                        + " of " + contract.interactions().size() + " match; the rename fails the payment team's build");

                out.add("");
                out.add("FOUR. The stub refuses what the contract does not cover.");
                out.add("  hand-written stub, charge in USD: " + new Checkout(hand.url()).pay("20.00", GOOD, "USD"));
                out.add("  contract stub, charge in USD:    " + tested.pay("20.00", GOOD, "USD"));
                out.add("  WireMock also reports the closest stub it had, so the difference is easy to see");
            }
        }

        out.add("");
        out.add("FIVE. The bill: the contract is shared work.");
        out.add("  both teams must share and version contracts/payments.json, and run it in both builds");
        out.add("  it covers only the listed interactions: not speed, and not the real network");
        out.add("  Spring Cloud Contract automates exactly this: it generates these WireMock stubs and the provider tests");
        return out;
    }

    private WireMockContractStubDemo() {
    }
}
