package com.jk.explore.externalisedconfig;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** The configuration source: what it stores, what it records, and how it fails. */
class ConfigServerTest {

    private static final LocalDateTime FRIDAY_1630 = LocalDateTime.of(2025, 3, 7, 16, 30);
    private static final String KEY = "delivery.freeOver";

    private final ChangeLog log = new ChangeLog();
    private final ConfigServer server = new ConfigServer(FRIDAY_1630, log);

    @Test
    @DisplayName("a missing key is empty, not an error")
    void aMissingKeyIsEmpty() {
        assertTrue(server.lookup(KEY).isEmpty());
    }

    @Test
    @DisplayName("a value that has been set can be read back as text")
    void aValueCanBeReadBack() {
        server.set(KEY, "35", "marketing");

        assertEquals("35", server.lookup(KEY).orElseThrow());
    }

    @Test
    @DisplayName("the server stores nonsense as happily as sense")
    void theServerDoesNotValidate() {
        server.set(KEY, "fifty", "marketing");
        assertEquals("fifty", server.lookup(KEY).orElseThrow());

        server.set(KEY, "-1", "marketing");
        assertEquals("-1", server.lookup(KEY).orElseThrow());
    }

    @Test
    @DisplayName("every write advances the clock by four seconds and is recorded")
    void everyWriteIsTimedAndRecorded() {
        ConfigChange first = server.set(KEY, "35", "marketing");

        assertEquals(1, first.sequence());
        assertEquals(FRIDAY_1630.plusSeconds(4), first.at());
        assertEquals(ConfigChange.NOT_SET, first.was());
        assertEquals("35", first.now());
        assertEquals("marketing", first.who());
        assertEquals(1, log.size());
    }

    @Test
    @DisplayName("an unreachable server throws rather than pretending the key is missing")
    void anUnreachableServerThrows() {
        server.set(KEY, "35", "marketing");
        server.goOffline("the network link to it dropped");

        assertTrue(server.isOffline());
        ConfigSourceUnavailableException thrown = assertThrows(
                ConfigSourceUnavailableException.class, () -> server.lookup(KEY));
        assertTrue(thrown.getMessage().contains("network link"));

        server.comeBackOnline();
        assertFalse(server.isOffline());
        assertEquals("35", server.lookup(KEY).orElseThrow());
    }

    @Test
    @DisplayName("a rollback puts the previous value back, and is itself a recorded change")
    void aRollbackGoesBackOneStep() {
        server.set(KEY, "35", "marketing");
        server.set(KEY, "-1", "ops");

        ConfigChange rollback = server.rollback(KEY, "on-call").orElseThrow();

        assertEquals("35", server.lookup(KEY).orElseThrow());
        assertEquals("-1", rollback.was());
        assertEquals("on-call (rollback)", rollback.who());
        assertEquals(3, log.size());
    }

    @Test
    @DisplayName("there is nothing to roll back to before the first change")
    void nothingToRollBackTo() {
        assertTrue(server.rollback(KEY, "on-call").isEmpty());

        server.set(KEY, "35", "marketing");
        assertTrue(server.rollback(KEY, "on-call").isEmpty());
    }

    @Test
    @DisplayName("fast-forwarding the clock never moves it backwards")
    void theClockOnlyGoesForward() {
        server.fastForwardTo(FRIDAY_1630.minusHours(5));

        assertEquals(FRIDAY_1630, server.now());
    }
}
