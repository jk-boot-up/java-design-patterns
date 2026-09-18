package com.jk.explore.bff;

import java.util.List;

/**
 * What each screen actually puts in front of a human being.
 *
 * <p>This is the measurement everything else in the project is argued against, so it
 * is written down once, on its own, rather than left implied by whichever class
 * happens to be building a response. A field is on one of these lists only if a
 * customer can see it.
 *
 * <p>The phone list is short for a reason that has nothing to do with engineering
 * taste. A product screen on a four-inch display shows a picture, a name, a price, a
 * star rating and a delivery promise, and then it runs out of screen. The desktop page
 * shows all of that plus the description, the specification table, five images and the
 * three most recent reviews, because it has the room.
 */
public final class Screens {

    private Screens() {
    }

    /** The six things the phone's product screen draws. */
    public static final List<String> PHONE = List.of(
            "title",
            "price",
            "image",
            "rating",
            "ratingCount",
            "delivery");

    /** The same six, named the way the shared endpoint happens to name them. */
    public static final List<String> PHONE_ON_SHARED_API = List.of(
            "title",
            "pricing.nowPence",
            "thumbnail",
            "reviews.average",
            "reviews.count",
            "inventory.nextDelivery");

    /** Everything the desktop page draws. */
    public static final List<String> DESKTOP = List.of(
            "title",
            "brand",
            "description",
            "materials",
            "dimensions",
            "images",
            "price",
            "wasPrice",
            "saving",
            "rating",
            "ratingCount",
            "reviews",
            "delivery",
            "stock",
            "related");
}
