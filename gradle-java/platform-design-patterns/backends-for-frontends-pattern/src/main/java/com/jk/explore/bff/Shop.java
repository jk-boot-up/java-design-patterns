package com.jk.explore.bff;

import java.util.List;

/**
 * The shop's five existing services, as they were before anybody wrote a backend for
 * a frontend.
 *
 * <p>These are the givens. Every design in this project -- the chatty phone, the one
 * shared endpoint, and the two backends the pattern ends up with -- reads from exactly
 * these five and invents nothing. That is deliberate: the pattern is not about
 * changing what the shop knows, it is about who assembles it and for whom.
 *
 * <p>The data is fixed rather than random so that every number the demo prints is the
 * same on every machine on every run. A size that moved between runs would make the
 * comparison at the heart of this project unquotable.
 */
public final class Shop {

    private final CallLog log;

    public Shop(CallLog log) {
        this.log = log;
    }

    /** What the product is. The long description is the web page's, not the phone's. */
    public Doc catalog(String sku) {
        log.record(CallLog.Origin.INTERNAL, "catalog");
        return Doc.doc()
                .put("sku", sku)
                .put("title", "Copper Filter Coffee Maker, 1 Litre")
                .put("brand", "Fenwick Home")
                .put("description",
                        "A hand-finished copper brewer for filter coffee, with a borosilicate "
                                + "carafe and a stainless steel mesh that never needs a paper filter. "
                                + "The lid is cork, cut from offcuts, and the handle is beech. Brews "
                                + "one litre in four minutes and keeps it warm for forty. Dishwasher "
                                + "safe apart from the carafe, which is happier in a sink.")
                .put("materials", List.of("copper", "borosilicate glass", "beech", "cork"))
                .put("dimensions", Doc.doc()
                        .put("heightMm", 310)
                        .put("widthMm", 140)
                        .put("depthMm", 140)
                        .put("weightGrams", 1180))
                .put("images", List.of(
                        "https://img.shop.example/4417/hero-2000.jpg",
                        "https://img.shop.example/4417/angle-2000.jpg",
                        "https://img.shop.example/4417/detail-copper-2000.jpg",
                        "https://img.shop.example/4417/lifestyle-kitchen-2000.jpg",
                        "https://img.shop.example/4417/box-2000.jpg"))
                .put("thumbnail", "https://img.shop.example/4417/hero-320.jpg");
    }

    /** What it costs, in pence, before anybody decides how to write it down. */
    public Doc pricing(String sku) {
        log.record(CallLog.Origin.INTERNAL, "pricing");
        return Doc.doc()
                .put("listPence", 5999)
                .put("nowPence", 4799)
                .put("currency", "GBP")
                .put("vatRate", 20)
                .put("promotionCode", "AUTUMN20")
                .put("promotionEnds", "2026-10-31")
                // The higher price went up eleven days ago, which is not long enough
                // for the shop to advertise the difference as a saving. The shop knows
                // this. Whether a screen acts on it is Act 5's whole subject.
                .put("listPriceHeldLongEnough", false);
    }

    /** Whether it can be sent, and from where. */
    public Doc inventory(String sku) {
        log.record(CallLog.Origin.INTERNAL, "inventory");
        return Doc.doc()
                .put("inStock", true)
                .put("quantity", 41)
                .put("warehouse", "Rugby")
                .put("nextDelivery", "2026-09-18")
                .put("reservedForOtherBaskets", 6);
    }

    /** What other people thought of it. The bodies are most of the weight. */
    public Doc reviews(String sku) {
        log.record(CallLog.Origin.INTERNAL, "reviews");
        return Doc.doc()
                .put("average", 4.6)
                .put("count", 218)
                .put("latest", List.of(
                        "Four minutes, and it really is four minutes. The copper keeps it hot "
                                + "long enough that I have stopped reheating cups in the microwave.",
                        "Handsome thing. The mesh filter took one wash to stop tasting of metal, "
                                + "and since then the coffee has been better than my old machine.",
                        "Arrived with a dented box but the brewer was fine. Customer services "
                                + "sent a replacement lid anyway, which I did not need."));
    }

    /** What else the customer might buy. */
    public Doc recommendations(String sku) {
        log.record(CallLog.Origin.INTERNAL, "recommendations");
        return Doc.doc()
                .put("related", List.of("SKU-9002", "SKU-1183", "SKU-7741", "SKU-2260"))
                .put("model", "collaborative-v4")
                .put("boughtTogether", List.of("SKU-9002", "SKU-4410"));
    }
}
