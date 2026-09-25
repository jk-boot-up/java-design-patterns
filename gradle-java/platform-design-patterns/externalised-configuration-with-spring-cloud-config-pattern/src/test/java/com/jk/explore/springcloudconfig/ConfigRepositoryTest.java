package com.jk.explore.springcloudconfig;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.LocalDateTime;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

/** The git repository on its own: no server, no shop. */
class ConfigRepositoryTest {

    @TempDir
    Path folder;

    @Test
    void theSameCommitsGiveTheSameIdsOnEveryRun() {
        String a;
        String b;
        try (ConfigRepository one = ConfigRepository.createIn(folder.resolve("one"))) {
            a = one.commit("50.00", "4.99", "Priya in engineering", LocalDateTime.of(2025, 3, 3, 10, 0), "Free delivery over 50 pounds");
        }
        try (ConfigRepository two = ConfigRepository.createIn(folder.resolve("two"))) {
            b = two.commit("50.00", "4.99", "Priya in engineering", LocalDateTime.of(2025, 3, 3, 10, 0), "Free delivery over 50 pounds");
        }
        assertEquals(a, b);
        assertEquals("2a6198d", a);
    }

    @Test
    void theFileIsNamedAfterTheApplicationThatReadsIt() throws IOException {
        try (ConfigRepository repo = ConfigRepository.createIn(folder)) {
            repo.commit("35.00", "4.99", "Maya in marketing", LocalDateTime.of(2025, 3, 7, 16, 30), "promotion");
        }
        String yaml = Files.readString(folder.resolve("checkout-service.yml"));
        assertEquals("delivery:\n  free-over: 35.00\n  standard: 4.99\n", yaml);
    }

    @Test
    void theLogIsNewestFirstWithWhoMadeEachChange() {
        try (ConfigRepository repo = ConfigRepository.createIn(folder)) {
            repo.commit("50.00", "4.99", "Priya in engineering", LocalDateTime.of(2025, 3, 3, 10, 0), "first");
            repo.commit("35.00", "4.99", "Maya in marketing", LocalDateTime.of(2025, 3, 7, 16, 30), "second");
            List<String> log = repo.log();
            assertEquals(2, log.size());
            assertTrue(log.get(0).contains("Maya in marketing  second"), log.toString());
            assertTrue(log.get(1).contains("Priya in engineering  first"), log.toString());
        }
    }

    @Test
    void theServerIsGivenAFileAddress() {
        try (ConfigRepository repo = ConfigRepository.createIn(folder)) {
            assertTrue(repo.uri().startsWith("file:"), repo.uri());
        }
    }
}
