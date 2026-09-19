package com.jk.explore.executearound;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

class ExecuteAroundTest {

    @Test
    void handOverLeaksOnFailure() {
        Pool pool = new Pool();
        Connection c = pool.acquire();
        try {
            c.query("x");
            throw new IllegalStateException("boom");
        } catch (IllegalStateException ignored) {
            // the release was after the failing line, so it never ran
        }
        assertEquals(1, pool.stillOpen());
    }

    @Test
    void executeAroundClosesOnSuccessAndOnFailure() {
        Pool pool = new Pool();
        pool.withConnection(c -> c.query("x"));
        assertThrows(IllegalStateException.class, () -> pool.withConnection(c -> {
            throw new IllegalStateException("boom");
        }));
        assertEquals(2, pool.opened());
        assertEquals(0, pool.stillOpen());
    }

    @Test
    void theResultComesOut() {
        Pool pool = new Pool();
        assertEquals("rows for orders", pool.withConnection(c -> c.query("orders")));
    }

    @Test
    void aFailedTransactionIsUndone() {
        Ledger ledger = new Ledger(5000);
        assertThrows(IllegalStateException.class, () -> ledger.inTransaction(l -> {
            l.spend(3000);
            l.spend(3000);
        }));
        assertEquals(5000, ledger.balance());
        ledger.inTransaction(l -> l.spend(3000));
        assertEquals(2000, ledger.balance());
    }

    @Test
    void timingIsRecordedEvenOnFailure() {
        FakeClock clock = new FakeClock();
        Timed t = new Timed(clock);
        t.around(() -> {
            clock.advance(5);
            return 1;
        });
        assertEquals(5, t.lastTicks());
        assertThrows(IllegalStateException.class, () -> t.around(() -> {
            clock.advance(9);
            throw new IllegalStateException("x");
        }));
        assertEquals(9, t.lastTicks());
    }

    @Test
    void aConnectionThatEscapesIsClosed() {
        Pool pool = new Pool();
        Connection escaped = pool.withConnection(c -> c);
        assertThrows(IllegalStateException.class, () -> escaped.query("x"));
    }
}
