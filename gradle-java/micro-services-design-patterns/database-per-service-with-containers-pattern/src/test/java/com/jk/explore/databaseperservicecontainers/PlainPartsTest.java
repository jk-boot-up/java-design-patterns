package com.jk.explore.databaseperservicecontainers;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.sql.SQLException;
import org.junit.jupiter.api.Test;

/** The parts that need no database at all. These run on any machine, container runtime or not. */
class PlainPartsTest {

    @Test
    void aRowPrintsInFixedColumns() {
        OrderHistoryRow row = new OrderHistoryRow("ord-101", "SKU-KETTLE", "Stainless Steel Kettle", 1);
        assertEquals("ord-101   SKU-KETTLE   Stainless Steel Kettle       x1", row.printed());
    }

    @Test
    void roundTripsAreCountedNotTimed() {
        RoundTrips trips = new RoundTrips();
        trips.one();
        trips.one();
        assertEquals(2, trips.count());
        trips.reset();
        assertEquals(0, trips.count());
    }

    @Test
    void anErrorFromAnyDriverStillShowsItsCode() {
        SQLException plain = new SQLException("relation \"products\" does not exist", "42P01");
        assertEquals("ERROR 42P01: relation \"products\" does not exist", SqlError.describe(plain));
    }

    @Test
    void withNoRuntimeTheAdviceSaysWhatToDo() {
        assertTrue(Engines.NO_RUNTIME_ADVICE.contains("Start Docker Desktop"));
        assertTrue(Engines.NO_RUNTIME_ADVICE.contains("./gradlew run"));
        assertTrue(Engines.WOULD_NOT_START_ADVICE.contains(Postgres.IMAGE));
        assertTrue(Engines.WOULD_NOT_START_ADVICE.contains(Mongo.IMAGE));
    }

    @Test
    void theImagesArePinnedNotLatest() {
        assertEquals("postgres:18.6-alpine", Postgres.IMAGE);
        assertEquals("mongo:8.3.11-noble", Mongo.IMAGE);
    }
}
