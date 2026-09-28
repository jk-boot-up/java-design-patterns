package com.jk.explore.stranglerfignginx;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;

/**
 * Six acts against a real NGINX, started and stopped by this program.
 *
 * <p>The shop is being rebuilt. The old shop does everything; the new service has so far built
 * prices and checkout. NGINX stands in front of both as the shop's one public address, and
 * moves one route at a time from the old shop to the new service, while the old shop keeps
 * serving the rest.
 */
public class StranglerFigNginxDemo {

    /** The four pages every act checks: one address per route, and a short name for each. */
    static final String[][] PAGES = {
            {"prices", "/api/prices/SKU-1"},
            {"stock", "/api/stock/SKU-1"},
            {"basket", "/api/basket"},
            {"orders", "/api/orders/1001"},
    };

    static final int TEN = 10;

    public static void main(String[] args) {
        if (!NginxRouter.containerRuntimeAvailable()) {
            System.out.println(NginxRouter.NO_RUNTIME_ADVICE);
            return;
        }
        try (OldShop old = OldShop.start();
             NewService fresh = NewService.start();
             NginxRouter nginx = new NginxRouter(old.port(), fresh.port())) {
            try {
                nginx.start();
            } catch (RuntimeException e) {
                System.out.println(NginxRouter.WOULD_NOT_START_ADVICE);
                return;
            }
            Browser customer = new Browser(nginx.address());
            one(nginx, customer);
            two(nginx, customer, old);
            three(nginx, customer);
            four(nginx, customer, fresh);
            five(nginx, customer, fresh);
            six(nginx, old, fresh);
        }
    }

    /** Every route to the old shop, and then every route to the new service at once. */
    private static void one(NginxRouter nginx, Browser customer) {
        System.out.println("ONE. The big bang.");
        System.out.println("  NGINX " + nginx.version() + " is running in a container, in front of the old shop. every route goes to the old shop.");
        System.out.println("  the shop's four pages: " + describePages(customer) + ".");
        nginx.apply(NginxConfig.bigBang());
        System.out.println("  Monday: one line sends every route to the new service, which has built only prices and checkout so far.");
        System.out.println("  the four pages: " + describePages(customer) + ".");
        nginx.apply(NginxConfig.everythingOnTheOldShop());
    }

    /** One route moves, with a reload, while a request on the old shop is still open. */
    private static void two(NginxRouter nginx, Browser customer, OldShop old) {
        System.out.println("TWO. One route at a time.");
        old.holdTheNextPriceRequest();
        Browser early = new Browser(nginx.address());
        CompletableFuture<Answer> open = CompletableFuture.supplyAsync(() -> early.get("/api/prices/SKU-1"));
        Poll.until("the open price request to reach the old shop", old::heldRequestArrived);
        System.out.println("  a customer's price request has reached the old shop, and the old shop is slow to answer it.");
        int mainBefore = nginx.mainProcessId();
        nginx.apply(NginxConfig.everythingOnTheOldShop().move("/api/prices/"));
        int mainAfter = nginx.mainProcessId();
        System.out.println("  the configuration gains location /api/prices/, sent to the new service. nginx -s reload.");
        System.out.println("  NGINX's main process: number " + mainBefore + " before the reload and number " + mainAfter + " after. nothing restarted.");
        Answer next = customer.get("/api/prices/SKU-1");
        System.out.println("  while that request is still open: workers still finishing old requests: " + nginx.workersStillFinishing()
                + ". workers taking new requests: " + nginx.workersTakingNewRequests() + ".");
        System.out.println("  a new price request: " + next.status() + ", from the " + who(next) + ".");
        old.releaseHeldRequest();
        Answer finished = open.join();
        Poll.until("the old worker to finish and exit", () -> nginx.workersStillFinishing() == 0);
        System.out.println("  the open request then finishes: " + finished.status() + ", from the " + who(finished)
                + ". workers still finishing old requests: " + nginx.workersStillFinishing() + ".");
        System.out.println("  the four pages now: " + describePages(customer) + ".");
    }

    /** An old regular-expression rule quietly keeps the moved route on the old shop. */
    private static void three(NginxRouter nginx, Browser customer) {
        System.out.println("THREE. A regular expression wins.");
        System.out.println("  the shop's real configuration has one more rule, written years ago to cache catalogue reads: " + NginxConfig.LEGACY_CACHE_RULE);
        NginxConfig moved = NginxConfig.everythingOnTheOldShop().withLegacyCacheRule().move("/api/prices/");
        nginx.apply(moved);
        System.out.println("  the same move, location /api/prices/, in that configuration, and a reload. " + tenPriceRequests(customer) + ".");
        System.out.println("  NGINX tries its regular-expression rules after finding the longest prefix, and the first one that matches wins. the move did nothing, and nothing said so.");
        NginxConfig fixed = NginxConfig.everythingOnTheOldShop().withLegacyCacheRule().moveAndStopLooking("/api/prices/");
        nginx.apply(fixed);
        System.out.println("  written as location ^~ /api/prices/, which tells NGINX to stop looking: " + tenPriceRequests(customer) + ".");
    }

    /** One slash after the new service's address changes the path it receives. */
    private static void four(NginxRouter nginx, Browser customer, NewService fresh) {
        System.out.println("FOUR. One slash.");
        NginxConfig without = NginxConfig.everythingOnTheOldShop().withLegacyCacheRule().moveAndStopLooking("/api/prices/");
        nginx.apply(without);
        Answer a = customer.get("/api/prices/SKU-1");
        System.out.println("  " + without.moves().get(0).proxyPassLine() + " the new service is asked for " + fresh.lastPathReceived() + " and answers " + a.status() + ".");
        NginxConfig with = NginxConfig.everythingOnTheOldShop().withLegacyCacheRule().moveWithTrailingSlash("/api/prices/");
        nginx.apply(with);
        Answer b = customer.get("/api/prices/SKU-1");
        System.out.println("  " + with.moves().get(0).proxyPassLine() + " the new service is asked for " + fresh.lastPathReceived() + " and answers " + b.status() + ".");
        System.out.println("  with anything after the address, even one slash, NGINX cuts the matched prefix off the path it passes on.");
        nginx.apply(without);
    }

    /** The new service goes down. The moved route fails; every other route carries on. */
    private static void five(NginxRouter nginx, Browser customer, NewService fresh) {
        System.out.println("FIVE. The new service goes down.");
        fresh.stop();
        System.out.println("  " + tenRequests(customer, "/api/prices/SKU-1", "price") + ". " + tenRequests(customer, "/api/stock/SKU-1", "stock") + ".");
        nginx.apply(NginxConfig.everythingOnTheOldShop().withLegacyCacheRule());
        System.out.println("  roll back: the one location removed, and a reload. " + tenRequests(customer, "/api/prices/SKU-1", "price") + ".");
        fresh.startAgain();
        nginx.apply(NginxConfig.everythingOnTheOldShop().withLegacyCacheRule().moveAndStopLooking("/api/prices/"));
        System.out.println("  the new service comes back, and one more reload moves prices to it again: " + tenPriceRequests(customer) + ".");
    }

    /** The old shop's cookie means nothing to the new service. */
    private static void six(NginxRouter nginx, OldShop old, NewService fresh) {
        System.out.println("SIX. The bill.");
        Browser shopper = new Browser(nginx.address());
        shopper.post("/api/basket/items?sku=SKU-1");
        shopper.post("/api/basket/items?sku=SKU-2");
        Answer basket = shopper.post("/api/basket/items?sku=SKU-3");
        String cookie = OldShop.SESSION_COOKIE + "=" + shopper.cookies().get(OldShop.SESSION_COOKIE);
        System.out.println("  a customer puts 3 items in the basket. the old shop answers \"" + basket.body() + "\" and sets the cookie " + cookie + ".");
        NginxConfig checkoutMoved = nginx.current().moveAndStopLooking("/api/checkout");
        nginx.apply(checkoutMoved);
        Answer onNew = shopper.post("/api/checkout");
        System.out.println("  checkout moves to the new service. it receives the cookie " + fresh.lastCookieReceived() + " and has no use for it: "
                + onNew.status() + ", " + onNew.body() + ".");
        nginx.apply(NginxConfig.everythingOnTheOldShop().withLegacyCacheRule().moveAndStopLooking("/api/prices/"));
        Answer onOld = shopper.post("/api/checkout");
        System.out.println("  checkout moved back to the old shop: " + onOld.status() + ", " + onOld.body() + ".");
        int oldShopRoutes = (onOld.fromOldShop() ? 1 : 0);
        for (String[] page : PAGES) {
            if (shopper.get(page[1]).fromOldShop()) {
                oldShopRoutes++;
            }
        }
        System.out.println("  checkout cannot move until the basket does. the old shop still serves " + oldShopRoutes + " of "
                + (PAGES.length + 1) + " routes: stock, basket, checkout and orders.");
        System.out.println("  and three things to run now, not one: 1 NGINX container, the old shop and the new service, and a configuration file that decides who answers.");
    }

    static String describePages(Browser customer) {
        List<String> parts = new ArrayList<>();
        int working = 0;
        int oldShop = 0;
        int newService = 0;
        for (String[] page : PAGES) {
            Answer a = customer.get(page[1]);
            parts.add(page[0] + " " + a.status());
            if (a.status() == 200) {
                working++;
                if (a.fromOldShop()) {
                    oldShop++;
                } else if (a.fromNewService()) {
                    newService++;
                }
            }
        }
        return String.join(", ", parts) + ". pages that work: " + working + " of " + PAGES.length
                + " (" + oldShop + " from the old shop, " + newService + " from the new service)";
    }

    static String tenPriceRequests(Browser customer) {
        int oldShop = 0;
        int newService = 0;
        for (int i = 0; i < TEN; i++) {
            Answer a = customer.get("/api/prices/SKU-1");
            if (a.fromOldShop()) {
                oldShop++;
            } else if (a.fromNewService()) {
                newService++;
            }
        }
        return TEN + " price requests: " + oldShop + " from the old shop, " + newService + " from the new service";
    }

    static String tenRequests(Browser customer, String path, String what) {
        int ok = 0;
        int badGateway = 0;
        String servedBy = "";
        for (int i = 0; i < TEN; i++) {
            Answer a = customer.get(path);
            if (a.status() == 200) {
                ok++;
                servedBy = who(a);
            } else if (a.status() == 502) {
                badGateway++;
            }
        }
        if (badGateway == TEN) {
            return TEN + " " + what + " requests: " + badGateway + " answered 502 Bad Gateway, by NGINX itself";
        }
        return TEN + " " + what + " requests: " + ok + " answered 200, by the " + servedBy;
    }

    static String who(Answer a) {
        if (a.fromOldShop()) {
            return "old shop";
        }
        if (a.fromNewService()) {
            return "new service";
        }
        return "router itself";
    }
}
