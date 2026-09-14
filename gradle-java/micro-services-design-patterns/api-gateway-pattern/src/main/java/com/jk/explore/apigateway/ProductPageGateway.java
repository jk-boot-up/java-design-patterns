package com.jk.explore.apigateway;

import java.util.List;

/**
 * The pattern. One service that sits in front of the other four and answers a
 * whole product page in a single call.
 *
 * It does four things and refuses to do a fifth. It checks the access token
 * once, at the edge, so no service behind it has to. It calls the services it
 * needs, over the fast internal network. It knows that Recommendations is
 * optional and every other service is not, so it lets that one call fail without
 * losing the page. And it returns one object shaped the way the app wants to
 * display it, so the app never learns four addresses or four response shapes.
 *
 * <p>The fifth thing — deciding prices, applying discounts, judging whether a
 * product may be sold — it does not do. A gateway that starts making business
 * decisions is a service that owns no data and makes decisions about everyone
 * else's, and it becomes the hardest thing in the system to change. That is the
 * one line in this class worth remembering, and it is a line about what is
 * <em>absent</em>.
 */
public final class ProductPageGateway {

    private final AuthService auth;
    private final StoreServices services;
    private final CallLog log;

    public ProductPageGateway(AuthService auth, StoreServices services, CallLog log) {
        this.auth = auth;
        this.services = services;
        this.log = log;
    }

    /**
     * Everything the app needs to draw a product page, in one answer.
     *
     * @throws IllegalArgumentException if the token is not a signed-in shopper's
     * @throws ServiceUnavailableException if a service the page cannot do
     *         without fails to answer
     */
    public ProductPage productPage(String token, String sku) {
        Customer customer = auth.check(token);
        log.note("Gateway", "AUTH", "one token check for " + customer);

        Product product = services.catalog().invoke(sku);
        Money price = services.pricing().invoke(sku);
        boolean inStock = services.inventory().invoke(sku);
        List<String> recommended = recommendationsOrNone(sku);

        return new ProductPage(sku, product.name(), product.description(),
                price, inStock, recommended);
    }

    /**
     * Suggestions if they arrive, an empty list if they do not.
     *
     * This is the only {@code catch} in the class, and it is here rather than
     * around all four calls on purpose. Losing the suggestions costs the shopper
     * nothing. Losing the price would mean showing a page with no price on it,
     * which is worse than showing an error, so a Pricing failure is allowed to
     * travel all the way out.
     */
    private List<String> recommendationsOrNone(String sku) {
        try {
            return services.recommendations().invoke(sku);
        } catch (ServiceUnavailableException e) {
            log.note("Gateway", "DEGRADED", "page served without suggestions");
            return List.of();
        }
    }
}
