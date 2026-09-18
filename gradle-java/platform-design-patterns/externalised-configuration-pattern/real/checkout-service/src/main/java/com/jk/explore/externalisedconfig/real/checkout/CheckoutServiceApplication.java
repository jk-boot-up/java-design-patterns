package com.jk.explore.externalisedconfig.real.checkout;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.ConfigurationPropertiesScan;

/**
 * The checkout service — Tier 1's ConfiguredCheckout, over HTTP.
 *
 * <p>Read {@link DeliverySettings} and {@link QuoteController} in that order.
 * Between them they are the entire pattern; this class only starts the
 * process.
 */
@SpringBootApplication
@ConfigurationPropertiesScan
public class CheckoutServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(CheckoutServiceApplication.class, args);
    }
}
