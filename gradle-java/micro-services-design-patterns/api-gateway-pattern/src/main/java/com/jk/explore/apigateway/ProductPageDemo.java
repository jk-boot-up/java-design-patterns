package com.jk.explore.apigateway;

/**
 * Five acts, one product page, and the timelines that tell them apart.
 *
 * Both ways of building the page produce the same page. That is the point: you
 * cannot tell them apart by looking at the answer, only by looking at what it
 * cost to get it. So every act prints its timeline.
 */
public final class ProductPageDemo {

    private static final String SKU = "SKU-1234";

    public static void main(String[] args) {
        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
    }

    /** Four services, called from the phone. It works, and it is slow. */
    private static void actOne() {
        heading("1. No gateway: the app calls all four services itself");

        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        AuthService auth = new AuthService();
        NaiveMobileApp app = new NaiveMobileApp(auth,
                StoreServices.onMobileNetwork(clock, log), AuthService.validToken());

        ProductPage page = app.productPage(SKU);

        System.out.print(log.timeline());
        System.out.printf("  page: %s%n", page);
        System.out.printf("  four round trips over the mobile network, "
                + "%d token checks, shopper waited %dms%n%n", auth.checks(), log.elapsedMillis());
    }

    /** One call from the phone, four fast calls behind it. */
    private static void actTwo() {
        heading("2. With a gateway: the app makes one call");

        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        AuthService auth = new AuthService();
        ProductPageGateway gateway = new ProductPageGateway(auth,
                StoreServices.onInternalNetwork(clock, log), log);
        MobileApp app = new MobileApp(gateway, AuthService.validToken(), clock, log);

        ProductPage page = app.productPage(SKU);

        System.out.print(log.timeline());
        System.out.printf("  page: %s%n", page);
        System.out.printf("  %d round trip over the mobile network, "
                + "%d token check, shopper waited %dms%n%n",
                app.remoteCalls(), auth.checks(), log.elapsedMillis());
    }

    /** Recommendations is down. Without a gateway, so is the product page. */
    private static void actThree() {
        heading("3. Recommendations is down, and there is no gateway");

        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        StoreServices services = StoreServices.onMobileNetwork(clock, log);
        services.recommendations().failNext(1);
        NaiveMobileApp app = new NaiveMobileApp(new AuthService(), services,
                AuthService.validToken());

        try {
            app.productPage(SKU);
            System.out.println("  a page was returned");
        } catch (ServiceUnavailableException e) {
            System.out.print(log.timeline());
            System.out.printf("  no page: %s%n", e.getMessage());
            System.out.println("  the name, the price and the stock all arrived, "
                    + "and were thrown away with the error.");
            System.out.println("  the shopper wanted to know what an espresso "
                    + "machine costs. They cannot find out,");
            System.out.println("  because a feature nobody would miss is "
                    + "unavailable.\n");
        }
    }

    /** Recommendations is down, and the gateway knows it does not matter. */
    private static void actFour() {
        heading("4. Recommendations is down, and there is a gateway");

        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        AuthService auth = new AuthService();
        StoreServices services = StoreServices.onInternalNetwork(clock, log);
        services.recommendations().failNext(1);
        ProductPageGateway gateway = new ProductPageGateway(auth, services, log);
        MobileApp app = new MobileApp(gateway, AuthService.validToken(), clock, log);

        ProductPage page = app.productPage(SKU);

        System.out.print(log.timeline());
        System.out.printf("  page: %s%n", page);
        System.out.printf("  degraded: %s. The shopper sees the price, "
                + "the stock and no suggestions,%n", page.isDegraded());
        System.out.println("  which is a product page. Nobody is told anything "
                + "is wrong, because for them");
        System.out.println("  nothing is.\n");
    }

    /**
     * Catalog is down, and the gateway refuses rather than hides.
     *
     * The act exists because the previous one is the half everybody quotes. A
     * gateway is not a machine for making failures disappear: it is a place where
     * somebody has decided, one service at a time, whether a failure costs a
     * section of the page or the whole page. Recommendations costs a section.
     * The product's own name costs the page, because a product page with no
     * product on it is not a degraded page, it is a blank one.
     */
    private static void actFive() {
        heading("5. Catalog is down: the gateway refuses instead of degrading");

        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        AuthService auth = new AuthService();
        StoreServices services = StoreServices.onInternalNetwork(clock, log);
        services.catalog().failNext(1);
        ProductPageGateway gateway = new ProductPageGateway(auth, services, log);
        MobileApp app = new MobileApp(gateway, AuthService.validToken(), clock, log);

        try {
            app.productPage(SKU);
            System.out.println("  a page was returned");
        } catch (ServiceUnavailableException e) {
            System.out.print(log.timeline());
            System.out.printf("  no page: %s%n", e.getMessage());
            System.out.println("  the shopper is told, in 110ms, that the page "
                    + "cannot be shown right now.");
            System.out.println("  that is the design decision the pattern forces: "
                    + "for each service behind");
            System.out.println("  the gateway, somebody has said whether losing it "
                    + "costs a section of the");
            System.out.println("  page or the page itself. Recommendations costs "
                    + "a section. The name");
            System.out.println("  costs the page.\n");
        }
    }

    private static void heading(String text) {
        System.out.println("=".repeat(66));
        System.out.println(text);
        System.out.println("=".repeat(66));
    }
}
