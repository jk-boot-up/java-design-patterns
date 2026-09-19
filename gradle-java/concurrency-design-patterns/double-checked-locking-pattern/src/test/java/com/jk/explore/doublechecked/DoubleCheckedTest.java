package com.jk.explore.doublechecked;

import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Modifier;

import static org.junit.jupiter.api.Assertions.*;

class DoubleCheckedTest {

    @RepeatedTest(10)
    void theUnprotectedVersionBuildsTwoWhenTwoThreadsRace() throws Exception {
        assertEquals(2, DoubleCheckedDemo.race(NaiveLazy::get, NaiveLazy::reset));
    }

    @RepeatedTest(10)
    void theSynchronisedVersionBuildsOne() throws Exception {
        assertEquals(1, DoubleCheckedDemo.race(SynchronisedLazy::get, SynchronisedLazy::reset));
    }

    @RepeatedTest(10)
    void theDoubleCheckedVersionBuildsOne() throws Exception {
        assertEquals(1, DoubleCheckedDemo.race(DoubleCheckedLazy::get, DoubleCheckedLazy::reset));
    }

    @Test
    void theSynchronisedVersionTakesTheLockOnEveryCallAndTheDoubleCheckedOnlyOnce() {
        SynchronisedLazy.reset();
        DoubleCheckedLazy.reset();
        for (int i = 0; i < 500; i++) {
            SynchronisedLazy.get();
            DoubleCheckedLazy.get();
        }
        assertEquals(500, SynchronisedLazy.LOCKS_TAKEN.get());
        assertEquals(1, DoubleCheckedLazy.LOCKS_TAKEN.get());
    }

    @Test
    void theDoubleCheckedFieldMustStayVolatile() throws Exception {
        assertTrue(Modifier.isVolatile(DoubleCheckedLazy.class.getDeclaredField("instance").getModifiers()));
    }

    @Test
    void everyCallGetsTheSameInstance() {
        assertSame(DoubleCheckedLazy.get(), DoubleCheckedLazy.get());
        assertSame(HolderLazy.get(), HolderLazy.get());
        assertSame(SynchronisedLazy.get(), SynchronisedLazy.get());
    }

    @Test
    void theHolderIsShorterThanTheDoubleCheckedVersion() throws Exception {
        java.lang.reflect.Method m = DoubleCheckedDemo.class.getDeclaredMethod("codeLines", String.class);
        m.setAccessible(true);
        int dcl = (int) m.invoke(null, "DoubleCheckedLazy.java");
        int holder = (int) m.invoke(null, "HolderLazy.java");
        assertTrue(holder < dcl);
    }
}
