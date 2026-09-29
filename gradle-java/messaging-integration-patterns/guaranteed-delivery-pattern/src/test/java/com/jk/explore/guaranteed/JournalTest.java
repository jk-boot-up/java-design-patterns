package com.jk.explore.guaranteed;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.nio.file.Path;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class JournalTest {

    @TempDir
    Path dir;

    @Test
    void messagesSurviveANewJournalOnTheSameFile() {
        Journal a = new Journal(dir.resolve("j"));
        a.send("1", "one");
        a.send("2", "two");
        assertEquals(Map.of("1", "one", "2", "two"), new Journal(dir.resolve("j")).unacknowledged());
    }

    @Test
    void acknowledgedMessagesAreNotReplayed() {
        Journal a = new Journal(dir.resolve("j"));
        a.send("1", "one");
        a.send("2", "two");
        a.acknowledge("1");
        assertEquals(List.of("2"), List.copyOf(new Journal(dir.resolve("j")).unacknowledged().keySet()));
    }

    @Test
    void emptyWhenNothingWasSent() {
        assertEquals(0, new Journal(dir.resolve("none")).unacknowledged().size());
    }

    @Test
    void memoryQueueLosesEverythingWhenReplaced() {
        MemoryQueue q = new MemoryQueue();
        q.send("x");
        q = new MemoryQueue();
        assertEquals(0, q.size());
    }
}
