package com.jk.explore.springcloudconfig.shop;

import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.ConfigurationPropertiesScan;

/**
 * The shop, as a Spring Boot web application. The demo starts it, stops it and starts it
 * again; see {@code Shop} for how.
 *
 * <p>It has two pages. {@code /quote} prices delivery on a basket, and {@code /banner} is the
 * line across the top of the home page that advertises free delivery.
 */
@SpringBootApplication
@ConfigurationPropertiesScan
public class ShopApplication {
}
