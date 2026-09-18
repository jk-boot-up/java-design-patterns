package com.jk.explore.sidecar;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * The arithmetic behind the claim, including the half of it that goes the wrong way.
 */
class ConcernsTest {

    @Test
    @DisplayName("four services carrying four concerns each is sixteen copies")
    void sixteenCopies() {
        assertEquals(16, Concerns.copiesInsideTheServices(4));
    }

    @Test
    @DisplayName("copies grow with the number of services when they are carried inside")
    void copiesGrowWithServices() {
        assertEquals(16, Concerns.copiesInsideTheServices(4));
        assertEquals(20, Concerns.copiesInsideTheServices(5));
        assertEquals(40, Concerns.copiesInsideTheServices(10));
    }

    @Test
    @DisplayName("beside the services the count does not grow, and takes no argument")
    void copiesBesideDoNotGrow() {
        assertEquals(Concerns.CROSS_CUTTING_CONCERNS, Concerns.copiesBesideTheServices());
        assertEquals(4, Concerns.copiesBesideTheServices());
    }

    @Test
    @DisplayName("one policy change is four edits before and one after")
    void oneChangeIsOneEdit() {
        assertEquals(4, Concerns.placesToEditAPolicy(4));
        assertEquals(1, Concerns.placesToEditAPolicyWithSidecars());
    }

    @Test
    @DisplayName("the number of places to edit is also the number of chances to miss one")
    void everyPlaceIsAChanceToMiss() {
        assertEquals(Concerns.placesToEditAPolicy(4), 4);
        assertEquals(3, Concerns.placesToEditAPolicy(4) - 1,
                "three were updated; the fourth is the incident");
    }

    @Test
    @DisplayName("the pattern doubles the number of processes, and says so")
    void processesDouble() {
        assertEquals(4, Concerns.processesToRun(4, false));
        assertEquals(8, Concerns.processesToRun(4, true));
    }

    @Test
    @DisplayName("the four concerns are the four values every service had to decide")
    void fourConcernsMatchTheSettingsRecord() {
        assertEquals(Settings.CONCERNS_PER_SERVICE, Concerns.CROSS_CUTTING_CONCERNS);
        assertEquals(4, Settings.class.getRecordComponents().length);
    }
}
