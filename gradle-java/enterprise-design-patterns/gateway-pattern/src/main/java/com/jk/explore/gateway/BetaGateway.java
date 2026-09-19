package com.jk.explore.gateway;

import com.jk.explore.gateway.vendor.BetaPayClient;

/** The same door, in front of a different provider. */
public class BetaGateway implements PaymentGateway {

    private final BetaPayClient client;

    public BetaGateway(BetaPayClient client) {
        this.client = client;
    }

    @Override
    public PaymentResult charge(long pence, String card) {
        String[] parts = client.pay(pence, card).split(":", 2);
        return parts[0].equals("OK")
                ? new PaymentResult(PaymentStatus.APPROVED, parts[1])
                : new PaymentResult(PaymentStatus.DECLINED, null);
    }
}
