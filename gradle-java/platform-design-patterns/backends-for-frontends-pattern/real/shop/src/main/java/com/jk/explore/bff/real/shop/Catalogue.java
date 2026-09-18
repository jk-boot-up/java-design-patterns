package com.jk.explore.bff.real.shop;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicBoolean;
import org.springframework.stereotype.Component;

/**
 * The data the five services hold, and the one piece of it that can change while the
 * demo is running.
 *
 * <p>The values are the same values Tier 1 uses, field for field and word for word, so
 * that a reader can hold the two side by side. That is not tidiness: the whole claim of
 * a two-tier project is that the shape Tier 1 teaches is the shape a real deployment
 * has, and the claim is only checkable if the data underneath is identical.
 *
 * <p>Everything is immutable except {@link #listPriceHeldLongEnough}, which the demo
 * flips once to stand for the pricing team's review. Nothing else about the product
 * changes, which is the point: the divergence in the last act is caused by a decision
 * taken behind the services, not by anybody editing a backend.
 */
@Component
public class Catalogue {

    /**
     * Whether the higher price was genuinely in force long enough to be advertised
     * against. It starts true — before the review, nobody had asked the question — and
     * {@code POST /pricing/review} flips it to false.
     */
    private final AtomicBoolean listPriceHeldLongEnough = new AtomicBoolean(true);

    public void applyPricingReview() {
        listPriceHeldLongEnough.set(false);
    }

    public boolean listPriceHeldLongEnough() {
        return listPriceHeldLongEnough.get();
    }

    /** What the product is. The long description is the web page's, not the phone's. */
    public Map<String, Object> catalog(String sku) {
        Map<String, Object> dimensions = new LinkedHashMap<>();
        dimensions.put("heightMm", 310);
        dimensions.put("widthMm", 140);
        dimensions.put("depthMm", 140);
        dimensions.put("weightGrams", 1180);

        Map<String, Object> doc = new LinkedHashMap<>();
        doc.put("sku", sku);
        doc.put("title", "Copper Filter Coffee Maker, 1 Litre");
        doc.put("brand", "Fenwick Home");
        doc.put("description",
                "A hand-finished copper brewer for filter coffee, with a borosilicate "
                        + "carafe and a stainless steel mesh that never needs a paper filter. "
                        + "The lid is cork, cut from offcuts, and the handle is beech. Brews "
                        + "one litre in four minutes and keeps it warm for forty. Dishwasher "
                        + "safe apart from the carafe, which is happier in a sink.");
        doc.put("materials", List.of("copper", "borosilicate glass", "beech", "cork"));
        doc.put("dimensions", dimensions);
        doc.put("images", List.of(
                "https://img.shop.example/4417/hero-2000.jpg",
                "https://img.shop.example/4417/angle-2000.jpg",
                "https://img.shop.example/4417/detail-copper-2000.jpg",
                "https://img.shop.example/4417/lifestyle-kitchen-2000.jpg",
                "https://img.shop.example/4417/box-2000.jpg"));
        doc.put("thumbnail", "https://img.shop.example/4417/hero-320.jpg");
        return doc;
    }

    /** What it costs, in pence, before anybody decides how to write it down. */
    public Map<String, Object> pricing(String sku) {
        Map<String, Object> doc = new LinkedHashMap<>();
        doc.put("listPence", 5999);
        doc.put("nowPence", 4799);
        doc.put("currency", "GBP");
        doc.put("vatRate", 20);
        doc.put("promotionCode", "AUTUMN20");
        doc.put("promotionEnds", "2026-10-31");
        // The shop knows this. Whether a screen acts on it is the last act's subject,
        // and the answer turns out to depend on which backend you ask.
        doc.put("listPriceHeldLongEnough", listPriceHeldLongEnough.get());
        return doc;
    }

    /** Whether it can be sent, and from where. */
    public Map<String, Object> inventory(String sku) {
        Map<String, Object> doc = new LinkedHashMap<>();
        doc.put("inStock", true);
        doc.put("quantity", 41);
        doc.put("warehouse", "Rugby");
        doc.put("nextDelivery", "2026-09-18");
        doc.put("reservedForOtherBaskets", 6);
        return doc;
    }

    /** What other people thought of it. The bodies are most of the weight. */
    public Map<String, Object> reviews(String sku) {
        Map<String, Object> doc = new LinkedHashMap<>();
        doc.put("average", 4.6);
        doc.put("count", 218);
        doc.put("latest", List.of(
                "Four minutes, and it really is four minutes. The copper keeps it hot "
                        + "long enough that I have stopped reheating cups in the microwave.",
                "Handsome thing. The mesh filter took one wash to stop tasting of metal, "
                        + "and since then the coffee has been better than my old machine.",
                "Arrived with a dented box but the brewer was fine. Customer services "
                        + "sent a replacement lid anyway, which I did not need."));
        return doc;
    }

    /** What else the customer might buy. */
    public Map<String, Object> recommendations(String sku) {
        Map<String, Object> doc = new LinkedHashMap<>();
        doc.put("related", List.of("SKU-9002", "SKU-1183", "SKU-7741", "SKU-2260"));
        doc.put("model", "collaborative-v4");
        doc.put("boughtTogether", List.of("SKU-9002", "SKU-4410"));
        return doc;
    }
}
