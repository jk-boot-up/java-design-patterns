package com.jk.explore.objectpool.naive;

import com.jk.explore.objectpool.domain.PaymentConnection;

/** <strong>A new connection for every payment.</strong> Simple, correct, and every payment pays the handshake. */
public class ConnectionPerPayment {

    private final long handshakeMillis;

    public ConnectionPerPayment(long handshakeMillis) {
        this.handshakeMillis = handshakeMillis;
    }

    public String pay(String cardHolder, long pence) {
        return new PaymentConnection(handshakeMillis).charge(cardHolder, pence);
    }
}
