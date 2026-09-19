package com.jk.explore.readwritelock;

import com.jk.explore.readwritelock.pattern.UpgradeDeadlock;
import org.junit.jupiter.api.RepeatedTest;

import java.util.concurrent.locks.ReentrantReadWriteLock;

import static org.junit.jupiter.api.Assertions.assertTrue;

class UpgradeDeadlockTest {

    @RepeatedTest(20)
    void upgradingFromReadToWriteAlwaysDeadlocksAgainstItself() throws InterruptedException {
        ReentrantReadWriteLock lock = new ReentrantReadWriteLock();

        UpgradeDeadlock.Outcome outcome = UpgradeDeadlock.attemptUpgrade(lock, 100);

        assertTrue(outcome.deadlocked(),
                "a thread already holding the read lock can never be granted the write lock");
        assertTrue(outcome.waitedMillis() >= 100,
                "the rescue timeout is the only thing that ends the wait");
    }
}
