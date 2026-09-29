package com.jk.explore.modularmonolith.payments;

import com.jk.explore.modularmonolith.payments.internal.PaymentsModule;

/**
 * The payments module's front door: take a payment, or ask what was taken.
 */
public interface PaymentsApi {

    /** Returns a payment reference. */
    String charge(String orderId, long pence);

    long takenFor(String orderId);

    static PaymentsApi create() {
        return new PaymentsModule();
    }
}
