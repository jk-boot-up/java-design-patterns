package com.jk.explore.pipefilterarch;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class PipeFilterArchTest {

    @Test
    void stagesOverlapSoMoreOrdersFinish() {
        Line big = new Line(new Stage("all", 5, 1, Integer.MAX_VALUE));
        big.run(30);
        Line line = PipeFilterArchDemo.pipeline(1, Integer.MAX_VALUE);
        line.run(30);
        assertTrue(line.out() > big.out());
    }

    @Test
    void theSlowestStageSetsTheRate() {
        Line line = PipeFilterArchDemo.pipeline(1, Integer.MAX_VALUE);
        line.run(60);
        Line more = PipeFilterArchDemo.pipeline(1, Integer.MAX_VALUE);
        more.run(30);
        assertEquals(line.out() - more.out(), 10);
        assertTrue(line.stage("price").queued() > 10);
    }

    @Test
    void wideningTheSlowStageHelps() {
        Line one = PipeFilterArchDemo.pipeline(1, Integer.MAX_VALUE);
        Line three = PipeFilterArchDemo.pipeline(3, Integer.MAX_VALUE);
        one.run(30);
        three.run(30);
        assertTrue(three.out() > one.out());
    }

    @Test
    void aLimitKeepsLinesShortAndOutputTheSame() {
        Line open = PipeFilterArchDemo.pipeline(1, Integer.MAX_VALUE);
        Line limited = PipeFilterArchDemo.pipeline(1, 3);
        open.run(30);
        limited.run(30);
        assertEquals(open.out(), limited.out());
        assertTrue(limited.stage("price").peakQueue() <= 3);
        assertTrue(open.stage("price").peakQueue() > 3);
        assertTrue(limited.refused() > 0);
    }

    @Test
    void aCrashLosesWhatIsInFlight() {
        Line line = PipeFilterArchDemo.pipeline(1, Integer.MAX_VALUE);
        line.run(30);
        int before = line.stage("price").inFlight();
        assertEquals(before, line.stage("price").crash());
        assertEquals(0, line.stage("price").inFlight());
    }
}
