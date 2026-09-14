package com.jk.explore.apigateway;

/**
 * The shop's mobile app, once there is a gateway to talk to.
 *
 * It knows one address and makes one call. Everything it used to know about
 * where Pricing lives, what shape Inventory answers in and whether
 * Recommendations is up has moved behind the gateway, which means those things
 * can now change without an app-store release.
 */
public final class MobileApp {

    private final RemoteCall<String, ProductPage> gateway;

    public MobileApp(ProductPageGateway gateway, String token,
                     SimulatedClock clock, CallLog log) {
        this.gateway = new RemoteCall<>("Gateway", StoreServices.MOBILE_LATENCY_MILLIS,
                sku -> gateway.productPage(token, sku), clock, log);
    }

    public ProductPage productPage(String sku) {
        return gateway.invoke(sku);
    }

    /** How many times the app has been over the mobile network. */
    public int remoteCalls() {
        return gateway.invocations();
    }
}
