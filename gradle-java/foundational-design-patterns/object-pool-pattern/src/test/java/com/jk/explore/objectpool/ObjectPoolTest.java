package com.jk.explore.objectpool;

import com.jk.explore.objectpool.bench.SmallObjectBenchmark;
import com.jk.explore.objectpool.domain.PaymentConnection;
import com.jk.explore.objectpool.naive.ConnectionPerPayment;
import com.jk.explore.objectpool.pattern.ConnectionPool;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** No test here asserts a timing. Counts and states only. */
class ObjectPoolTest {

    @BeforeEach
    void resetCounter() {
        PaymentConnection.resetCounter();
    }

    @Test
    void aNewConnectionPerPaymentOpensOneEachTime() {
        ConnectionPerPayment naive = new ConnectionPerPayment(0);
        for (int i = 0; i < 10; i++) {
            naive.pay("c" + i, 100);
        }
        assertEquals(10, PaymentConnection.openedSoFar());
    }

    @Test
    void aPoolOpensItsConnectionsOnceAndReusesThem() throws InterruptedException {
        ConnectionPool pool = new ConnectionPool(2, 0, true);
        for (int i = 0; i < 10; i++) {
            PaymentConnection c = pool.borrow();
            c.charge("c" + i, 100);
            pool.giveBack(c);
        }
        assertEquals(2, PaymentConnection.openedSoFar());
        assertEquals(2, pool.idleCount());
    }

    @Test
    void aBorrowedConnectionIsTheSameObjectOnceReturned() throws InterruptedException {
        ConnectionPool pool = new ConnectionPool(1, 0, true);
        PaymentConnection first = pool.borrow();
        pool.giveBack(first);
        assertSame(first, pool.borrow());
    }

    @Test
    void aPoolWithNoResetHandsTheNextBorrowerThePreviousCustomersData() throws InterruptedException {
        ConnectionPool careless = new ConnectionPool(1, 0, false);
        PaymentConnection c = careless.borrow();
        c.charge("Ada Lovelace", 5_000);
        careless.giveBack(c);
        assertEquals("Ada Lovelace", careless.borrow().lastCardHolder());
    }

    @Test
    void resettingOnReturnClearsThePreviousCustomersData() throws InterruptedException {
        ConnectionPool safe = new ConnectionPool(1, 0, true);
        PaymentConnection c = safe.borrow();
        c.charge("Ada Lovelace", 5_000);
        safe.giveBack(c);
        assertNull(safe.borrow().lastCardHolder());
    }

    @Test
    void aLeakedConnectionExhaustsThePoolAndTheNextBorrowerCanOnlyTimeOut() throws InterruptedException {
        ConnectionPool pool = new ConnectionPool(2, 0, true);
        pool.borrow();
        pool.borrow();
        assertEquals(0, pool.idleCount());
        assertNull(pool.borrow(100), "nothing to give: without a timeout this would wait forever");
    }

    @Test
    void aPoolOfFiftyOpensFiftyConnectionsWhateverIsUsed() throws InterruptedException {
        ConnectionPool pool = new ConnectionPool(50, 0, true);
        PaymentConnection c = pool.borrow();
        assertNotNull(c);
        assertEquals(50, PaymentConnection.openedSoFar());
        assertEquals(49, pool.idleCount());
    }

    @Test
    void theBenchmarkReportsPositiveTimesForAllThreeVariants() {
        SmallObjectBenchmark.Result r = SmallObjectBenchmark.run(200_000, 1, 3);
        assertTrue(r.allocateNanosPerOp() > 0);
        assertTrue(r.allocateEscapingNanosPerOp() > 0);
        assertTrue(r.poolNanosPerOp() > 0);
    }

    @Test
    void theBenchmarkCountsTheObjectsEachVariantCreates() {
        assertEquals(1_000, SmallObjectBenchmark.objectsCreatedByAllocating(1_000));
        assertEquals(4, SmallObjectBenchmark.objectsCreatedByPooling());
        assertNotSame(SmallObjectBenchmark.objectsCreatedByAllocating(1_000), SmallObjectBenchmark.objectsCreatedByPooling());
    }
}
