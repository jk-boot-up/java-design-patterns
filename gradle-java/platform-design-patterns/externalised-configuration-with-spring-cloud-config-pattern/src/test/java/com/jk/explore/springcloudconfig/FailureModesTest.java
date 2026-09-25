package com.jk.explore.springcloudconfig;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.LocalDateTime;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

/** The two bills: a value the range check refuses, and a config server that is not there. */
class FailureModesTest {

    @TempDir
    Path tmp;

    private ConfigRepository repo;
    private ConfigServerProcess server;
    private Shop shop;

    @BeforeEach
    void start() throws IOException {
        Path work = Files.createDirectories(tmp).toRealPath();
        repo = ConfigRepository.createIn(work.resolve("repo"));
        repo.commit("35.00", "4.99", "Maya in marketing", LocalDateTime.of(2025, 3, 7, 16, 30), "Weekend promotion");
        server = ConfigServerProcess.start(repo.uri(), work);
        shop = Shop.start(server.url(), Shop.WhenServerIsDown.REFUSE_TO_START);
    }

    @AfterEach
    void stop() {
        if (shop != null) {
            shop.close();
        }
        server.close();
        repo.close();
    }

    @Test
    void theServerServesMinusOneBecauseItChecksNothing() {
        repo.commit("-1", "4.99", "Maya in marketing", LocalDateTime.of(2025, 3, 8, 9, 12), "typo");
        assertTrue(server.settingsFor("checkout-service", "default").contains("\"delivery.free-over\":-1"));
    }

    @Test
    void aRefusedValueFailsEveryQuoteUntilItIsPutRight() {
        repo.commit("-1", "4.99", "Maya in marketing", LocalDateTime.of(2025, 3, 8, 9, 12), "typo");
        assertEquals(200, shop.refresh().status());
        for (int i = 0; i < 5; i++) {
            assertEquals(500, shop.quote("48.00").status());
        }
        repo.commit("35.00", "4.99", "Sam on call", LocalDateTime.of(2025, 3, 8, 9, 40), "put it back");
        assertEquals(200, shop.refresh().status());
        assertEquals("goods £48.00 delivery FREE threshold £35.00", shop.quote("48.00").body());
    }

    @Test
    void withTheServerGoneTheRunningShopKeepsWhatItHas() {
        server.close();
        assertEquals(500, shop.refresh().status());
        assertEquals("goods £48.00 delivery FREE threshold £35.00", shop.quote("48.00").body());
    }

    @Test
    void withTheServerGoneAShopToldToFailFastRefusesToStart() {
        server.close();
        RuntimeException e = assertThrows(RuntimeException.class,
                () -> Shop.start(server.url(), Shop.WhenServerIsDown.REFUSE_TO_START));
        assertTrue(messages(e).contains("the fail fast property is set"), messages(e));
    }

    @Test
    void withTheServerGoneAnOptionalShopStartsOnItsOwnDefault() {
        server.close();
        try (Shop optional = Shop.start(server.url(), Shop.WhenServerIsDown.START_ON_LOCAL_DEFAULTS)) {
            assertEquals("goods £48.00 delivery £4.99 threshold £50.00", optional.quote("48.00").body());
        }
    }

    private static String messages(Throwable e) {
        StringBuilder all = new StringBuilder();
        for (Throwable t = e; t != null; t = t.getCause()) {
            all.append(t.getMessage()).append('\n');
        }
        return all.toString();
    }
}
