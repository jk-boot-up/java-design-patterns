package com.jk.explore.plugin;

/**
 * What the shop needs from the outside world. The shop's code only ever names these interfaces.
 */
public final class Services {

    public interface PaymentGateway {
        String charge(String orderId, long pence);
    }

    public interface Emailer {
        String send(String to, String subject);
    }

    private Services() {
    }
}
