package com.jk.explore.discoveryconsul.instance;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

/**
 * One copy of the Pricing service. On startup Spring Cloud registers it with Consul, with a health
 * check, and answers with its own name so a caller can tell which copy replied.
 */
@SpringBootApplication
@RestController
public class PricingInstance {

    private final String name;

    public PricingInstance(@Value("${instance.name}") String name) {
        this.name = name;
    }

    @GetMapping("/price/{sku}")
    public String price(@PathVariable String sku) {
        return name;
    }
}
