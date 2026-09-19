package com.jk.explore.gateway.vendor;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * The payment provider's own client, as they ship it: stringly typed maps in, stringly typed maps out,
 * and result codes: "00" approved, "51" declined, "91" timed out. Every call is a network call, and is counted.
 * Responses are scripted so that the demo is the same every time.
 */
public class AcmeClient {

    public static final AtomicInteger NETWORK_CALLS = new AtomicInteger();

    private final Queue<String> script = new ArrayDeque<>();
    private final java.util.List<Map<String, String>> requests = new java.util.ArrayList<>();

    public java.util.List<Map<String, String>> requests() {
        return requests;
    }

    public void script(String... codes) {
        script.addAll(java.util.List.of(codes));
    }

    public Map<String, String> postCharge(Map<String, String> request) {
        NETWORK_CALLS.incrementAndGet();
        requests.add(new HashMap<>(request));
        String code = script.isEmpty() ? "00" : script.poll();
        Map<String, String> response = new HashMap<>();
        response.put("rsp_code", code);
        response.put("txn_ref", code.equals("00") ? "AC-" + request.get("amt_minor") : "");
        return response;
    }
}
