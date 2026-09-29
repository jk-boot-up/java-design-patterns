package com.jk.explore.asyncreply;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class AsyncReportApiTest {

    private final Clock clock = new Clock();
    private final ReportBuilder builder = new ReportBuilder();
    private final AsyncReportApi api = new AsyncReportApi(clock, builder);

    @Test
    void submitAnswersAcceptedWithStatusLink() {
        Response r = api.submit("k");
        assertEquals(202, r.code());
        assertEquals("/reports/status/R-1", r.location());
        assertEquals(2000, r.retryAfterMs());
    }

    @Test
    void statusReportsProgressThenRedirects() {
        String link = api.submit("k").location();
        clock.advance(3000);
        assertEquals("running, 50%", api.status(link).body());
        clock.advance(3000);
        Response done = api.status(link);
        assertEquals(303, done.code());
        assertEquals("/reports/R-1", done.location());
    }

    @Test
    void fetchReturnsTheReport() {
        api.submit("k");
        assertEquals("412 orders, £18240.50", api.fetch("/reports/R-1").body());
    }

    @Test
    void sameKeyDoesNotStartWorkTwice() {
        api.submit("k");
        assertEquals("/reports/status/R-1", api.submit("k").location());
        assertEquals(1, builder.runs());
    }

    @Test
    void differentKeysGetDifferentJobs() {
        api.submit("a");
        assertEquals("/reports/status/R-2", api.submit("b").location());
    }

    @Test
    void syncVersionTimesOutButStillWorks() {
        SyncReportApi sync = new SyncReportApi(clock, builder);
        assertEquals(504, sync.getReport().code());
        assertEquals(1, builder.runs());
    }

    @Test
    void clientFollowsTheHint() {
        PollingClient client = new PollingClient(clock, api);
        assertEquals("412 orders, £18240.50", client.getReport("k", 0));
        assertEquals(6000, clock.now());
        assertEquals(5, api.requests());
    }
}
