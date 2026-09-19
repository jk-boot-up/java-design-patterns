package com.jk.explore.discoveryconsul.client;

import org.springframework.web.client.RestClient;

public class PricingClient {

    private final RestClient.Builder builder;

    PricingClient(RestClient.Builder loadBalancedBuilder) {
        this.builder = loadBalancedBuilder;
    }

    /** Asks whichever copy of pricing the balancer picks, by service name. Returns that copy's name. */
    public String price(String sku) {
        return builder.build().get().uri("http://pricing/price/" + sku).retrieve().body(String.class);
    }

    /** Asks one fixed address, the way a hardcoded URL does. */
    public String priceAt(String baseUrl, String sku) {
        return RestClient.create().get().uri(baseUrl + "/price/" + sku).retrieve().body(String.class);
    }
}
