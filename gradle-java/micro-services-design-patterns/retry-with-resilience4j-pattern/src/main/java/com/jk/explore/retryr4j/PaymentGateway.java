package com.jk.explore.retryr4j;

import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * The remote gateway, in memory. It counts every call, records every charge that really
 * happened, and can fail in the three ways a real one does: a timeout before anything
 * happened, a timeout after the charge went through, and a declined card.
 */
@Component
public class PaymentGateway {

    private int calls;
    private int timeoutsBeforeCharge;
    private int timeoutsAfterCharge;
    private boolean declined;
    private final List<Long> charges = new ArrayList<>();
    private final Set<String> seenKeys = new HashSet<>();

    public synchronized void reset() {
        calls = 0;
        timeoutsBeforeCharge = 0;
        timeoutsAfterCharge = 0;
        declined = false;
        charges.clear();
        seenKeys.clear();
    }

    public synchronized void timeOutBeforeCharging(int times) {
        timeoutsBeforeCharge = times;
    }

    public synchronized void timeOutAfterCharging(int times) {
        timeoutsAfterCharge = times;
    }

    public synchronized void declineCards(boolean declined) {
        this.declined = declined;
    }

    public synchronized int calls() {
        return calls;
    }

    public synchronized List<Long> charges() {
        return List.copyOf(charges);
    }

    /** @param idempotencyKey when not null, a second charge with the same key is ignored */
    public synchronized String charge(String idempotencyKey, long pence) {
        calls++;
        if (declined) {
            throw new CardDeclined();
        }
        if (timeoutsBeforeCharge > 0) {
            timeoutsBeforeCharge--;
            throw new GatewayTimeout();
        }
        boolean duplicate = idempotencyKey != null && !seenKeys.add(idempotencyKey);
        if (!duplicate) {
            charges.add(pence);
        }
        if (timeoutsAfterCharge > 0) {
            timeoutsAfterCharge--;
            throw new GatewayTimeout();
        }
        return "R-" + charges.size();
    }
}
