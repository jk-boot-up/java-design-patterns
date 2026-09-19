package com.jk.explore.monitorobject;

import com.jk.explore.monitorobject.pattern.MonitorHazards;
import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertTrue;

class MonitorHazardsTest {

    @RepeatedTest(20)
    void oppositeOrderTransfersDeadlockEveryRun() throws InterruptedException {
        MonitorHazards.NestedOutcome outcome = MonitorHazards.nestedMonitors();
        assertTrue(outcome.deadlockDetected(), "the JVM must see the two threads deadlocked");
        assertTrue(outcome.rescued(), "interrupting both must break it");
    }

    @Test
    void callingOutWhileHoldingTheLockCannotComplete() throws InterruptedException {
        assertTrue(MonitorHazards.calloutWhileHoldingLock(200).timedOut());
    }
}
