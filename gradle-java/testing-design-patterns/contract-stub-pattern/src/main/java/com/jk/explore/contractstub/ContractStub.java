package com.jk.explore.contractstub;

import java.util.Map;

/**
 * The pattern: a stub made from the contract. It answers exactly the requests the contract lists,
 * with exactly the agreed replies, and refuses anything else.
 */
public final class ContractStub implements PaymentProvider {

    private final Contract contract;

    public ContractStub(Contract contract) {
        this.contract = contract;
    }

    @Override
    public Map<String, String> charge(Map<String, String> request) {
        return contract.interactions().stream()
                .filter(i -> i.request().equals(request))
                .map(Interaction::reply)
                .findFirst()
                .orElseThrow(() -> new IllegalStateException("no interaction in the contract for " + request));
    }
}
