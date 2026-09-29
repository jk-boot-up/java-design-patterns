package com.jk.explore.asyncreply;

/**
 * What the server answers: an HTTP status code, an optional link, a retry hint in milliseconds, and a body.
 */
public record Response(int code, String location, long retryAfterMs, String body) {

    static Response of(int code, String body) {
        return new Response(code, null, 0, body);
    }

    @Override
    public String toString() {
        StringBuilder s = new StringBuilder(String.valueOf(code));
        if (location != null) {
            s.append(" -> ").append(location);
        }
        if (retryAfterMs > 0) {
            s.append(", retry after ").append(retryAfterMs / 1000).append(" s");
        }
        if (body != null) {
            s.append(", ").append(body);
        }
        return s.toString();
    }
}
