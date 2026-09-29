package com.jk.explore.gatewayoffloading;

/**
 * An HTTP-like response: a status code, a body, and whether the body is gzip-compressed.
 */
public record Response(int status, byte[] body, boolean gzipped) {

    public static Response of(int status, String body) {
        return new Response(status, body.getBytes(), false);
    }

    public String text() {
        return new String(body);
    }
}
