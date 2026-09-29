package com.jk.explore.asyncreply;

/**
 * Without the pattern: the request waits while the report is built, and the gateway gives up after 3 seconds.
 *
 * <p>The server does not know the caller has gone, so it finishes the work
 * anyway, and nobody receives it.
 */
public final class SyncReportApi {

    public static final long GATEWAY_TIMEOUT_MS = 3000;

    private final Clock clock;
    private final ReportBuilder builder;

    public SyncReportApi(Clock clock, ReportBuilder builder) {
        this.clock = clock;
        this.builder = builder;
    }

    public Response getReport() {
        builder.build();
        clock.advance(ReportBuilder.WORK_MS);
        return ReportBuilder.WORK_MS > GATEWAY_TIMEOUT_MS
                ? Response.of(504, "Gateway Timeout")
                : Response.of(200, "report");
    }
}
