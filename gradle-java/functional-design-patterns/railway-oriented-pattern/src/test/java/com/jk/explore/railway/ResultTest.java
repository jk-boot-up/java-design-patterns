package com.jk.explore.railway;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class ResultTest {

    @Test
    void mapRunsOnSuccess() {
        int v = Result.success(2).map(x -> x * 2).fold(x -> x, f -> -1);
        assertEquals(4, v);
    }

    @Test
    void mapIsSkippedOnFailure() {
        int[] calls = {0};
        Result.<Integer>failure("s", "r").map(x -> ++calls[0]);
        assertEquals(0, calls[0]);
    }

    @Test
    void failureKeepsTheFirstStep() {
        Result<Integer> r = Result.<Integer>failure("first", "boom").flatMap(x -> Result.failure("second", "later"));
        assertEquals("first", r.fold(x -> "", Result.Failure::step));
    }

    @Test
    void recoverLeavesSuccessAlone() {
        int v = Result.success(1).recover(f -> Result.success(2)).fold(x -> x, f -> -1);
        assertEquals(1, v);
    }
}
