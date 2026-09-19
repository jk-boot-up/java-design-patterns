package com.jk.explore.loadleveling;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class LoadLevelingTest {

    @Test
    void withNoQueueABurstBeyondCapacityIsRefused() {
        Result r = Sim.direct(Sim.burst(100), 10, 20);
        assertEquals(10, r.processed());
        assertEquals(90, r.rejected());
    }

    @Test
    void aQueueSpreadsTheBurstAndLosesNothing() {
        Result r = Sim.queued(Sim.burst(100), 10, 0, 20, -1);
        assertEquals(100, r.processed());
        assertEquals(0, r.rejected());
        assertEquals(100, r.maxDepth());
        assertEquals(0, r.leftInQueue());
    }

    @Test
    void theCostIsWaiting() {
        Result r = Sim.queued(Sim.burst(100), 10, 0, 20, -1);
        assertEquals(9, r.maxWaitTicks());
        assertEquals(4.5, r.averageWaitTicks(), 0.0001);
    }

    @Test
    void anUnboundedQueueGrowsWhenArrivalsExceedTheWorker() {
        Result r = Sim.queued(Sim.steady(15), 10, 0, 100, -1);
        assertEquals(500, r.leftInQueue());
        assertEquals(0, r.rejected());
    }

    @Test
    void aBoundedQueueRefusesWhatWouldNotFit() {
        Result r = Sim.queued(Sim.steady(15), 10, 50, 100, -1);
        assertTrue(r.leftInQueue() <= 50);
        assertEquals(460, r.rejected());
        assertEquals(r.arrived(), r.processed() + r.rejected() + r.leftInQueue());
    }

    @Test
    void aFasterWorkerShortensTheWait() {
        assertEquals(9, Sim.queued(Sim.burst(100), 10, 0, 40, -1).maxWaitTicks());
        assertEquals(4, Sim.queued(Sim.burst(100), 20, 0, 40, -1).maxWaitTicks());
    }

    @Test
    void anInMemoryQueueLosesWhatWasWaitingWhenItStops() {
        Result r = Sim.queued(Sim.burst(100), 10, 0, 20, 3);
        assertEquals(30, r.processed());
        assertEquals(70, r.lost());
        assertEquals(r.arrived(), r.processed() + r.lost());
    }

    @Test
    void everyOrderIsAccountedForInEveryRun() {
        for (int limit : new int[]{0, 5, 50}) {
            for (int crash : new int[]{-1, 2, 10}) {
                Result r = Sim.queued(Sim.steady(13), 10, limit, 30, crash);
                assertEquals(r.arrived(), r.processed() + r.rejected() + r.lost() + r.leftInQueue(), "limit " + limit + " crash " + crash);
            }
        }
    }
}
