package com.jk.explore.externalisedconfig;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The audit trail, which is what takes over from version control once the value
 * no longer lives in the source.
 */
class ChangeLogTest {

    private static final LocalDateTime SATURDAY = LocalDateTime.of(2025, 3, 8, 9, 12);

    private final ChangeLog log = new ChangeLog();

    @Test
    @DisplayName("changes are numbered from one, in the order they happened")
    void changesAreNumberedInOrder() {
        log.record(SATURDAY, "delivery.freeOver", ConfigChange.NOT_SET, "35", "marketing");
        log.record(SATURDAY.plusMinutes(8), "delivery.freeOver", "35", "-1", "ops");

        List<ConfigChange> changes = log.changes();
        assertEquals(2, changes.size());
        assertEquals(1, changes.get(0).sequence());
        assertEquals(2, changes.get(1).sequence());
        assertEquals(2, log.size());
    }

    @Test
    @DisplayName("the log can be filtered to one key")
    void theLogCanBeFilteredToOneKey() {
        log.record(SATURDAY, "delivery.freeOver", ConfigChange.NOT_SET, "35", "marketing");
        log.record(SATURDAY, "catalog.pageSize", ConfigChange.NOT_SET, "24", "web");
        log.record(SATURDAY, "delivery.freeOver", "35", "-1", "ops");

        assertEquals(2, log.changesTo("delivery.freeOver").size());
        assertEquals(1, log.changesTo("catalog.pageSize").size());
        assertTrue(log.changesTo("nothing.at.all").isEmpty());
    }

    @Test
    @DisplayName("the previous value is what makes a rollback a lookup rather than a memory")
    void thePreviousValueIsAvailable() {
        log.record(SATURDAY, "delivery.freeOver", ConfigChange.NOT_SET, "35", "marketing");
        log.record(SATURDAY.plusMinutes(8), "delivery.freeOver", "35", "-1", "ops");

        assertEquals("35", log.valueBefore("delivery.freeOver").orElseThrow());
    }

    @Test
    @DisplayName("a key set for the first time has nothing to go back to")
    void aFirstSettingHasNoPreviousValue() {
        log.record(SATURDAY, "delivery.freeOver", ConfigChange.NOT_SET, "35", "marketing");

        assertTrue(log.valueBefore("delivery.freeOver").isEmpty());
        assertTrue(log.valueBefore("never.touched").isEmpty());
    }

    @Test
    @DisplayName("the log is append-only, so a bad change cannot be tidied away")
    void theLogCannotBeEdited() {
        log.record(SATURDAY, "delivery.freeOver", "35", "-1", "ops");

        assertThrows(UnsupportedOperationException.class, () -> log.changes().clear());
    }

    @Test
    @DisplayName("each line names the key, both values, the time and the person")
    void eachLineIsReadable() {
        String line = log.record(SATURDAY, "delivery.freeOver", "35", "-1", "ops").asLine();

        assertTrue(line.contains("delivery.freeOver"));
        assertTrue(line.contains("35"));
        assertTrue(line.contains("-1"));
        assertTrue(line.contains("Sat 08 Mar 09:12:00"));
        assertTrue(line.contains("by ops"));
    }
}
