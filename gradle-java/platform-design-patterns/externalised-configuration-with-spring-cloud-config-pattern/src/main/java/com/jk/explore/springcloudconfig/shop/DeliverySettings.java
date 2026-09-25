package com.jk.explore.springcloudconfig.shop;

import jakarta.validation.constraints.DecimalMax;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotNull;
import java.math.BigDecimal;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.validation.annotation.Validated;

/**
 * The delivery settings, filled from whatever the config server sent.
 *
 * <p>{@code @RefreshScope} is the annotation that matters. It means: when the shop is told to
 * refresh, throw this object away, and build a new one from the newly fetched settings the next
 * time somebody asks for it. The checkout asks for it on every quote, so a refresh reaches the
 * very next quote.
 *
 * <p>The range is a guard. A threshold below five pounds would give delivery away on nearly
 * every basket, and one above two hundred would mean the offer does not exist.
 */
@RefreshScope
@Validated
@ConfigurationProperties(prefix = "delivery")
public class DeliverySettings {

    @NotNull
    @DecimalMin("5.00")
    @DecimalMax("200.00")
    private BigDecimal freeOver;

    @NotNull
    @DecimalMin("0.00")
    @DecimalMax("50.00")
    private BigDecimal standard;

    public BigDecimal getFreeOver() {
        return freeOver;
    }

    public void setFreeOver(BigDecimal freeOver) {
        this.freeOver = freeOver;
    }

    public BigDecimal getStandard() {
        return standard;
    }

    public void setStandard(BigDecimal standard) {
        this.standard = standard;
    }
}
