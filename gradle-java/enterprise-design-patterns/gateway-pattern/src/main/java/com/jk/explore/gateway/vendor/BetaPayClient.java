package com.jk.explore.gateway.vendor;

/** A second provider, with a completely different shape: one string in the form STATUS:REFERENCE. */
public class BetaPayClient {

    public String pay(long pence, String card) {
        return pence > 100000 ? "DECLINED:" : "OK:BP-" + pence;
    }
}
