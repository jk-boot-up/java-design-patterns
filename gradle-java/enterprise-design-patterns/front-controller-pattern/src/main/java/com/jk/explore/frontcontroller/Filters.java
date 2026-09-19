package com.jk.explore.frontcontroller;

import java.util.Set;

public final class Filters {

    private Filters() {
    }

    /** Logs every request and its outcome, including the ones that never reach a handler. */
    public static Filter logging(Journal journal) {
        return (request, next) -> {
            Response response = next.apply(request);
            journal.add(request.method() + " " + request.path() + " -> " + response.status());
            return response;
        };
    }

    /** Refuses anyone without a valid token, except on the public paths. */
    public static Filter authentication(Set<String> publicPaths) {
        return (request, next) -> {
            if (publicPaths.contains(request.path()) || (request.token() != null && request.token().startsWith("t-"))) {
                return next.apply(request);
            }
            return new Response(401, "please sign in");
        };
    }

    /** A filter with a bug in it, to show that everything now depends on the filters. */
    public static Filter buggy() {
        return (request, next) -> {
            throw new IllegalStateException("null pointer in a filter");
        };
    }
}
