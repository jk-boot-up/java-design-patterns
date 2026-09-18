package com.jk.explore.bff;

import java.util.List;

/**
 * The phone's backend. Owned by the phone team, changed by the phone team, deployed
 * with the phone team's releases.
 *
 * <p>Read what it returns before reading how. Six fields, all of them flat, all of them
 * already in the form the screen draws them: the price is a string with a pound sign in
 * it, the rating is a number the phone puts straight next to a star, and the delivery
 * promise is a whole English sentence. Nothing is left for the phone to work out.
 *
 * <p>That is the second half of the pattern and it is the half people miss. Trimming
 * bytes is the obvious win. The quieter win is that the *thinking* moved: the join
 * across three services, the clock arithmetic, and the sentence are now done once, in
 * the data centre, in a process that can be fixed in an afternoon — instead of three
 * times, in three app stores, in versions of the app that customers will still be
 * running in two years.
 */
public final class MobileBff implements ClientBackend {

    private final Shop shop;
    private final CallLog log;
    private final SavingRules savingRules;

    public MobileBff(Shop shop, CallLog log) {
        this(shop, log, SavingRules.current());
    }

    public MobileBff(Shop shop, CallLog log, SavingRules savingRules) {
        this.shop = shop;
        this.log = log;
        this.savingRules = savingRules;
    }

    @Override
    public String client() {
        return "phone app";
    }

    @Override
    public Doc productScreen(String sku) {
        log.record(CallLog.Origin.DEVICE, "mobile-bff");
        Doc catalog = shop.catalog(sku);
        Doc pricing = shop.pricing(sku);
        Doc inventory = shop.inventory(sku);
        Doc reviews = shop.reviews(sku);

        return Doc.doc()
                .put("title", catalog.get("title"))
                .put("price", Money.format((int) pricing.get("nowPence")))
                .put("image", catalog.get("thumbnail"))
                .put("rating", reviews.get("average"))
                .put("ratingCount", reviews.get("count"))
                .put("delivery", deliveryPromise(inventory));
    }

    /** The label the discount gets, which the phone prints without deciding anything. */
    public String savingLabel(String sku) {
        Doc pricing = shop.pricing(sku);
        return savingRules.savingLabel(
                (int) pricing.get("listPence"),
                (int) pricing.get("nowPence"),
                (boolean) pricing.get("listPriceHeldLongEnough"));
    }

    /**
     * Three services and a calendar, joined into one sentence.
     *
     * <p>This is the field the shared endpoint could not give anybody, because it is
     * not a field any service owns. It is stock, plus a delivery date, plus a promise
     * the phone's designer wrote — and it is four lines of code in the one place that
     * is allowed to care.
     */
    private static String deliveryPromise(Doc inventory) {
        boolean inStock = (boolean) inventory.get("inStock");
        if (!inStock) {
            return "Out of stock";
        }
        return "Free delivery, arrives " + inventory.get("nextDelivery");
    }

    /** What the screen draws, so the demo can check nothing was sent that is not drawn. */
    public List<String> screenFields() {
        return Screens.PHONE;
    }
}
