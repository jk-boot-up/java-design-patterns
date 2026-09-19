package com.jk.explore.futurepromise;

import com.jk.explore.futurepromise.pattern.AsyncFailure;
import org.junit.jupiter.api.Test;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AsyncFailureTest {

    @Test
    void theCauseSurvivesButItsStackTraceOmitsTheCallingThreadEntirely() {
        ExecutorService pool = Executors.newSingleThreadExecutor();
        try {
            AsyncFailure.Outcome outcome = AsyncFailure.attempt(pool,
                    () -> { throw new IllegalStateException("catalogue unavailable for ESP-001"); });

            assertEquals("catalogue unavailable for ESP-001", outcome.causeMessage());
            assertTrue(outcome.stackTop().contains("lambda"),
                    "the top frame belongs to the submitted task itself");
            assertTrue(outcome.traceOmits("theCauseSurvivesButItsStackTraceOmitsTheCallingThreadEntirely"),
                    "this test method's own frame -- the calling thread, blocked in get() -- "
                            + "cannot appear in a stack trace captured on a different thread");
        } finally {
            pool.shutdown();
        }
    }
}
