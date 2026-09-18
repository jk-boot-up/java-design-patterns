package com.jk.explore.bff.real.web;

import java.util.LinkedHashMap;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

/**
 * One endpoint, named after a page.
 *
 * <p>Fifteen fields, and worth saying plainly: this response is bigger than the shared
 * endpoint's would have been in places and smaller in others, and neither is the point.
 * The desktop page has room for the description, the specification table, five
 * full-size images and the three most recent reviews, so it asks for them.
 *
 * <p>Compare the {@code delivery} field with the phone's. The phone is sent a whole
 * sentence; this page is sent the bare date, because it has a delivery panel with its
 * own layout and wants the parts. Two backends over the same data, disagreeing about
 * what a product is, is not an inconsistency waiting to be tidied up. It is the pattern
 * working, and a shared endpoint is structurally incapable of it.
 */
@RestController
public class ProductPageController {

    private final Shop shop;

    public ProductPageController(Shop shop) {
        this.shop = shop;
    }

    @GetMapping("/desktop/product-page/{sku}")
    public Map<String, Object> productPage(@PathVariable String sku) {
        Map<String, Object> catalog = shop.catalog(sku);
        Map<String, Object> pricing = shop.pricing(sku);
        Map<String, Object> inventory = shop.inventory(sku);
        Map<String, Object> reviews = shop.reviews(sku);
        Map<String, Object> recommendations = shop.recommendations(sku);

        int listPence = ((Number) pricing.get("listPence")).intValue();
        int nowPence = ((Number) pricing.get("nowPence")).intValue();

        Map<String, Object> page = new LinkedHashMap<>();
        page.put("title", catalog.get("title"));
        page.put("brand", catalog.get("brand"));
        page.put("description", catalog.get("description"));
        page.put("materials", catalog.get("materials"));
        page.put("dimensions", catalog.get("dimensions"));
        page.put("images", catalog.get("images"));
        page.put("price", Money.format(nowPence));
        page.put("wasPrice", Money.format(listPence));
        page.put("saving", SavingRules.savingLabel(
                listPence, nowPence, Boolean.TRUE.equals(pricing.get("listPriceHeldLongEnough"))));
        page.put("rating", reviews.get("average"));
        page.put("ratingCount", reviews.get("count"));
        page.put("reviews", reviews.get("latest"));
        page.put("delivery", inventory.get("nextDelivery"));
        page.put("stock", inventory.get("quantity"));
        page.put("related", recommendations.get("related"));
        return page;
    }

    /** The same saving label, on its own, so the demo can put the two side by side. */
    @GetMapping("/desktop/saving/{sku}")
    public Map<String, Object> saving(@PathVariable String sku) {
        Map<String, Object> pricing = shop.pricing(sku);
        return Map.of(
                "client", "desktop store",
                "saving", SavingRules.savingLabel(
                        ((Number) pricing.get("listPence")).intValue(),
                        ((Number) pricing.get("nowPence")).intValue(),
                        Boolean.TRUE.equals(pricing.get("listPriceHeldLongEnough"))));
    }
}
