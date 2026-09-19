package com.jk.explore.forkjoin;

import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Test;

import java.util.concurrent.ForkJoinPool;

import static org.junit.jupiter.api.Assertions.*;

class ForkJoinTest {

    @Test
    void theForkJoinSumEqualsTheLoopForAnyThreshold() {
        long[] t = OrderTotals.generate(50_000);
        long expected = OrderTotals.sequentialSum(t);
        for (int threshold : new int[]{1, 7, 100, 10_000, 50_000, 100_000}) {
            SumTask.reset();
            assertEquals(expected, ForkJoinPool.commonPool().invoke(new SumTask(t, 0, t.length, threshold)), "threshold " + threshold);
        }
    }

    @Test
    void theTasksAndLeavesMatchTheShapeWorkedOutWithNoThreads() {
        long[] t = OrderTotals.generate(100_000);
        SumTask.reset();
        ForkJoinPool.commonPool().invoke(new SumTask(t, 0, t.length, 10_000));
        Splitting.Shape s = Splitting.of(100_000, 10_000);
        assertEquals(s.leaves(), SumTask.LEAVES.get());
        assertEquals(s.tasks(), SumTask.TASKS.get());
        assertEquals(16, s.leaves());
        assertEquals(31, s.tasks());
    }

    @Test
    void aTreeOfLeavesHasOneFewerJoinsThanLeaves() {
        for (int threshold : new int[]{1, 10, 1000}) {
            Splitting.Shape s = Splitting.of(5000, threshold);
            assertEquals(2 * s.leaves() - 1, s.tasks());
        }
    }

    @Test
    void anEmptyAndASingleItemSliceAreOneLeaf() {
        assertEquals(new Splitting.Shape(1, 1), Splitting.of(0, 10));
        assertEquals(new Splitting.Shape(1, 1), Splitting.of(1, 1));
    }

    @RepeatedTest(3)
    void aPoolOfFourRunsFourPiecesAtOnce() {
        assertEquals(4, ForkJoinDemo.mostLeavesAtOnce(4, 16, 4));
    }

    @RepeatedTest(3)
    void aPoolOfTwoRunsOnlyTwoEvenWithEightPiecesWaiting() {
        assertEquals(2, ForkJoinDemo.mostLeavesAtOnce(2, 8, 2));
    }

    @Test
    void oneHugePieceCapsTheSpeedup() {
        assertEquals(4.0, Splitting.bestSpeedup(new long[]{25, 25, 25, 25}), 0.0001);
        assertEquals(1.1765, Splitting.bestSpeedup(new long[]{85, 5, 5, 5}), 0.001);
    }
}
