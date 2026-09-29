package com.jk.explore.wiretap;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;

/**
 * The payment service at the end of the channel. The "old" version had logging typed into its charge path only.
 */
public final class PaymentService implements Consumer<PaymentMessage> {

    private final List<String> handled = new ArrayList<>();
    private final List<String> ownLog;

    public PaymentService(List<String> ownLog) {
        this.ownLog = ownLog;
    }

    @Override
    public void accept(PaymentMessage m) {
        if (m.kind().equals("CHARGE")) {
            if (ownLog != null) {
                ownLog.add("payment saw " + m);   // logging added by hand, here only
            }
            handled.add("charged " + m.orderId());
        } else {
            handled.add("refunded " + m.orderId());   // nobody added logging to refunds
        }
    }

    public List<String> handled() {
        return handled;
    }
}
