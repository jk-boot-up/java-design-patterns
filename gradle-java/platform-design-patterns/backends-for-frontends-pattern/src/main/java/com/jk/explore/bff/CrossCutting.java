package com.jk.explore.bff;

import java.util.List;

/**
 * The jobs every client's traffic needs done, regardless of which client it is:
 * checking the token, refusing the hundred-and-first request this minute, terminating
 * TLS, writing the access log.
 *
 * <p>These are the jobs that pull a backend for a frontend out of shape. They have to
 * happen, they have to happen the same way everywhere, and the nearest place to put
 * them is inside whichever backend you happen to be editing. Do that once per backend
 * and the shop has as many copies of its authentication code as it has clients, which
 * is the position it was in before it had a gateway.
 *
 * <p>The line this class exists to draw: **a backend for a frontend is about shape, and
 * a gateway is about entry.** If the code answers "what does this screen need?", it
 * belongs in a backend. If it answers "is this request allowed in at all?", it belongs
 * in front of all of them.
 */
public final class CrossCutting {

    /** The jobs themselves. Identical for every client, by definition. */
    public static final List<String> JOBS = List.of(
            "verify the customer's token",
            "refuse traffic over the rate limit",
            "terminate TLS",
            "write the access log");

    private CrossCutting() {
    }

    /** Copies of each job when every backend does it itself. */
    public static int copiesWhenEachBackendDoesIt(int backends) {
        return JOBS.size() * backends;
    }

    /**
     * Copies when a gateway in front does it once and the backends trust it.
     *
     * <p>It takes no argument, and that is the answer: the number does not depend on
     * how many backends there are.
     */
    public static int copiesBehindAGateway() {
        return JOBS.size();
    }
}
