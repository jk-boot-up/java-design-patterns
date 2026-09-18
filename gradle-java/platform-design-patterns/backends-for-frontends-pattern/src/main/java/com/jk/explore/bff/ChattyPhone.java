package com.jk.explore.bff;

/**
 * The first design, and the one most shops arrive at by accident: the phone talks to
 * every service itself.
 *
 * <p>It is not a silly design. Each service owns its own data and exposes its own
 * endpoint, which is exactly what the microservices chapter told everybody to build,
 * and nothing in the shop is duplicated. The problem is not in the data centre. It is
 * that the assembling happens on the far side of the customer's connection, so five
 * calls that would have cost almost nothing between our own machines now cost five
 * round trips over a train-window signal, one after another, before a single pixel can
 * be drawn.
 *
 * <p>And every one of those five responses arrives whole, because a service that
 * publishes one endpoint publishes one shape. The phone downloads all of it and draws
 * six fields.
 */
public final class ChattyPhone {

    private final Shop shop;
    private final CallLog log;

    public ChattyPhone(Shop shop, CallLog log) {
        this.shop = shop;
        this.log = log;
    }

    /**
     * Everything the phone has to fetch to draw one product screen. The returned
     * document is the concatenation of what came back, which is what the phone holds
     * in memory once all five calls have landed.
     */
    public Doc productScreen(String sku) {
        Doc everything = Doc.doc();
        everything.put("catalog", fetch("catalog", shop.catalog(sku)));
        everything.put("pricing", fetch("pricing", shop.pricing(sku)));
        everything.put("inventory", fetch("inventory", shop.inventory(sku)));
        everything.put("reviews", fetch("reviews", shop.reviews(sku)));
        everything.put("recommendations", fetch("recommendations", shop.recommendations(sku)));
        return everything;
    }

    /**
     * The service calls are recorded a second time, as calls from the device. The same
     * work is happening either way; what changes between this design and the others is
     * only which network it happens on, and that is the column that hurts.
     */
    private Doc fetch(String target, Doc response) {
        log.record(CallLog.Origin.DEVICE, target);
        return response;
    }
}
