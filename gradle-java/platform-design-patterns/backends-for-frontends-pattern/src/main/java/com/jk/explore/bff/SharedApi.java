package com.jk.explore.bff;

import java.util.List;

/**
 * The second design, and the one that looks like the obvious fix: one endpoint,
 * {@code GET /api/products/4417}, owned by one team, serving every client there is.
 *
 * <p>It solves the real problem the chatty phone had. Five calls become one, and the
 * four extra round trips move off the customer's connection and into the data centre
 * where they are nearly free. That much is a genuine improvement and this project does
 * not pretend otherwise.
 *
 * <p>What it cannot solve is shape. One endpoint publishes one document, and that
 * document has to satisfy the fussiest client, so it grows until it is the union of
 * everything anybody has ever needed. The phone downloads the union and draws six
 * fields of it.
 *
 * <p>The usual answer to that is {@link #product(String, List)} -- a {@code ?fields=}
 * parameter -- and it is worth taking seriously rather than dismissing, because it
 * genuinely fixes the size. What it does not fix is the other half of the problem,
 * which is who is allowed to change the shape. See {@link #joinedDelivery}.
 */
public final class SharedApi {

    private final Shop shop;
    private final CallLog log;

    public SharedApi(Shop shop, CallLog log) {
        this.shop = shop;
        this.log = log;
    }

    /** The whole union document: one call from the device, everything in the shop. */
    public Doc product(String sku) {
        log.record(CallLog.Origin.DEVICE, "shared-api");
        Doc catalog = shop.catalog(sku);
        Doc document = Doc.doc()
                .put("sku", sku)
                .put("title", catalog.get("title"))
                .put("brand", catalog.get("brand"))
                .put("description", catalog.get("description"))
                .put("materials", catalog.get("materials"))
                .put("dimensions", catalog.get("dimensions"))
                .put("images", catalog.get("images"))
                .put("thumbnail", catalog.get("thumbnail"))
                .put("pricing", shop.pricing(sku))
                .put("inventory", shop.inventory(sku))
                .put("reviews", shop.reviews(sku))
                .put("recommendations", shop.recommendations(sku));
        return document;
    }

    /**
     * The same endpoint with a {@code ?fields=} list, which trims the response to what
     * was asked for.
     *
     * <p>It works. The bytes come down to something close to what a tailored backend
     * would have sent, and a project that stopped here would have most of the benefit
     * for none of the extra processes. It is a reasonable thing to build and plenty of
     * shops run on it.
     */
    public Doc product(String sku, List<String> fields) {
        return product(sku).select(fields);
    }

    /**
     * The thing a field list cannot do, and the reason this class is the rejected
     * design rather than the answer.
     *
     * <p>The phone does not want {@code inventory.nextDelivery} and
     * {@code inventory.warehouse} and {@code pricing.promotionEnds}. It wants one line
     * of text that says "Free next-day delivery if you order in the next 3 hours",
     * which is three services joined, a clock consulted, and a sentence composed. That
     * is a new field, and a new field on a shared endpoint is a change to a document
     * every other client also receives.
     *
     * <p>So it goes in the owning team's queue, behind their own work, and it ships
     * when it ships. The phone team, who could have written this in an afternoon, wait.
     * That is the cost this pattern is actually paying to remove, and it is an
     * organisational cost rather than a technical one -- which is why measuring only
     * bytes misses it.
     */
    public static String joinedDelivery() {
        return "not available -- a field like this belongs to one client, and this "
                + "endpoint belongs to all of them";
    }
}
