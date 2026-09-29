package com.jk.explore.resequencer;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;

class ResequencerTest {

    @Test
    void releasesInSequenceWhateverTheArrivalOrder() {
        List<Integer> seen = new ArrayList<>();
        Resequencer r = new Resequencer(u -> seen.add(u.seq()), 10);
        ResequencerDemo.ARRIVALS.forEach(r::accept);
        assertEquals(List.of(1, 2, 3, 4, 5), seen);
    }

    @Test
    void holdsUntilTheGapIsFilled() {
        List<Integer> seen = new ArrayList<>();
        Resequencer r = new Resequencer(u -> seen.add(u.seq()), 10);
        r.accept(ResequencerDemo.u("X", 2));
        assertEquals(List.of(), seen);
        assertEquals(1, r.holding("X"));
        r.accept(ResequencerDemo.u("X", 1));
        assertEquals(List.of(1, 2), seen);
    }

    @Test
    void ordersAreIndependent() {
        List<String> seen = new ArrayList<>();
        Resequencer r = new Resequencer(u -> seen.add(u.toString()), 10);
        r.accept(ResequencerDemo.u("A", 1));
        r.accept(ResequencerDemo.u("B", 2));
        r.accept(ResequencerDemo.u("A", 2));
        assertEquals(List.of("A#1 PLACED", "A#2 PAID"), seen);
    }

    @Test
    void skipsAGapWhenTooManyWait() {
        List<Integer> seen = new ArrayList<>();
        Resequencer r = new Resequencer(u -> seen.add(u.seq()), 2);
        r.accept(ResequencerDemo.u("X", 1));
        r.accept(ResequencerDemo.u("X", 3));
        r.accept(ResequencerDemo.u("X", 4));
        assertEquals(List.of(1, 3, 4), seen);
    }
}
