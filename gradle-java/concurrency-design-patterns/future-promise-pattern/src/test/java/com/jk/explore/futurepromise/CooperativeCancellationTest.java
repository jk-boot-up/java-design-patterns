package com.jk.explore.futurepromise;

import com.jk.explore.futurepromise.pattern.CooperativeCancellation;
import org.junit.jupiter.api.RepeatedTest;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import static org.junit.jupiter.api.Assertions.assertTrue;

class CooperativeCancellationTest {

    @RepeatedTest(20)
    void aTaskThatIgnoresInterruptionRunsToCompletionDespiteBeingCancelled() {
        ExecutorService pool = Executors.newSingleThreadExecutor();
        try {
            CooperativeCancellation.Outcome outcome = CooperativeCancellation.attempt(pool);

            assertTrue(outcome.reportedCancelled(),
                    "cancel(true) on a running task reports true regardless of whether the task stops");
            assertTrue(outcome.taskRanToCompletion(),
                    "a task that catches and ignores every InterruptedException finishes anyway");
        } finally {
            pool.shutdown();
        }
    }
}
