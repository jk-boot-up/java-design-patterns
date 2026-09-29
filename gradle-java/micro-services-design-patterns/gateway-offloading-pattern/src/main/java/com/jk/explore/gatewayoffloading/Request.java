package com.jk.explore.gatewayoffloading;

import java.util.HashMap;
import java.util.Map;

/**
 * An HTTP-like request: a path and its headers.
 */
public record Request(String path, Map<String, String> headers) {

    public static Request of(String path, String... headerPairs) {
        Map<String, String> headers = new HashMap<>();
        for (int i = 0; i < headerPairs.length; i += 2) {
            headers.put(headerPairs[i], headerPairs[i + 1]);
        }
        return new Request(path, headers);
    }

    public String header(String name) {
        return headers.get(name);
    }

    public Request with(String name, String value) {
        Map<String, String> copy = new HashMap<>(headers);
        copy.put(name, value);
        return new Request(path, copy);
    }
}
