package com.jk.explore.springcloudconfig.shop;

import java.math.BigDecimal;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * The shop's two pages.
 *
 * <p>The quote reads the threshold inside the request, every time, from the refreshable
 * settings. The banner hands back the text it built when the shop started.
 */
@RestController
public class ShopController {

    private final DeliverySettings settings;
    private final PromotionBanner banner;

    ShopController(DeliverySettings settings, PromotionBanner banner) {
        this.settings = settings;
        this.banner = banner;
    }

    /** One line of plain text, for example {@code goods £48.00 delivery £4.99 threshold £50.00}. */
    @GetMapping(value = "/quote", produces = "text/plain")
    public String quote(@RequestParam BigDecimal goods) {
        BigDecimal threshold = settings.getFreeOver();
        BigDecimal delivery = goods.compareTo(threshold) >= 0 ? BigDecimal.ZERO : settings.getStandard();
        String charge = delivery.signum() == 0 ? "FREE" : Money.pounds(delivery);
        return "goods " + Money.pounds(goods) + " delivery " + charge + " threshold " + Money.pounds(threshold);
    }

    @GetMapping(value = "/banner", produces = "text/plain")
    public String banner() {
        return banner.text();
    }
}
