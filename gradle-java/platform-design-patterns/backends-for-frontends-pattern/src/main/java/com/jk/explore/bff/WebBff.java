package com.jk.explore.bff;

import java.util.List;

/**
 * The desktop store's backend. Same shop, same five services, a different answer.
 *
 * <p>It is worth being clear that this one is *bigger* than the shared endpoint's
 * response would have been in some places and smaller in others, and that neither is
 * the point. The desktop page has room for the description, the specification table,
 * five full-size images and the three most recent reviews, so it asks for them. It also
 * has no use for a pre-written delivery sentence, because the page has a whole panel
 * for delivery, so this backend returns the parts and lets the page lay them out.
 *
 * <p>Two backends over the same data, disagreeing about what a product is. That
 * disagreement is not a design failure to be resolved. It is the pattern working.
 */
public final class WebBff implements ClientBackend {

    private final Shop shop;
    private final CallLog log;
    private final SavingRules savingRules;

    public WebBff(Shop shop, CallLog log) {
        this(shop, log, SavingRules.current());
    }

    public WebBff(Shop shop, CallLog log, SavingRules savingRules) {
        this.shop = shop;
        this.log = log;
        this.savingRules = savingRules;
    }

    @Override
    public String client() {
        return "desktop store";
    }

    @Override
    public Doc productScreen(String sku) {
        log.record(CallLog.Origin.DEVICE, "web-bff");
        Doc catalog = shop.catalog(sku);
        Doc pricing = shop.pricing(sku);
        Doc inventory = shop.inventory(sku);
        Doc reviews = shop.reviews(sku);
        Doc recommendations = shop.recommendations(sku);

        int listPence = (int) pricing.get("listPence");
        int nowPence = (int) pricing.get("nowPence");

        return Doc.doc()
                .put("title", catalog.get("title"))
                .put("brand", catalog.get("brand"))
                .put("description", catalog.get("description"))
                .put("materials", catalog.get("materials"))
                .put("dimensions", catalog.get("dimensions"))
                .put("images", catalog.get("images"))
                .put("price", Money.format(nowPence))
                .put("wasPrice", Money.format(listPence))
                .put("saving", savingRules.savingLabel(
                        listPence, nowPence, (boolean) pricing.get("listPriceHeldLongEnough")))
                .put("rating", reviews.get("average"))
                .put("ratingCount", reviews.get("count"))
                .put("reviews", reviews.get("latest"))
                .put("delivery", inventory.get("nextDelivery"))
                .put("stock", inventory.get("quantity"))
                .put("related", recommendations.get("related"));
    }

    /** The saving label this backend would print for the same product. */
    public String savingLabel(String sku) {
        Doc pricing = shop.pricing(sku);
        return savingRules.savingLabel(
                (int) pricing.get("listPence"),
                (int) pricing.get("nowPence"),
                (boolean) pricing.get("listPriceHeldLongEnough"));
    }

    /** What the page draws. */
    public List<String> screenFields() {
        return Screens.DESKTOP;
    }
}
