package com.jk.explore.asyncreply;

import java.util.HashMap;
import java.util.Map;

/**
 * The pattern: accept the request at once, hand back a status link, and let the caller come back.
 *
 * <p>Three addresses: submit answers 202 Accepted with a status link; the
 * status link answers "still running" with a retry hint, then 303 See Other
 * pointing at the finished report; and the report link returns the result.
 * The same request key always maps to the same job, so a repeated submit does
 * not start the work twice.
 */
public final class AsyncReportApi {

    public static final long RETRY_AFTER_MS = 2000;

    private record Job(String id, long startedAt, String result) {
    }

    private final Clock clock;
    private final ReportBuilder builder;
    private final Map<String, Job> jobs = new HashMap<>();
    private final Map<String, String> jobOfKey = new HashMap<>();
    private int requests;

    public AsyncReportApi(Clock clock, ReportBuilder builder) {
        this.clock = clock;
        this.builder = builder;
    }

    /** POST /reports */
    public Response submit(String requestKey) {
        requests++;
        String id = jobOfKey.computeIfAbsent(requestKey, k -> {
            String newId = "R-" + (jobs.size() + 1);
            jobs.put(newId, new Job(newId, clock.now(), builder.build()));
            return newId;
        });
        return new Response(202, "/reports/status/" + id, RETRY_AFTER_MS, "Accepted");
    }

    /** GET /reports/status/{id} */
    public Response status(String statusLink) {
        requests++;
        Job job = jobs.get(statusLink.substring(statusLink.lastIndexOf('/') + 1));
        long done = Math.min(100, (clock.now() - job.startedAt()) * 100 / ReportBuilder.WORK_MS);
        if (done < 100) {
            return new Response(200, null, RETRY_AFTER_MS, "running, " + done + "%");
        }
        return new Response(303, "/reports/" + job.id(), 0, "See Other");
    }

    /** GET /reports/{id} */
    public Response fetch(String reportLink) {
        requests++;
        Job job = jobs.get(reportLink.substring(reportLink.lastIndexOf('/') + 1));
        return Response.of(200, job.result());
    }

    public int requests() {
        return requests;
    }
}
