package com.jk.explore.securegateway;

import java.util.Map;

/**
 * A request as it arrives from the internet: method, path, headers and body size.
 */
public record HttpRequest(String method, String path, Map<String, String> headers, int bodyBytes) {

    public static HttpRequest get(String path) {
        return new HttpRequest("GET", path, Map.of(), 0);
    }
}
