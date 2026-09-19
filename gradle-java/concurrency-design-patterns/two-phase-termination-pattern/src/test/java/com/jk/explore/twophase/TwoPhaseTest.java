package com.jk.explore.twophase;

import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Test;

import static com.jk.explore.twophase.TwoPhaseDemo.holdMidOrder;
import static com.jk.explore.twophase.TwoPhaseDemo.until;
import static org.junit.jupiter.api.Assertions.*;

class TwoPhaseTest {

    @RepeatedTest(3)
    void closingTheLedgerUnderAWorkerLeavesAnOrderHalfWritten() throws Exception {
        Ledger l = new Ledger();
        Gate g = new Gate();
        Worker w = holdMidOrder(l, g, false);
        l.close();
        g.open();
        assertTrue(w.awaitStop(5000));
        assertTrue(l.leftHalfWritten());
        assertEquals(1, l.lines().size());
    }

    @RepeatedTest(3)
    void aRequestedStopFinishesTheOrderInProgressAndStartsNoOther() throws Exception {
        Ledger l = new Ledger();
        Gate g = new Gate();
        Worker w = holdMidOrder(l, g, true);
        w.submit("ORD-2");
        w.requestStop(false);
        g.open();
        assertTrue(w.awaitStop(5000));
        l.close();
        assertEquals(3, l.lines().size());
        assertFalse(l.leftHalfWritten());
        assertEquals(1, w.finishedOrders());
        assertEquals(1, w.pending());
        assertTrue(w.cleanedUp());
    }

    @Test
    void aFlagAloneDoesNotWakeAWorkerThatIsWaitingForAnOrder() throws Exception {
        Worker w = new Worker(new Ledger(), true);
        w.start();
        until(() -> w.state() == Thread.State.WAITING);
        w.requestStop(false);
        assertFalse(w.awaitStop(150));
        assertEquals(Thread.State.WAITING, w.state());
        w.requestStop(true);
        assertTrue(w.awaitStop(5000));
    }

    @Test
    void cleanupRunsWhenTheWorkerIsInterrupted() throws Exception {
        Worker w = new Worker(new Ledger(), true);
        w.start();
        until(() -> w.state() == Thread.State.WAITING);
        w.requestStop(true);
        w.awaitStop(5000);
        assertTrue(w.cleanedUp());
    }

    @Test
    void aWorkerThatIgnoresTheRequestIsStillAliveAfterTheTimeLimit() throws Exception {
        Ledger l = new Ledger();
        Gate g = new Gate();
        Worker w = holdMidOrder(l, g, true);
        w.requestStop(true);
        assertFalse(w.awaitStop(100));
        assertTrue(w.isAlive());
        g.open();
        assertTrue(w.awaitStop(5000));
    }

    @Test
    void askingTwiceIsHarmless() throws Exception {
        Worker w = new Worker(new Ledger(), true);
        w.start();
        until(() -> w.state() == Thread.State.WAITING);
        w.requestStop(true);
        w.requestStop(true);
        assertTrue(w.awaitStop(5000));
        assertTrue(w.awaitStop(5000));
    }
}
