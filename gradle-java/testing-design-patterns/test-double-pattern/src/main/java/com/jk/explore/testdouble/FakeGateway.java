package com.jk.explore.testdouble;

import java.util.HashMap;
import java.util.Map;

/**
 * A fake: a small, working payment provider that keeps its ledger in memory instead of at a bank.
 *
 * <p>It really declines over the card limit and really refunds, so whole
 * journeys (pay, cancel, pay again) can be tested quickly and offline.
 */
public final class FakeGateway implements PaymentGateway {

    private final long cardLimitPence;
    private final Map<String, Long> charges = new HashMap<>();
    private long balancePence;
    private int next = 1;

    public FakeGateway(long cardLimitPence) {
        this.cardLimitPence = cardLimitPence;
    }

    @Override
    public Result charge(String orderId, long pence) {
        if (balancePence + pence > cardLimitPence) {
            return Result.declined("over the card limit");
        }
        String receipt = "fake-" + next++;
        charges.put(receipt, pence);
        balancePence += pence;
        return Result.approved(receipt);
    }

    @Override
    public void refund(String receiptId) {
        Long pence = charges.remove(receiptId);
        if (pence == null) {
            throw new IllegalArgumentException("no such charge: " + receiptId);
        }
        balancePence -= pence;
    }

    /** What the customer currently owes on the card. */
    public long balancePence() {
        return balancePence;
    }
}
