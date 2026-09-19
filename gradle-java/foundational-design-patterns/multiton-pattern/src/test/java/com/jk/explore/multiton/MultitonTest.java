package com.jk.explore.multiton;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.concurrent.CyclicBarrier;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class MultitonTest {

    @BeforeEach
    void fresh() {
        Warehouse.resetAll();
    }

    @Test
    void sameRegionSameObjectOtherRegionOtherObject() {
        assertSame(Warehouse.of("UK"), Warehouse.of("UK"));
        assertNotSame(Warehouse.of("UK"), Warehouse.of("EU"));
        assertEquals(2, Warehouse.created());
    }

    @Test
    void stateIsSharedThroughEveryReference() {
        Warehouse.of("UK").reserve(10);
        assertEquals(90, Warehouse.of("UK").stock());
        assertEquals(100, Warehouse.of("EU").stock());
    }

    @Test
    void unknownRegionsAreRefused() {
        assertThrows(IllegalArgumentException.class, () -> Warehouse.of("MARS"));
        assertEquals(0, Warehouse.held());
    }

    @Test
    void unsharedCopiesDisagree() {
        Warehouse a = Warehouse.unshared("UK");
        Warehouse b = Warehouse.unshared("UK");
        a.reserve(10);
        assertEquals(90, a.stock());
        assertEquals(100, b.stock());
    }

    @Test
    void lookThenCreateWithoutALockMakesTwo() throws Exception {
        CyclicBarrier both = new CyclicBarrier(2);
        NaiveWarehouses naive = new NaiveWarehouses(() -> {
            try {
                both.await();
            } catch (Exception e) {
                throw new IllegalStateException(e);
            }
        });
        Warehouse[] got = new Warehouse[2];
        Thread t1 = new Thread(() -> got[0] = naive.of("UK"));
        Thread t2 = new Thread(() -> got[1] = naive.of("UK"));
        t1.start();
        t2.start();
        t1.join();
        t2.join();
        assertNotSame(got[0], got[1]);
        assertEquals(2, Warehouse.created());
    }

    @Test
    void anAtomicCreateGivesOneUnderRace() throws Exception {
        int n = 8;
        Thread[] threads = new Thread[n];
        Warehouse[] got = new Warehouse[n];
        CyclicBarrier start = new CyclicBarrier(n);
        for (int i = 0; i < n; i++) {
            int k = i;
            threads[i] = new Thread(() -> {
                try {
                    start.await();
                } catch (Exception e) {
                    throw new IllegalStateException(e);
                }
                got[k] = Warehouse.of("UK");
            });
            threads[i].start();
        }
        for (Thread t : threads) {
            t.join();
        }
        for (Warehouse w : got) {
            assertSame(got[0], w);
        }
        assertEquals(1, Warehouse.created());
    }
}
