package com.jk.explore.stranglerfignginx;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.util.concurrent.CompletableFuture;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

/**
 * What the real NGINX does, asked of it directly.
 *
 * <p>One NGINX is started for the whole class, because starting it is the slow part, and every
 * test begins by reloading it with every route on the old shop. Every wait here is a bounded
 * poll on something that can actually be asked: whether NGINX answers with the new
 * configuration, whether a request has arrived, whether an old worker has exited. There is no
 * sleep anywhere in this file.
 */
class RealNginxTest {

    private static OldShop old;
    private static NewService fresh;
    private static NginxRouter nginx;

    @BeforeAll
    static void startEverything() {
        assumeTrue(NginxRouter.containerRuntimeAvailable(), "needs a container runtime");
        old = OldShop.start();
        fresh = NewService.start();
        nginx = new NginxRouter(old.port(), fresh.port());
        nginx.start();
    }

    @AfterAll
    static void stopEverything() {
        if (nginx != null) {
            nginx.close();
        }
        if (fresh != null) {
            fresh.close();
        }
        if (old != null) {
            old.close();
        }
    }

    @BeforeEach
    void everyRouteBackOnTheOldShop() {
        fresh.startAgain();
        nginx.apply(NginxConfig.everythingOnTheOldShop());
    }

    private Browser customer() {
        return new Browser(nginx.address());
    }

    @Test
    void itIsTheNginxVersionThisProjectPins() {
        assertEquals("1.31.6", nginx.version());
        assertTrue(NginxRouter.IMAGE.startsWith("nginx:" + nginx.version()));
    }

    @Test
    void theBigBangLeavesOnlyTheRoutesTheNewServiceHasBuilt() {
        assertEquals("prices 200, stock 200, basket 200, orders 200. pages that work: 4 of 4 (4 from the old shop, 0 from the new service)",
                StranglerFigNginxDemo.describePages(customer()));
        nginx.apply(NginxConfig.bigBang());
        assertEquals("prices 200, stock 404, basket 404, orders 404. pages that work: 1 of 4 (0 from the old shop, 1 from the new service)",
                StranglerFigNginxDemo.describePages(customer()));
    }

    @Test
    void movingOneRouteLeavesEveryOtherRouteOnTheOldShop() {
        nginx.apply(NginxConfig.everythingOnTheOldShop().move("/api/prices/"));
        assertTrue(customer().get("/api/prices/SKU-1").fromNewService());
        assertTrue(customer().get("/api/stock/SKU-1").fromOldShop());
        assertTrue(customer().get("/api/basket").fromOldShop());
        assertTrue(customer().get("/api/orders/1001").fromOldShop());
    }

    @Test
    void aReloadKeepsTheMainProcessAndLetsAnOpenRequestFinishOnTheOldConfiguration() {
        int mainBefore = nginx.mainProcessId();
        old.holdTheNextPriceRequest();
        CompletableFuture<Answer> open = CompletableFuture.supplyAsync(() -> customer().get("/api/prices/SKU-1"));
        Poll.until("the open request to reach the old shop", old::heldRequestArrived);

        nginx.apply(NginxConfig.everythingOnTheOldShop().move("/api/prices/"));

        assertEquals(mainBefore, nginx.mainProcessId());
        assertEquals(1, nginx.workersStillFinishing());
        assertEquals(1, nginx.workersTakingNewRequests());
        assertTrue(customer().get("/api/prices/SKU-1").fromNewService());
        assertFalse(open.isDone());

        old.releaseHeldRequest();
        Answer finished = open.join();
        assertEquals(200, finished.status());
        assertTrue(finished.fromOldShop());
        Poll.until("the old worker to exit", () -> nginx.workersStillFinishing() == 0);
    }

    @Test
    void anOldRegularExpressionRuleBeatsTheLongerPrefix() {
        nginx.apply(NginxConfig.everythingOnTheOldShop().withLegacyCacheRule().move("/api/prices/"));
        assertEquals("10 price requests: 10 from the old shop, 0 from the new service",
                StranglerFigNginxDemo.tenPriceRequests(customer()));
        assertEquals("max-age=60", customer().headerOf("/api/prices/SKU-1", "Cache-Control"));
    }

    @Test
    void theCaretTildeStopsNginxLookingAtRegularExpressions() {
        nginx.apply(NginxConfig.everythingOnTheOldShop().withLegacyCacheRule().moveAndStopLooking("/api/prices/"));
        assertEquals("10 price requests: 0 from the old shop, 10 from the new service",
                StranglerFigNginxDemo.tenPriceRequests(customer()));
        // stock was never moved, and the old rule still catches it
        assertEquals("max-age=60", customer().headerOf("/api/stock/SKU-1", "Cache-Control"));
    }

    @Test
    void aSlashAfterTheAddressCutsTheMatchedPrefixOffThePath() {
        nginx.apply(NginxConfig.everythingOnTheOldShop().moveAndStopLooking("/api/prices/"));
        assertEquals(200, customer().get("/api/prices/SKU-1").status());
        assertEquals("/api/prices/SKU-1", fresh.lastPathReceived());

        nginx.apply(NginxConfig.everythingOnTheOldShop().moveWithTrailingSlash("/api/prices/"));
        assertEquals(404, customer().get("/api/prices/SKU-1").status());
        assertEquals("/SKU-1", fresh.lastPathReceived());
    }

    @Test
    void aNewServiceThatIsDownGives502OnlyOnTheRouteThatMoved() {
        nginx.apply(NginxConfig.everythingOnTheOldShop().moveAndStopLooking("/api/prices/"));
        fresh.stop();
        Answer price = customer().get("/api/prices/SKU-1");
        assertEquals(502, price.status());
        assertEquals("nginx", price.servedBy());
        assertEquals(200, customer().get("/api/stock/SKU-1").status());

        nginx.apply(NginxConfig.everythingOnTheOldShop());
        Answer rolledBack = customer().get("/api/prices/SKU-1");
        assertEquals(200, rolledBack.status());
        assertTrue(rolledBack.fromOldShop());
    }

    @Test
    void theOldShopsCookieReachesTheNewServiceAndMeansNothingThere() {
        Browser shopper = customer();
        shopper.post("/api/basket/items?sku=SKU-1");
        shopper.post("/api/basket/items?sku=SKU-2");
        shopper.post("/api/basket/items?sku=SKU-3");
        nginx.apply(NginxConfig.everythingOnTheOldShop().moveAndStopLooking("/api/checkout"));
        Answer onNew = shopper.post("/api/checkout");
        assertEquals(422, onNew.status());
        assertTrue(fresh.lastCookieReceived().startsWith("LEGACYSESSION=L-"));

        nginx.apply(NginxConfig.everythingOnTheOldShop());
        Answer onOld = shopper.post("/api/checkout");
        assertEquals(200, onOld.status());
        assertTrue(onOld.body().endsWith("placed: 3 items, 4249 pence"), onOld.body());
    }
}
