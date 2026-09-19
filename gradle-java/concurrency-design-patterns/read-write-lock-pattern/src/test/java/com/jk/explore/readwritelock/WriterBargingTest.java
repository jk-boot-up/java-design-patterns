package com.jk.explore.readwritelock;

import com.jk.explore.readwritelock.pattern.WriterBarging;
import org.junit.jupiter.api.RepeatedTest;

import java.util.concurrent.locks.ReentrantReadWriteLock;

import static org.junit.jupiter.api.Assertions.assertTrue;

class WriterBargingTest {

    @RepeatedTest(20)
    void aQueuedWriterIsBargedByASecondReadersTryLock() throws InterruptedException {
        ReentrantReadWriteLock lock = new ReentrantReadWriteLock();

        WriterBarging.Outcome outcome = WriterBarging.demonstrate(lock);

        assertTrue(outcome.writerWasQueued(),
                "the writer must be provably parked in the lock's own queue before the barge is attempted");
        assertTrue(outcome.secondReaderBarged(),
                "tryLock() is documented to acquire the read lock regardless of a waiting writer");
    }
}
