package com.jk.explore.springcloudconfig;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.LocalDateTime;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

/**
 * A real config server process and a real shop: what a commit does, what a refresh does, and
 * what a refresh does not reach. Every process started here is stopped after each test.
 */
class RefreshTest {

    @TempDir
    Path tmp;

    private ConfigRepository repo;
    private ConfigServerProcess server;
    private Shop shop;

    @BeforeEach
    void start() throws IOException {
        Path work = Files.createDirectories(tmp).toRealPath();
        repo = ConfigRepository.createIn(work.resolve("repo"));
        repo.commit("50.00", "4.99", "Priya in engineering", LocalDateTime.of(2025, 3, 3, 10, 0), "Free delivery over 50 pounds");
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

    private void promote() {
        repo.commit("35.00", "4.99", "Maya in marketing", LocalDateTime.of(2025, 3, 7, 16, 30), "Weekend promotion");
    }

    @Test
    void theShopQuotesWithTheValueFetchedAtStartup() {
        assertEquals("goods £48.00 delivery £4.99 threshold £50.00", shop.quote("48.00").body());
    }

    @Test
    void aCommitReachesTheServerAtOnceButNotTheRunningShop() {
        promote();
        assertTrue(server.settingsFor("checkout-service", "default").contains("\"delivery.free-over\":35.0"));
        assertEquals("goods £48.00 delivery £4.99 threshold £50.00", shop.quote("48.00").body());
    }

    @Test
    void aRefreshReportsTheChangedKeysAndTheNextQuoteUsesThem() {
        long startedAt = shop.startedAt();
        promote();
        Http.Reply refresh = shop.refresh();
        assertEquals(200, refresh.status());
        assertTrue(refresh.body().contains("delivery.free-over"), refresh.body());
        assertTrue(refresh.body().contains("config.client.version"), refresh.body());
        assertEquals("goods £48.00 delivery FREE threshold £35.00", shop.quote("48.00").body());
        assertEquals(startedAt, shop.startedAt());
    }

    @Test
    void aRefreshWithNothingCommittedChangesNothing() {
        assertEquals("[]", shop.refresh().body());
    }

    @Test
    void theBannerKeepsTheValueItCopiedAtStartup() {
        promote();
        shop.refresh();
        assertEquals("goods £48.00 delivery FREE threshold £35.00", shop.quote("48.00").body());
        assertEquals("Free delivery on orders over £50.00", shop.banner());
    }

    @Test
    void aRestartIsWhatReachesTheBanner() {
        promote();
        shop.refresh();
        shop.close();
        shop = Shop.start(server.url(), Shop.WhenServerIsDown.REFUSE_TO_START);
        assertEquals("Free delivery on orders over £35.00", shop.banner());
    }
}
