package com.jk.explore.springcloudconfig.shop;

import java.math.BigDecimal;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

/**
 * The line across the top of the home page: "Free delivery on orders over £50.00".
 *
 * <p>It reads the same setting as the checkout, but it reads it once. The value is copied into
 * a field when the shop starts, and this object is an ordinary one that lives as long as the
 * shop does. A refresh does not rebuild it, so it keeps the number it started with. Nothing
 * here is unusual code; that is the point.
 */
@Component
public class PromotionBanner {

    private final String text;

    public PromotionBanner(@Value("${delivery.free-over}") BigDecimal freeOver) {
        this.text = "Free delivery on orders over " + Money.pounds(freeOver);
    }

    public String text() {
        return text;
    }
}
