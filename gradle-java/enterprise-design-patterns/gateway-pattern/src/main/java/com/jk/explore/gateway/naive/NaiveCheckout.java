package com.jk.explore.gateway.naive;

import com.jk.explore.gateway.vendor.AcmeClient;

import java.util.HashMap;
import java.util.Map;

/**
 * Checkout, refunds and subscriptions each calling the provider's client directly. Each builds the request
 * fields and each has learnt the result codes for itself.
 */
public class NaiveCheckout {

    private final AcmeClient client;

    public NaiveCheckout(AcmeClient client) {
        this.client = client;
    }

    public String checkout(long pence) {
        Map<String, String> request = new HashMap<>();
        request.put("amt_minor", String.valueOf(pence));
        request.put("ccy", "GBP");
        request.put("pan_token", "tok_ada");
        Map<String, String> r = client.postCharge(request);
        return r.get("rsp_code").equals("00") ? "paid, receipt " + r.get("txn_ref") : "card declined";
    }

    public String renewSubscription(long pence) {
        Map<String, String> request = new HashMap<>();
        request.put("amt_minor", String.valueOf(pence));
        request.put("ccy", "GBP");
        request.put("pan_token", "tok_ada");
        Map<String, String> r = client.postCharge(request);
        return r.get("rsp_code").equals("00") ? "renewed" : "renewal failed";
    }

    public String topUpGiftCard(long pence) {
        Map<String, String> request = new HashMap<>();
        request.put("amt_minor", String.valueOf(pence));
        request.put("pan_token", "tok_ada");
        Map<String, String> r = client.postCharge(request);
        return r.get("rsp_code").equals("00") ? "topped up" : "top-up failed";
    }
}
