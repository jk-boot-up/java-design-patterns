package com.jk.explore.apigateway;

import java.util.List;

/**
 * The version without a gateway, and the reason the gateway exists.
 *
 * There is nothing stupid about this class. It is the obvious thing to write:
 * the app needs four pieces of information, so it asks four services. It works.
 * The demo runs it and it produces the correct page.
 *
 * <p>Three costs are built into it, and each one is pinned by a test rather than
 * asserted in a comment. It crosses the mobile network four times instead of
 * once, so the shopper waits four times as long. It checks the access token four
 * times, because each service insists, and that logic is repeated at every call
 * site — and the web client repeats it again, slightly differently. And it treats
 * all four services as equally essential, so the day Recommendations goes down,
 * a shopper who wanted to know the price of an espresso machine gets an error
 * page instead.
 */
public final class NaiveMobileApp {

    private final AuthService auth;
    private final StoreServices services;
    private final String token;

    public NaiveMobileApp(AuthService auth, StoreServices services, String token) {
        this.auth = auth;
        this.services = services;
        this.token = token;
    }

    public ProductPage productPage(String sku) {
        // Four round trips over the mobile network, and the token checked at
        // each one because that is what every service demands.
        auth.check(token);
        Product product = services.catalog().invoke(sku);

        auth.check(token);
        Money price = services.pricing().invoke(sku);

        auth.check(token);
        boolean inStock = services.inventory().invoke(sku);

        auth.check(token);
        List<String> recommended = services.recommendations().invoke(sku);

        return new ProductPage(sku, product.name(), product.description(),
                price, inStock, recommended);
    }
}
