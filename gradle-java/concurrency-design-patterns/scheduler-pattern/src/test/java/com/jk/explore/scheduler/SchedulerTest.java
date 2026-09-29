package com.jk.explore.scheduler;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import org.junit.jupiter.api.Test;

class SchedulerTest {

    @Test
    void fairLockServesArrivalOrder() throws Exception {
        assertEquals(List.of("STD-1", "STD-2", "STD-3", "EXP-1", "EXP-2", "EXP-3"),
                Printer.run(Printer.fairLock(), SchedulerDemo.MIXED));
    }

    @Test
    void expressFirst() throws Exception {
        assertEquals(List.of("EXP-1", "EXP-2", "EXP-3", "STD-1", "STD-2", "STD-3"),
                Printer.run(Printer.scheduler(new Scheduler(Scheduler.EXPRESS_FIRST)), SchedulerDemo.MIXED));
    }

    @Test
    void smallestFirst() throws Exception {
        assertEquals(List.of("STD-2", "EXP-2", "STD-3", "EXP-3", "EXP-1", "STD-1"),
                Printer.run(Printer.scheduler(new Scheduler(Scheduler.SMALLEST_FIRST)), SchedulerDemo.MIXED));
    }

    @Test
    void ageingStopsStarvation() throws Exception {
        assertEquals(List.of("EXP-1", "EXP-2", "EXP-3", "STD-1", "EXP-4", "EXP-5"),
                Printer.run(Printer.scheduler(new Scheduler(Scheduler.EXPRESS_FIRST, 3)), SchedulerDemo.EXPRESS_RUSH));
    }
}
