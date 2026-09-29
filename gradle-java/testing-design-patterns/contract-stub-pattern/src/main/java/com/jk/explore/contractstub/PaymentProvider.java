package com.jk.explore.contractstub;

import java.util.Map;

/**
 * The payment service as checkout sees it: a request of named fields in, a reply of named fields out,
 * the way a JSON call over HTTP would look.
 */
public interface PaymentProvider {

    Map<String, String> charge(Map<String, String> request);
}
