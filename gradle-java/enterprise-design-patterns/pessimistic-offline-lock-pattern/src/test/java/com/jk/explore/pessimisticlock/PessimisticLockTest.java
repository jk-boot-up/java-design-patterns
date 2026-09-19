package com.jk.explore.pessimisticlock;

import org.junit.jupiter.api.Test;

import java.time.Duration;

import static org.junit.jupiter.api.Assertions.*;

class PessimisticLockTest {

    private static final Duration TTL = Duration.ofMinutes(15);
    private final Clock clock = new Clock();
    private final LockManager locks = new LockManager(clock);

    @Test
    void theSecondPersonIsRefusedAndToldWhoHoldsTheLock() {
        locks.acquire("P", "A", TTL);
        LockedBy e = assertThrows(LockedBy.class, () -> locks.acquire("P", "B", TTL));
        assertEquals("A", e.holder());
    }

    @Test
    void theHolderMayAcquireAgain() {
        locks.acquire("P", "A", TTL);
        assertDoesNotThrow(() -> locks.acquire("P", "A", TTL));
    }

    @Test
    void releasingLetsTheNextPersonIn() {
        locks.acquire("P", "A", TTL);
        locks.release("P", "A");
        assertDoesNotThrow(() -> locks.acquire("P", "B", TTL));
    }

    @Test
    void onlyTheHolderCanRelease() {
        locks.acquire("P", "A", TTL);
        locks.release("P", "B");
        assertTrue(locks.holds("P", "A"));
    }

    @Test
    void aLockExpiresAndTheOldHolderCanNoLongerWrite() {
        ProductStore store = new ProductStore(locks);
        locks.acquire("MUG-BLUE", "A", TTL);
        clock.advance(Duration.ofMinutes(15));
        assertDoesNotThrow(() -> locks.acquire("MUG-BLUE", "B", TTL));
        assertThrows(IllegalStateException.class, () -> store.write("MUG-BLUE", "A", new ProductStore.Product("MUG-BLUE", 1, 1)));
    }

    @Test
    void aWriteWithoutTheLockIsRefusedAndWithTheLockAccepted() {
        ProductStore store = new ProductStore(locks);
        assertThrows(IllegalStateException.class, () -> store.write("MUG-BLUE", "A", new ProductStore.Product("MUG-BLUE", 1, 1)));
        locks.acquire("MUG-BLUE", "A", TTL);
        store.write("MUG-BLUE", "A", new ProductStore.Product("MUG-BLUE", 1200, 50));
        assertEquals(1200, store.read("MUG-BLUE").pricePence());
    }

    @Test
    void oppositeOrderAcquisitionDeadlocksAndFixedOrderDoesNot() {
        locks.acquire("MUG-BLUE", "A", TTL);
        locks.acquire("TEA-050", "B", TTL);
        assertThrows(LockedBy.class, () -> locks.acquire("TEA-050", "A", TTL));
        assertThrows(LockedBy.class, () -> locks.acquire("MUG-BLUE", "B", TTL));
        LockManager ordered = new LockManager(new Clock());
        ordered.acquire("MUG-BLUE", "A", TTL);
        ordered.acquire("TEA-050", "A", TTL);
        assertThrows(LockedBy.class, () -> ordered.acquire("MUG-BLUE", "B", TTL));
        assertFalse(ordered.holds("TEA-050", "B"));
    }

    @Test
    void aCoarseLockBlocksUnrelatedWork() {
        locks.acquire("catalogue", "A", TTL);
        assertThrows(LockedBy.class, () -> locks.acquire("catalogue", "B", TTL));
        locks.acquire("MUG-BLUE", "A", TTL);
        assertDoesNotThrow(() -> locks.acquire("TEA-050", "B", TTL));
    }
}
