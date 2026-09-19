package com.jk.explore.futurepromise;

import com.jk.explore.futurepromise.harness.Gate;
import com.jk.explore.futurepromise.pattern.UnboundedWait;
import org.junit.jupiter.api.RepeatedTest;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import static org.junit.jupiter.api.Assertions.assertTrue;

class UnboundedWaitTest {

    @RepeatedTest(20)
    void aTaskParkedForeverAlwaysTimesOutRatherThanReturning() {
        ExecutorService pool = Executors.newSingleThreadExecutor();
        try {
            UnboundedWait.Outcome outcome = UnboundedWait.attemptGet(pool, new Gate(), 100);

            assertTrue(outcome.timedOut(),
                    "the gate is never opened in this test, so get() can never succeed");
            assertTrue(outcome.waitedMillis() >= 100,
                    "the rescue timeout is the only thing that ends the wait");
        } finally {
            pool.shutdown();
        }
    }
}
