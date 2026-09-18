package com.jk.explore.bff.real.mobile;

import java.util.LinkedHashMap;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

/**
 * One endpoint, named after a screen.
 *
 * <p>Read the path before the code. {@code /phone/product-screen/{sku}} belongs to one
 * team and can have a field added to it this week. {@code /api/products/{sku}} belongs
 * to everybody and therefore to nobody in particular. That difference is the
 * distinguishing question of the whole pattern, and here it is visible in a URL.
 *
 * <p>Six fields come back, all flat, all in the form the screen draws them: the price
 * is a string with a pound sign in it, the rating is a number that goes next to a star,
 * and the delivery promise is a whole English sentence. Nothing is left for the phone
 * to work out.
 */
@RestController
public class ProductScreenController {

    private final Shop shop;

    public ProductScreenController(Shop shop) {
        this.shop = shop;
    }

    @GetMapping("/phone/product-screen/{sku}")
    public Map<String, Object> productScreen(@PathVariable String sku) {
        // Four calls, not five. The fifth service is reachable and is not asked.
        Map<String, Object> catalog = shop.catalog(sku);
        Map<String, Object> pricing = shop.pricing(sku);
        Map<String, Object> inventory = shop.inventory(sku);
        Map<String, Object> reviews = shop.reviews(sku);

        Map<String, Object> screen = new LinkedHashMap<>();
        screen.put("title", catalog.get("title"));
        screen.put("price", Money.format(((Number) pricing.get("nowPence")).intValue()));
        screen.put("image", catalog.get("thumbnail"));
        screen.put("rating", reviews.get("average"));
        screen.put("ratingCount", reviews.get("count"));
        screen.put("delivery", deliveryPromise(inventory));
        return screen;
    }

    /**
     * The label the discount gets, which the phone prints without deciding anything.
     *
     * <p>Its own endpoint rather than a seventh field, because the phone's product
     * screen draws six things and a backend that quietly grows a seventh is how this
     * pattern turns back into a shared endpoint over a year.
     */
    @GetMapping("/phone/saving/{sku}")
    public Map<String, Object> saving(@PathVariable String sku) {
        Map<String, Object> pricing = shop.pricing(sku);
        int listPence = ((Number) pricing.get("listPence")).intValue();
        int nowPence = ((Number) pricing.get("nowPence")).intValue();
        return Map.of(
                "client", "phone app",
                "saving", SavingRules.savingLabel(listPence, nowPence));
    }

    /**
     * Three services and a calendar, joined into one sentence.
     *
     * <p>This is the field the shared endpoint could not give anybody, because it is
     * not a field any service owns. Four lines of code, in the phone team's own
     * repository, in the phone team's own deployment — and the thing they waited five
     * weeks for when the only endpoint was a shared one.
     */
    private static String deliveryPromise(Map<String, Object> inventory) {
        if (!Boolean.TRUE.equals(inventory.get("inStock"))) {
            return "Out of stock";
        }
        return "Free delivery, arrives " + inventory.get("nextDelivery");
    }
}
