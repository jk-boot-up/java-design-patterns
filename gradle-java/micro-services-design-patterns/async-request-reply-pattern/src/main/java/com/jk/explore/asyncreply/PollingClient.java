package com.jk.explore.asyncreply;

import java.util.ArrayList;
import java.util.List;

/**
 * The caller's side: submit, then check the status link, waiting between checks, until it is sent to the result.
 */
public final class PollingClient {

    private final Clock clock;
    private final AsyncReportApi api;
    private final List<String> trace = new ArrayList<>();

    public PollingClient(Clock clock, AsyncReportApi api) {
        this.clock = clock;
        this.api = api;
    }

    /** Waits the server's retry hint between checks, or {@code everyMs} if that is given (0 = use the hint). */
    public String getReport(String requestKey, long everyMs) {
        Response accepted = api.submit(requestKey);
        trace.add("t=" + clock.now() / 1000.0 + "s  submit: " + accepted);
        Response r = accepted;
        while (r.code() != 303) {
            clock.advance(everyMs > 0 ? everyMs : r.retryAfterMs());
            r = api.status(accepted.location());
            trace.add("t=" + clock.now() / 1000.0 + "s  status: " + r);
        }
        Response report = api.fetch(r.location());
        trace.add("t=" + clock.now() / 1000.0 + "s  fetch:  " + report);
        return report.body();
    }

    public List<String> trace() {
        return List.copyOf(trace);
    }
}
