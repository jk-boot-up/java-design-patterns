package com.jk.explore.futurepromise;

import com.jk.explore.futurepromise.harness.Gate;
import com.jk.explore.futurepromise.pattern.FutureAndPromise;
import org.junit.jupiter.api.RepeatedTest;

import java.util.concurrent.atomic.AtomicBoolean;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class FutureAndPromiseTest {

    @RepeatedTest(20)
    void theReaderReceivesExactlyWhatTheWriterCompletedTheFutureWith() {
        Gate writerHold = new Gate();
        AtomicBoolean writerRan = new AtomicBoolean(false);

        // handOff blocks the calling (reader) thread inside future.get()
        // until the writer thread -- started inside handOff itself -- calls
        // future.complete(). Parking the writer's own work behind a gate
        // first proves the reader is not merely reading a value that was
        // already sitting there: writerRan can only become true after this
        // test opens the gate, and handOff cannot return before that.
        Thread opener = new Thread(writerHold::open);

        opener.start();
        String result = FutureAndPromise.handOff(() -> {
            writerHold.awaitOpen();
            writerRan.set(true);
            return "£129.99";
        });

        assertEquals("£129.99", result);
        assertTrue(writerRan.get(), "the writer's own work must have run before the reader got a result");
    }
}
